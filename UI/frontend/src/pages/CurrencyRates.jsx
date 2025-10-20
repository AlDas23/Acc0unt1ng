import { useEffect, useState } from "react";
import { HistoryTable } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import ToggleButton from 'react-bootstrap/ToggleButton';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/CurrRatePageStyles.css'

function LegacyPlotComponent({ imageUrl }) {
    return (
        <>
            <h3>Currency dynamics plot</h3>
            <img id="CurrRatePlot" src={imageUrl} alt="Currency dynamics plot" />
        </>
    );
}

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

            if (formObject.Currency_S === "" && formDataObj.Currency_M) {
                alert("Currency cannot be empty!")
                return false;
            }

            if (formObject.Currency_S === formDataObj.Currency_M) {
                alert("Selected currencies cannot be same!")
                return false;
            }

            if (isNaN(formObject.Rate) || formObject.Rate <= 0) {
                alert("Rate is not a number!")
                return false;
            }

            if (formObject.IsReverse) {
                formObject.Rate = 1 / formObject.Rate;
            }

            const payload = {
                date: formObject.date,
                currency_S: formDataObj.Currency_S,
                currency_M: formDataObj.Currency_M,
                rate: formDataObj.Rate
            }

            // Send POST request
            fetch("/api/add/currencyrates", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
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
                <Col xl="2">
                    <Form.Label htmlFor="checkReverse">
                        Calculate reverse rate
                    </Form.Label>
                    <Form.Check
                        type="switch"
                        id="checkReverse"
                        name="IsReverse"
                    />
                </Col>
            </Row>
            <Row>
                <Button type="submit" value="Submit" id="SubmitButton">Submit</Button>
            </Row>
        </Form>
    );
};

function PlotComponent({ currencyList, onFilterChange, FetchFilteredPlot, imageUrl }) {
    const rows = [];
    for (let i = 0; i < currencyList.length; i += 4) {
        rows.push(currencyList.slice(i, i + 4));
    }

    return (
        <>
            <h3 className="currPlotText">Currency dynamics plot</h3>
            <br />
            <p className="currPlotText">Select currencies to display on the plot:</p>
            <Form noValidate className="form" id="plotFilters" onSubmit={FetchFilteredPlot}>
                {rows.map((row) => (
                    <Row>
                        <ToggleButtonGroup type="checkbox">
                            {row.map((name, nameIndex) => (
                                <Form.Label key={name} className="checkbox-item">
                                    <ToggleButton
                                        name={name}
                                        id={`checkbox-${nameIndex}`}
                                        onChange={(e) => onFilterChange && onFilterChange(name, e.target.checked)}
                                    >
                                        {name}
                                    </ToggleButton>
                                </Form.Label>
                            ))}
                        </ToggleButtonGroup>
                    </Row>
                ))}
                <br />
                <Button type="submit" value="Submit" id="ApplyFiltersButton">Apply Filters</Button>
            </Form>
            <br />
            <img id="CurrRatePlot" src={imageUrl} alt="Currency dynamics plot" />
        </>
    )
};

export default function CurrencyRatesPage() {
    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [isLegacy, setIsLegacy] = useState(null);
    const [selectedCurrencies, setSelectedCurrencies] = useState([]);

    useEffect(() => {
        document.title = "Currency Rates";

        const initializeApp = async () => {
            try {
                // Check if DB is legacy
                const isLegacyResult = await CheckLegacy();
                if (isLegacyResult) {
                    console.info("Legacy DB schema used! Switching to legacy mode");
                    setIsLegacy(true);
                } else {
                    setIsLegacy(false);
                }

                const [optionsData, historyData, plotUrl] = await Promise.all([
                    GetOptions(),
                    GetHistory(),
                    GetPlot()
                ]);

                setOptions(optionsData);
                setHistory(historyData);
                setImageUrl(plotUrl);
                setLoading(false);

            } catch (error) {
                setError('Failed to initialize page: ' + error.message);
                setLoading(false);
                console.error('Error initializing page:', error);
            }
        };

        initializeApp();
    }, []);

    const CheckLegacy = () => {
        return fetch(`/api/database/status`)
            .then(response => response.json())
            .then(data => data.legacy || false)
            .catch(error => {
                console.error('Error fetching db status:', error);
                alert('Unexpected error occurred while fetching db status: ' + error.message);
                throw error;
            });
    };

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
        if (isLegacy) {
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
        } else {
            const filters = selectedCurrencies.length > 0 ? selectedCurrencies.join("-") : "None";

            return fetch(`/api/get/plot/currencyrates/${filters}`)
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
    }

    const onFilterChange = (currency, isChecked) => {
        if (isChecked) {
            setSelectedCurrencies(prev => [...prev, currency]);
        } else {
            setSelectedCurrencies(prev => prev.filter(c => c !== currency));
        }
    }

    const FetchFilteredPlot = (e) => {
        e.preventDefault();

        GetPlot()
            .then(plotUrl => {
                setImageUrl(plotUrl);
            })
            .catch(error => {
                console.error('Error fetching filtered plot:', error);
                alert('Unexpected error occurred while fetching filtered plot: ' + error.message);
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
                    <div className="col-md-8" id="  ">
                        {isLegacy ? (imageUrl && <LegacyPlotComponent imageUrl={imageUrl} />)
                            : (imageUrl && options && <PlotComponent
                                currencyList={options.currency}
                                onFilterChange={onFilterChange}
                                FetchFilteredPlot={FetchFilteredPlot}
                                imageUrl={imageUrl}
                            />)}
                    </div>
                </div>
            </div>
        </>
    );
}
