import { useEffect, useState } from "react";
import Header from "../commonComponents/Header"
import { CheckLegacy } from '../commonComponents/Common'
import { HistoryTable } from "../../commonComponents/Common";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';

function PlotComponent({ imageUrl }) {
    return (
        <>
            <h3>Currency dynamics plot</h3>
            <img id="StocksPlot" src={imageUrl} alt="Stocks dynamics plot" />
        </>
    );
}

function Forms({ options }) {
    return (
        <Form noValidate className="invest-stockprice-form" id="i-sp-form" onSubmit={(e) => {
            e.preventDefault();
            const form = e.target;
            const formDataObj = new FormData(form);
            const formObject = Object.fromEntries(formDataObj.entries());

            if (formObject.date === '' || formObject.stock === '' || isNaN(formObject.price) || formObject.currency === '') {
                alert("All fields are required!");
                return false;
            }

            if (formObject.price <= 0) {
                alert('Stock price must be greater than 0');
                return false;
            }

            // Send POST request
            fetch(`/api/add/invest/stockprice`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formObject),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert('Error: ' + (data.message || 'Failed to add invest transaction'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Date</Form.Label>
                </Col>
                <Col>
                    <Form.Control type="date" id="i-sp-date" name="date" defaultValue={new Date().toISOString().split('T')[0]} />
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Stock</Form.Label>
                </Col>
                <Col>
                    <Form.Select id="i-sp-stock" name="stock" defaultValue="">
                        <option value="" disabled></option>
                        {options.stocks.map((stock, index) => (
                            <option key={index} value={stock.id}>{stock.name} ({stock.symbol})</option>
                        ))}
                    </Form.Select>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Stock amount</Form.Label>
                </Col>
                <Col>
                    <Form.Control type="text" id="i-sp-stock-amount" name="stockAmount" autoComplete="off" />
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Currency</Form.Label>
                </Col>
                <Col>
                    <Form.Select id="i-sp-currency" name="currency" defaultValue="">
                        <option value="" disabled></option>
                        {options.currencies.map((currency, index) => (
                            <option key={index} value={currency.code}>{currency.code}</option>
                        ))}
                    </Form.Select>
                </Col>
            </Row>
            <Button variant="primary" type="submit" id="i-sp-submit">
                Add Stock Price
            </Button>
        </Form>
    )
}

export default function InvestStockPricePage() {
    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        document.title = "Invest Stock Price";

        const isLegacyResult = CheckLegacy();
        if (isLegacyResult) {
            setError("The current database is in legacy mode and does not support invest transactions.");
            setLoading(false);
        } else {
            const InitApp = async () => {
                const promises = [
                    GetOptions(),
                    GetHistory(),
                    GetPlot()
                ];

                const results = await Promise.all(promises)

                setOptions(results[0]);
                setHistory(results[1])
                setImageUrl(results[2].imageUrl);
                setLoading(false);
            }
            InitApp();
        }
    }, []);

    const GetOptions = () => {
        return fetch(`/api/get/options/invest-stockprice`)
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
                    return data.options;
                } else {
                    throw new Error(data.message || 'Failed to load options');
                }
            })
            .catch(error => {
                console.error('Error fetching options:', error);
                alert('Unexpected error occurred while fetching options: ' + error.message);
                throw error;
            });
    }

    const GetHistory = () => {
        return fetch(`/api/get/invest/history/stockprice`)
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
                    return data.history;
                } else {
                    throw new Error(data.message || 'Failed to load history');
                }
            })
            .catch(error => {
                console.error('Error fetching history:', error);
                alert('Unexpected error occurred while fetching history: ' + error.message);
                throw error;
            });
    }

    const GetPlot = () => {
        return fetch(`/api/get/plot/investstockprice`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
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
                    return data.plot;
                } else {
                    throw new Error(data.message || 'Failed to load plot');
                }
            })
            .catch(error => {
                console.error('Error fetching plot:', error);
                alert('Unexpected error occurred while fetching plot: ' + error.message);
                throw error;
            });
    }

    if (loading) {
        return (
            <>
                <Header />
                <div className="invest-stockPricePage container">
                    <h1>Invest Stock Price</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="invest-stockPricePage container">
                    <h1>Invest Stock Price</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }
    return (
        <>
            <Header />
            <div className="invest-stockPricePage container">
                <h1>Invest Stock Price</h1>
                <div className="stockprice-left">
                    {options && (<Forms options={options} />)}
                </div>
                <div className="stockprice-right">
                    {history && (<HistoryTable
                        data={history}
                        title="Stock Price History"
                        numberColumns={["3-2"]}
                    />)}
                    <PlotComponent imageUrl={imageUrl} />
                </div>
            </div>
        </>
    )
}