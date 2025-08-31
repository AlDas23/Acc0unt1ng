import { useEffect, useState } from "react";
import { HistoryTable } from "../commonComponents/Common";
import Header from "../commonComponents/Header";


export default function CurrencyRatesPage() {
    const [data, setData] = useState([]);
    const [imageUrl, setImageUrl] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            try {
                document.title = "Currency Rates";

                const response = await fetch('http://localhost:5050/api/get/history/currencyrates');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result = await response.json();
                if (result.success) {
                    setData(result.data);
                }

                const plotResponse = await fetch('http://localhost:5050/api/get/plot/currencyrates');
                if (!plotResponse.ok) {
                    throw new Error('Network response was not ok');
                }
                const blob = await plotResponse.blob();
                const url = URL.createObjectURL(blob);
                setImageUrl(url);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();

        return () => {
            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }
        };
    }, [imageUrl]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('http://localhost:5050/api/add/currencyrates', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();
            if (result.success) {
                window.location.reload();
            } else {
                alert('Error: ' + (result.message || 'Failed to add currency rate'));
            }
        } catch (error) {
            console.error('Unexpected error:', error);
            alert('Unexpected error occurred');
        }
    };

    const Form = (options) => {
        return (
            <form action="/currency" method="post" onSubmit={handleSubmit}>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Currency</th>
                            <th>Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <input type="date" id="Date" name="Date" />
                            </td>
                            <td className="fields">
                                <select id="Currency" name="Currency" required>
                                    {options && options.currency.map((currency, index) => (
                                        <option key={currency} value={index}>{currency}</option>
                                    ))}
                                </select>
                            </td>
                            <td className="fields">
                                <input type="text" id="Rate" name="Rate" autoComplete="off" required />
                            </td>
                        </tr>
                    </tbody>
                </table>
                <br />
                <input type="submit" value="Submit" className="submitrec" />
            </form>
        );
    };

    return (
        <>
            <Header />
            <div className="currency-rates-page">
                <Form />
                <br />
                <div className="historyTable-split">
                    <h2>Currency Rates History</h2>
                    <div className="left-split">
                        <HistoryTable
                            columns={["Date", "Currency", "Rate"]}
                            data={data}
                        />
                    </div>
                    <div className="right-split">
                        <h2>Currency dynamics plot</h2>
                        <img id="CurrRatePlot" src={imageUrl} alt="Currency dynamics plot" />
                    </div>
                </div>
            </div>
        </>
    );
}