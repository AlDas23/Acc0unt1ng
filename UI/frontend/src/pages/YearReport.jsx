import { useState, useEffect } from "react";
import { HistoryTable, YearSelectorOnChange } from "../commonComponents/Common"
import Header from "../commonComponents/Header";
import '../assets/styles/ReportsPageStyles.css';

export default function YearReportPage() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currencyList, setCurrencyList] = useState([]);
    const [yearsList, setYearsList] = useState([]);
    const [currentYear, setCurrentYear] = useState(null);
    const [data, setData] = useState({
        income: [],
        expense: [],
        total: []
    });

    useEffect(() => {
        document.title = "Yearly Report";

        GetCurrencyList()
            .then(optionsData => {
                setCurrencyList(optionsData);
            })
            .catch(error => {
                setError('Failed to load currency list: ' + error.message);
                console.error('Error loading currency list:', error);
            });
        GetYearsList()
            .then(yearsData => {
                setYearsList(yearsData);
                setCurrentYear(yearsData[0]);
            })
            .catch(error => {
                setError('Failed to load years list: ' + error.message);
                console.error('Error loading years list:', error);
            });
    }, []);

    useEffect(() => {
        GetData('income', currentYear)
            .then(incomeData => {
                setData(prevData => ({ ...prevData, income: incomeData }));
            })
            .catch(error => {
                setError('Failed to load income data: ' + error.message);
                console.error('Error loading income data:', error);
            });
        GetData('expense', currentYear)
            .then(expenseData => {
                setData(prevData => ({ ...prevData, expense: expenseData }));
            })
            .catch(error => {
                setError('Failed to load expense data: ' + error.message);
                console.error('Error loading expense data:', error);
            });
        GetData('total', currentYear)
            .then(totalData => {
                setData(prevData => ({ ...prevData, total: totalData }));
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load total data: ' + error.message);
                console.error('Error loading total data:', error);
            });
    }, [currentYear]);

    const GetCurrencyList = () => {
        return fetch(`/api/get/list/currency`)
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
                    return data.currencies;
                } else {
                    throw new Error(data.message || 'Failed to load currency list');
                }
            })
            .catch(error => {
                console.error('Error fetching currency list:', error);
                alert('Unexpected error occurred while fetching currency list: ' + error.message);
            });
    }

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
            });
    }

    const GetData = (type, year) => {
        const url = `/api/get/report/year/${type}/${year}`;

        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            }
            )
            .then(data => {
                if (data.redirect) {
                    alert('Database is missing or corrupted. You will be redirected to the setup page.');
                    window.location.href = data.redirect;
                    return Promise.reject('Redirect initiated');
                }

                if (data.success) {
                    return data.data;
                } else {
                    throw new Error(data.message || "Failed to fetch data");
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                return [];
            })
    }

    const OnYearChange = (event) => {
        const selectedYear = event.target.value;
        setCurrentYear(selectedYear);
    }

    if (loading) {
        return (
            <>
                <Header />
                <div className="year-report-page">
                    <h1>Yearly Report</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="year-report-page">
                    <h1>Yearly Report</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="year-report-page">
                <h1>Yearly Report for <YearSelectorOnChange
                    yearsList={yearsList}
                    selectedYear={currentYear}
                    onYearChange={OnYearChange}
                    id="yearReport-year-selector"
                /></h1>
                <div className="row">
                    <div className="col-md-4">
                        <h3>Income</h3>
                        {data.income && (<HistoryTable
                            columns={["Month", ...currencyList, "Total in Main currency"]}
                            data={data.income}
                            tableId="income-table" />)}
                    </div>
                    <div className="col-md-4">
                        <h3>Expenses</h3>
                        {data.expense && (<HistoryTable
                            columns={["Month", ...currencyList, "Total in Main currency"]}
                            data={data.expense}
                            tableId="expense-table" />)}
                    </div>
                    <div className="col-md-3">
                        <h3>Total balance</h3>
                        {data.total && (<HistoryTable
                            columns={["Month", "Incomes", "Expenses", "Balance"]}
                            data={data.total}
                            tableId="total-table" />)}
                    </div>
                </div>
            </div>
        </>
    );
}