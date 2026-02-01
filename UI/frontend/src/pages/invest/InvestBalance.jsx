import { useState, useEffect } from "react";
import { HistoryTable } from "../commonComponents/Common"
import Header from "../commonComponents/Header";

export default function InvestBalancePage() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        document.title = "Invest Balance";
        fetchBalanceData()
            .then(balanceData => {
                setData(balanceData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load invest balance data: ' + error.message);
                console.error('Error loading invest balance data:', error);
                setLoading(false);
            });
    }, []);

    const fetchBalanceData = () => {
        return fetch(`/api/get/invest/balance`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            });
    }

    if (loading) {
        return (
            <>
                <Header />
                <div className="invest-balance container">
                    <h1>Invest Balance</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="invest-balance container">
                    <h1>Invest Balance</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="invest-balance container">
                <h1>Invest Balance</h1>
                {data && (<HistoryTable
                    data={data}
                    title="investBalanceTable"
                    columns={["Invest Person-Bank", "Stock", "Stock Amount", "Converted Value"]}
                    numberColumns={["2-6", "3-2"]}
                />)}
            </div>
        </>
    )
}