import { useState, useEffect } from "react";
import { HistoryTable } from "../commonComponents/Common"
import { useNavigate } from "react-router-dom";
import Header from "../commonComponents/Header";
import '../assets/styles/ReportsPageStyles.css';

export default function YearReportPage() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currencyList, setCurrencyList] = useState([]);
    const [data, setData] = useState({
        income: [],
        expense: [],
        total: []
    });

    const navigate = useNavigate();

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

        GetData('income')
            .then(incomeData => {
                setData(prevData => ({ ...prevData, income: incomeData }));
            })
            .catch(error => {
                setError('Failed to load income data: ' + error.message);
                console.error('Error loading income data:', error);
            });
        GetData('expense')
            .then(expenseData => {
                setData(prevData => ({ ...prevData, expense: expenseData }));
            })
            .catch(error => {
                setError('Failed to load expense data: ' + error.message);
                console.error('Error loading expense data:', error);
            });
        GetData('total')
            .then(totalData => {
                setData(prevData => ({ ...prevData, total: totalData }));
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load total data: ' + error.message);
                console.error('Error loading total data:', error);
            });
    }, []);

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
                    navigate(data.redirect);
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

    const GetData = (type) => {
        const url = `/api/get/report/year/${type}`;

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
                    navigate(data.redirect);
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
                <h1>Yearly Report</h1>
                <div className="row">
                    <div className="col-md-4">
                        <h3>Income</h3>
                        {data.income && (<HistoryTable
                            columns={["Month", ...currencyList, "Total in RON"]}
                            data={data.income}
                            tableId="income-table" />)}
                    </div>
                    <div className="col-md-4">
                        <h3>Expenses</h3>
                        {data.expense && (<HistoryTable
                            columns={["Month", ...currencyList, "Total in RON"]}
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