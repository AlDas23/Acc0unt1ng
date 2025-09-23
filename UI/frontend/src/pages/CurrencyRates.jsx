import { useEffect, useState } from "react";
import { HistoryTable } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/CurrRatePageStyles.css'

function FormsLegacy({ options }) {
    return (
        <Form noValidate className="form" id="form" onSubmit={(e) => {
            e.preventDefault();

            const form = e.target;
            const formDataObj = new FormData(form);
            const formObject = Object.fromEntries(formDataObj.entries());

            if (formObject.currency === "") {
                alert("Currency cannot be empty!")
                return false;
            }

            if (isNaN(formObject.Rate) || formObject.Rate <= 0) {
                alert("Rate is not a number!")
                return false;
            }

            // Send POST request
            fetch("/api/add/currencyrates", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formObject)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert('Error: ' + (data.message || 'Failed to add currency rate'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}>
            <Row>
                <Col xl="2">
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input type="date" id="inputDate" name="Date" defaultValue={new Date().toISOString().split('T')[0]} />
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select id="inputCurrency" name="Currency" defaultValue={""}>
                        <option value="" disabled></option>
                        {options.currency.map((currency, index) => (
                            <option value={currency} key={index}>{currency}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputRate">
                        Rate
                    </Form.Label>
                    <Form.Control type="text" id="inputRate" name="Rate" autoComplete="off" />
                </Col>
            </Row>
            <Row>
                <Button type="submit" value="Submit" id="SubmitButton">Submit</Button>
            </Row>
        </Form>
    );
};

function Forms({ options }) {
    return (
        <Form noValidate className="form" id="form" onSubmit={(e) => {
            e.preventDefault();

            const form = e.target;
            const formDataObj = new FormData(form);
            const formObject = Object.fromEntries(formDataObj.entries());

            if (formObject.currency_S === "" && formDataObj.currency_M) {
                alert("Currency cannot be empty!")
                return false;
            }

            if (formObject.currency_S === formDataObj.currency_M) {
                alert("Selected currencies cannot be same!")
                return false;
            }

            if (isNaN(formObject.Rate) || formObject.Rate <= 0) {
                alert("Rate is not a number!")
                return false;
            }

            // Send POST request
            fetch("/api/add/currencyrates", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formObject)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert('Error: ' + (data.message || 'Failed to add currency rate'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}>
            <Row>
                <Col xl="2">
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input type="date" id="inputDate" name="Date" defaultValue={new Date().toISOString().split('T')[0]} />
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputCurrency_M">
                        Currency Sell
                    </Form.Label>
                    <Form.Select id="inputCurrency_M" name="Currency_M" defaultValue={""}>
                        <option value="" disabled></option>
                        {options.currency.map((currency, index) => (
                            <option value={currency} key={index}>{currency}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputCurrency_S">
                        Currency Buy
                    </Form.Label>
                    <Form.Select id="inputCurrency_S" name="Currency_S" defaultValue={""}>
                        <option value="" disabled></option>
                        {options.currency.map((currency, index) => (
                            <option value={currency} key={index}>{currency}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputRate">
                        Rate
                    </Form.Label>
                    <Form.Control type="text" id="inputRate" name="Rate" autoComplete="off" />
                </Col>
            </Row>
            <Row>
                <Button type="submit" value="Submit" id="SubmitButton">Submit</Button>
            </Row>
        </Form>
    );
};

export default function CurrencyRatesPage() {
    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [isLegacy, setIsLegacy] = useState(null)

    useEffect(() => {
        document.title = "Currency Rates";
    }, []);

    useEffect(() => {
        // Check if db is legacy version
        CheckLegacy()
            .then(result => {
                if (result) {
                    console.info("Legacy DB used! Switching to legacy mode")
                    setIsLegacy(true)
                }
            })

        // Fetch options
        GetOptions()
            .then(optionsData => {
                setOptions(optionsData);
            })
            .catch(error => {
                setError('Failed to load options: ' + error.message);
                setLoading(false);
                console.error('Error loading options:', error);
            });

        // Fetch history
        GetHistory()
            .then(historyData => {
                setHistory(historyData);
            })
            .catch(error => {
                setError('Failed to load history: ' + error.message);
                setLoading(false);
                console.error('Error loading history:', error);
            });

        // Fetch plot image
        GetPlot()
            .then(url => {
                setImageUrl(url);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load plot: ' + error.message);
                setLoading(false);
                console.error('Error loading plot:', error);
            });

    }, []);

    const CheckLegacy = () => {
        return fetch(`/api/database/status`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.legacy) {
                    return true
                }
                else {
                    return false
                }
            })
            .catch(error => {
                console.error('Error fetching db status:', error);
                alert('Unexpected error occurred while fetching db status: ' + error.message);
                throw error;
            });
    }

    const GetOptions = () => {
        return fetch(`/api/get/options/currencyrates`)
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
        return fetch(`/api/get/history/currencyrates`)
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
        return fetch(`/api/get/plot/currencyrates`)
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
                <div className="currency-rates-page">
                    <h1>Currency Rates</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="currency-rates-page">
                    <h1>Currency Rates</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="currency-rates-page container">
                <h1>Currency Rates</h1>
                <div className="row" id="cr-forms">
                    {options && (isLegacy ? (<FormsLegacy
                        options={options}
                    />) : (<Forms options={options} />))}
                </div>
                <br />
                <div className="row">
                    <div className="col-md-4">
                        <h3>Currency Rates History</h3>
                        {history && (<HistoryTable
                            columns={isLegacy ?
                                ["Date", "Currency", "Rate"]
                                : ["ID", "Date", "Currency Sell", "Currency Buy", "Rate"]}
                            data={history}
                            tableId="CurrRateHistoryTable"
                            numberColumns={isLegacy ? ["2-4"] : ["4-4"]}
                        />)}
                    </div>
                    <div className="col-md-8" id="plot-col">
                        <h3>Currency dynamics plot</h3>
                        {imageUrl && (<img id="CurrRatePlot" src={imageUrl} alt="Currency dynamics plot" />)}
                    </div>
                </div>
            </div>
        </>
    );
}
