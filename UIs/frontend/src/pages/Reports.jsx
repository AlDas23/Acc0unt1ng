import { useEffect, useState } from "react";
import { backendURL } from "../commonComponents/Common";
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
    const [reportType, setReportType] = useState("");
    const [reportFormat, setReportFormat] = useState("percent");
    const [category, setCategory] = useState("");
    const [isCategoryFilterVisible, setIsCategoryFilterVisible] = useState(false);
    const [tableData, setTableData] = useState(null);
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        document.title = "Reports";
        // Fetch categories from backend when component mounts
        fetchCategories()
            .then(data => {
                setCategories(data);
            })
    }, []);

    const fetchCategories = () => {
        return fetch(`http://${backendURL}/api/get/list/categories_exp`,)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                return response.json();
            })
            .then(data => {
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

    const handleReportTypeChange = (e) => {
        const value = e.target.value;
        setReportType(value);
        categoryFilter(value);
    };

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

        if (reportType === "subcat" && (category === "" || category === "None")) {
            alert("Please select a category for sub-categories report.");
            return;
        }


        // Fetch report data based on selected type and format
        fetch(`http://${backendURL}/api/get/report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                report_type: reportType,
                report_format: reportFormat,
                category: category
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



    return (
        <>
            <Header />
            <div className="reports-page container">
                <h3>Reports view</h3>
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
                        <option value="ron">Converted to RON</option>
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
                        <option value="" disabled>Select a category</option>
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
                        Show report
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
