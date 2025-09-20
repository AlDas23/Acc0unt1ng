import { useEffect, useState } from "react";
import { HistoryTable } from "../commonComponents/Common";
import { useNavigate } from "react-router-dom";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/CurrRatePageStyles.css'

const initialFormData = {
    date: new Date().toISOString().split('T')[0],
    currency: '',
    rate: ''
};

function Forms({ options, ValidateForm, handleInputChange, formData }) {
    return (
        <Form noValidate className="form" id="form" onSubmit={ValidateForm}>
            <Row>
                <Col xl="2">
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input type="date" id="inputDate" name="Date" value={formData.date}
                        onChange={handleInputChange} />
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select id="inputCurrency" name="Currency" value={formData.currency}
                        onChange={handleInputChange} >
                        {options.currency.map((currency, index) => (
                            <option key={index} value={currency}>{currency}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputRate">
                        Rate
                    </Form.Label>
                    <Form.Control type="text" id="inputRate" name="Rate" autoComplete="off" value={formData.rate}
                        onChange={handleInputChange} />
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
    const [formData, setFormData] = useState(initialFormData);

    const navigate = useNavigate();

    useEffect(() => {
        document.title = "Currency Rates";
    }, []);

    useEffect(() => {
        // Fetch options
        GetOptions()
            .then(optionsData => {
                setOptions(optionsData);
            })
            .catch(error => {
                setError('Failed to load options: ' + error.message);
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
                console.error('Error loading plot:', error);
            });

    }, []);

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
                    navigate(data.redirect);
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
                    navigate(data.redirect);
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
                    navigate(data.redirect);
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

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        const key = name.replace('input', '');
        setFormData(prevData => ({
            ...prevData,
            [key.charAt(0).toLowerCase() + key.slice(1)]: value
        }));
    };

    const ValidateForm = (e) => {
        e.preventDefault();

        const { date, currency, rate } = formData;

        if (isNaN(rate) || rate <= 0) {
            alert("Please enter a valid rate.");
            return false;
        }

        const RequestData = {
            date: date,
            currency: currency,
            rate: rate
        }

        // Send POST request
        fetch("/api/add/currencyrates", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(RequestData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    setFormData(initialFormData)
                    GetHistory()
                        .then(historyData => {
                            setHistory(historyData);
                        })
                    GetPlot()
                        .then(url => {
                            setImageUrl(url);
                        })
                } else {
                    alert('Error: ' + (data.message || 'Failed to add currency rate'));
                }
            })
            .catch(error => {
                console.error('Unexpected error:', error);
                alert('Unexpected error occurred');
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
                    {options && (<Forms
                        options={options}
                        ValidateForm={ValidateForm}
                        handleInputChange={handleInputChange}
                        formData={formData}
                    />)}
                </div>
                <br />
                <div className="row">
                    <div className="col-md-4">
                        <h3>Currency Rates History</h3>
                        {history && (<HistoryTable
                            columns={["Date", "Currency", "Rate"]}
                            data={history}
                            tableId="CurrRateHistoryTable"
                            numberColumns={["2-4"]}
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
