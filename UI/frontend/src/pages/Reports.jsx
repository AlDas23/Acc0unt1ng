import { useEffect, useState } from "react";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import "../assets/styles/ReportsPageStyles.css";

function CreateReportTable({ tableData }) {
    if (!tableData) return null;

    return (
        <table className="repTable table-bordered">
            <thead>
                <tr>
                    <th className="genRep_HeaderCell">Months</th>
                    {[...Array(12)].map((_, i) => (
                        <th key={i} className="genRep_HeaderCell">{i + 1}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {tableData.report_format === "ron" && (
                    <tr>
                        <td className="genRep_HeaderCell">Total</td>
                        {tableData.total.map((val, index) => (
                            <td key={index} className="genRep_DataCell">{val}</td>
                        ))}
                    </tr>
                )}
                {Object.entries(tableData.table_dict)
                    .sort((a, b) => a[0].localeCompare(b[0]))
                    .map(([rowName, rowData]) => (
                        <tr key={rowName}>
                            <td className="genRep_HeaderCell">{rowName}</td>
                            {rowData.map((val, index) => (
                                <td key={index} className="genRep_DataCell">{val}</td>
                            ))}
                        </tr>
                    ))}
            </tbody>
        </table>
    );
};

export default function ReportsPage() {
    const [loading, setLoading] = useState(true);
    const [reportType, setReportType] = useState("");
    const [reportYear, setReportYear] = useState("");
    const [reportFormat, setReportFormat] = useState("percent");
    const [category, setCategory] = useState("all");
    const [isCategoryFilterVisible, setIsCategoryFilterVisible] = useState(false);
    const [tableData, setTableData] = useState(null);
    const [categories, setCategories] = useState([]);
    const [years, setYears] = useState([]);

    useEffect(() => {
        document.title = "Reports";
        // Fetch categories from backend when component mounts
        fetchCategories()
            .then(data => {
                setCategories(data);
            })
        GetYearsList()
            .then(yearsData => {
                setYears(yearsData);
                setReportYear(yearsData[0]);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error loading years list:', error);
            });
    }, []);


    const fetchCategories = () => {
        return fetch(`/api/get/list/categories_exp`,)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                return response.json();
            })
            .then(data => {
                if (data.redirect) {
                    alert('Database is missing or corrupted. You will be redirected to the setup page.');
                    window.location.href = data.redirect;
                    return Promise.reject('Redirect initiated');
                }

                if (data.success) {
                    return data.categories;
                } else {
                    throw new Error(data.message || 'Failed to load categories');
                }
            })
            .catch(error => {
                console.error('Error fetching categories:', error);
                alert('Unexpected error occurred while fetching categories: ' + error.message);
                throw error;
            });
    };

    const GetYearsList = () => {
        return fetch(`/api/get/list/exYears`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.redirect) {
                    alert('Database is missing or corrupted. You will be redirected to the setup page.');
                    window.location.href = data.redirect;
                    return Promise.reject('Redirect initiated');
                }

                if (data.success) {
                    return data.data.years;
                } else {
                    throw new Error(data.message || 'Failed to load years list');
                }
            })
            .catch(error => {
                console.error('Error fetching years list:', error);
                alert('Unexpected error occurred while fetching years list: ' + error.message);
                throw error;
            });
    }

    const handleReportTypeChange = (e) => {
        const value = e.target.value;
        setReportType(value);
        categoryFilter(value);
    };

    const handleReportYearChange = (e) => {
        setReportYear(e.target.value);
    }

    const categoryFilter = (selectedReportType) => {
        if (selectedReportType === "inccat" || selectedReportType === "expcat") {
            setIsCategoryFilterVisible(false);
        } else {
            setIsCategoryFilterVisible(true);
        }
    };

    const validateReport = () => {
        if (reportType === "" || reportType === "None") {
            alert("Please select a report type.");
            return;
        }

        // Fetch report data based on selected type and format
        fetch(`/api/get/report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                report_type: reportType,
                report_format: reportFormat,
                category: category,
                report_year: reportYear.toString()
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    setTableData(data.table_data);
                } else {
                    alert('Error: ' + (data.message || 'Failed to generate report'));
                }
            })
            .catch(error => {
                console.error('Error fetching report:', error);
            });
    }

    if (loading) {
        return (
            <>
                <Header />
                <div className="reports-page container">
                    <h1>Reports view</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="reports-page container">
                <h3>Reports view</h3>
                {years && (<div className="row">
                    <label htmlFor="rep_year">Report year</label>
                    <select
                        name="rep_year"
                        id="rep_year"
                        value={reportYear}
                        onChange={handleReportYearChange}
                    >
                        {years.map((year, index) => (
                            <option key={index} value={year}>{year}</option>
                        ))}
                    </select>
                </div>)}
                <div className="row">
                    <label htmlFor="rep_type">Report type</label>
                    <select
                        name="rep_type"
                        id="rep_type"
                        value={reportType}
                        onChange={handleReportTypeChange}
                    >
                        <option value="" disabled>Select a type</option>
                        <option value="inccat">Income categories</option>
                        <option value="expcat">Expense categories</option>
                        <option value="subcat">Expense sub-categories</option>
                    </select>
                </div>
                <div className="row">
                    <label htmlFor="rep_format">Output format</label>
                    <select
                        name="rep_format"
                        id="rep_format"
                        value={reportFormat}
                        onChange={(e) => setReportFormat(e.target.value)}
                    >
                        <option value="percent">Converted to %</option>
                        <option value="ron">Converted to Main currency</option>
                    </select>
                </div>
                <div className="row">
                    <label
                        id="rep_cat_label"
                        htmlFor="rep_cat"
                        style={{ display: isCategoryFilterVisible ? 'inline' : 'none' }}
                    >
                        Category filter
                    </label>
                    <select
                        name="rep_cat"
                        id="rep_cat"
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        style={{ display: isCategoryFilterVisible ? 'inline' : 'none' }}
                        disabled={!isCategoryFilterVisible}
                    >
                        <option value="all">All</option>
                        {categories.map((cat, index) => (
                            <option key={index} value={cat}>{cat}</option>
                        ))}
                    </select>
                </div>
                <div className="row">
                    <Button
                        id="showTableButton"
                        onClick={validateReport}
                    >
                        {tableData === null ? "Show report" : "Refresh report"}
                    </Button>
                </div>
                <div id="rep-table" className="row">
                    <CreateReportTable
                        tableData={tableData} />
                </div>
            </div>
        </>
    );
}
