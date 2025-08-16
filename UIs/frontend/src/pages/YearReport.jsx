import { useState, useEffect } from "react";
import { HistoryTable } from "../commonComponents/Common"

export default function YearReportPage() {
    const [currencyList, setCurrencyList] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5050/api/get/list/currency')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    setCurrencyList(data.currencyList);
                } else {
                    throw new Error(data.message || 'Failed to load currency list');
                }
            })
            .catch(error => {
                console.error('Error fetching currency list:', error);
                alert('Unexpected error occurred while fetching currency list: ' + error.message);
            });
    }, []);

    const GetData = (type) => {
        const url = `http://localhost:5050/api/get/report/year/${type}`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            }
            )
            .then(data => {
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

    return (
        <div className="year-report-page">
            <h1>Yearly Report</h1>
            <div className="left-column">
                <h3>Income</h3>
                <HistoryTable
                    columns={["Month", ...currencyList, "Total in RON"]}
                    data={GetData('income')}
                    tableId="income-table" />
            </div>
            <div className="center-column">
                <h3>Expenses</h3>
                <HistoryTable
                    columns={["Month", ...currencyList, "Total in RON"]}
                    data={GetData('expense')}
                    tableId="expense-table" />
            </div>
            <div className="right-column">
                <h3>Total balance</h3>
                <HistoryTable
                    columns={["Month", "Incomes", "Expenses", "Balance"]}
                    data={GetData('total')}
                    tableId="total-table" />
            </div>
        </div>
    )
}