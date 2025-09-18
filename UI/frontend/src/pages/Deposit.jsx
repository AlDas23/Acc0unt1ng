import { useEffect, useState } from "react";
import { HistoryTable } from "../commonComponents/Common";
import { useNavigate } from "react-router-dom";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/DepositPageStyles.css'

const initialFormData = {
    dateIn: new Date().toISOString().split('T')[0],
    name: '',
    owner: '',
    sum: '',
    currency: '',
    months: '',
    dateOut: '',
    percent: '',
    crencyRate: '',
    comment: ''
};


function Forms({ options, ValidateForm, handleInputChange, formData }) {
    return (
        <Form noValidate className="form" id="form" onSubmit={ValidateForm}>
            <Row>
                <Col>
                    <Form.Label htmlFor="inputDateIn">
                        Deposit Date
                    </Form.Label>
                    <input type="date" id="inputDateIn" name="DateIn" className="datePicker" value={formData.dateIn}
                        onChange={handleInputChange} />
                </Col>
                <Col>
                    <Form.Label htmlFor="inputName">
                        Deposit Name
                    </Form.Label>
                    <Form.Control type="text" id="inputName" name="Name" autoComplete="off" value={formData.name}
                        onChange={handleInputChange} />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputOwner">
                        Person-bank
                    </Form.Label>
                    <Form.Select id="inputOwner" name="Owner" value={formData.owner}
                        onChange={handleInputChange}>
                        <option value="" disabled></option>
                        {options.pb.map((pb, index) => (
                            <option value={pb} key={index}>{pb}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col >
                    <Form.Label htmlFor="inpuSum">
                        Sum
                    </Form.Label>
                    <Form.Control type="text" id="inpuSum" name="Sum" autoComplete="off" value={formData.sum}
                        onChange={handleInputChange} />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select id="inputCurrency" name="Currency" value={formData.currency}
                        onChange={handleInputChange}>
                        <option value="" disabled></option>
                        {options.currencies.map((currencies, index) => (
                            <option value={currencies} key={index}>{currencies}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col >
                    <Form.Label htmlFor="inputMonths">
                        Months
                    </Form.Label>
                    <Form.Control type="text" id="inputMonths" name="Months" autoComplete="off" value={formData.months}
                        onChange={handleInputChange} />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputDateOut">
                        Closing Date
                    </Form.Label>
                    <input type="date" id="inputDateOut" name="DateOut" className="datePicker" value={formData.dateOut}
                        onChange={handleInputChange} />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputPercent">
                        %
                    </Form.Label>
                    <Form.Control type="text" id="inputPercent" name="Percent" autoComplete="off" value={formData.Percent}
                        onChange={handleInputChange} />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputCurrencyRate">
                        Currency Rate
                    </Form.Label>
                    <Form.Control type="text" id="inputCurrencyRate" name="CurrencyRate" autoComplete="off" value={formData.currencyRate}
                        onChange={handleInputChange} />
                </Col>
                <Col>
                    <Form.Label htmlFor="inputComment">
                        Comment
                    </Form.Label>
                    <Form.Control type="text" id="inputComment" name="Comment" autoComplete="off" value={formData.comment}
                        onChange={handleInputChange} />
                </Col>

            </Row>
            <Row>
                <Button type="submit" id="SubmitButton">Submit record</Button>
            </Row>
        </Form>
    );
}

export default function DepositPage() {
    const [options, setOptions] = useState(null);
    const [historyO, setHistoryO] = useState(null);
    const [historyC, setHistoryC] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState(initialFormData);

    const navigate = useNavigate();

    useEffect(() => {
        document.title = "Deposit Records";
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
        GetHistory(true)
            .then(historyData => {
                setHistoryO(historyData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load history: ' + error.message);
                setLoading(false);
                console.error('Error loading history:', error);
            });
        GetHistory(false)
            .then(historyData => {
                setHistoryC(historyData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load history: ' + error.message);
                setLoading(false);
                console.error('Error loading history:', error);
            });
    }, []);

    const GetOptions = () => {
        return fetch(`/api/get/options/deposit`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    return data.options;
                } else if (data.redirect) {
                    alert('Database is missng or corrupted. You will be redirected to the setup page.');
                    navigate(data.redirect);
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

    const GetHistory = (isActive) => {
        if (isActive) {
            return fetch(`/api/get/history/depositO`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        return data.history;
                    } else if (data.redirect) {
                        alert('Database is missng or corrupted. You will be redirected to the setup page.');
                        navigate(data.redirect);
                    } else {
                        throw new Error(data.message || 'Failed to load history');
                    }
                })
                .catch(error => {
                    console.error('Error fetching history:', error);
                    alert('Unexpected error occurred while fetching history: ' + error.message);
                    throw error;
                });
        } else {
            return fetch(`/api/get/history/depositC`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        return data.history;
                    } else if (data.redirect) {
                        alert('Database is missng or corrupted. You will be redirected to the setup page.');
                        navigate(data.redirect);
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

        const { dateIn, name, owner, sum, currency, months, dateOut, percent, currencyRate, comment } = formData;

        if (!dateIn || !name || !owner || isNaN(sum) || !currency || !dateOut) {
            alert("Please fill in all reqired fields.\n Deposit date, name, owner, sum, currency, percent are required.");
            return false;
        }

        if (isNaN(sum) || sum <= 0) {
            alert("Please enter a valid sum.");
            return false;
        }

        if (!months && (isNaN(months) || months <= 0)) {
            alert("Please enter a valid number of months.");
            return false;
        }

        if (isNaN(percent) || percent < 0 || percent > 100) {
            alert("Please enter a valid percent.");
            return false;
        }

        if (currencyRate && (isNaN(currencyRate) || currencyRate <= 0)) {
            alert("Please enter a valid currency rate.");
            return false;
        }

        const RequestData = {
            dateIn: dateIn,
            name: name,
            owner: owner,
            sum: sum,
            currency: currency,
            months: months,
            dateOut: dateOut,
            percent: percent,
            currencyRate: currencyRate,
            comment: comment
        }

        // Send POST request
        fetch(`/api/add/deposit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(RequestData)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    setFormData(initialFormData)
                    GetHistory(true)
                        .then(historyData => {
                            setHistoryO(historyData);
                        })
                    GetHistory(false)
                        .then(historyData => {
                            setHistoryC(historyData);
                        })
                } else {
                    alert('Error: ' + (data.message || 'Failed to add deposit'));
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
                <div className="deposit-page">
                    <h1>Deposit Records</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="deposit-page">
                    <h1>Deposit Records</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="deposit-page container">
                <h1>Deposit Records</h1>
                {options && (<Forms
                    options={options}
                    ValidateForm={ValidateForm}
                    handleInputChange={handleInputChange}
                    formData={formData}
                />)}
                <br />
                <div className="row">
                    <div className="col xl-12">
                        <h3>Active deposits</h3>
                        {historyO && (<HistoryTable
                            columns={["Deposit Date", "Name", "Person-bank", "Sum", "Currency", "Months", "Closing Date", "%", "Currency rate", "Expected amount", "Comment"]}
                            data={historyO}
                            tableId="openDepositsTable"
                            numberColumns={["3-2", "7-1", "8-4", "9-2"]}
                        />)}
                    </div>
                </div>
                <br />
                <div className="row">
                    <div className="col xl-12">
                        <h3>Closed deposits</h3>
                        {historyC && (<HistoryTable
                            columns={["Deposit Date", "Name", "Person-bank", "Sum", "Currency", "Months", "Closing Date", "%", "Currency rate", "Expected amount", "Comment"]}
                            data={historyC}
                            tableId="closedDepositsTable"
                            numberColumns={["3-2", "7-1", "8-4", "9-2"]}
                        />)}
                    </div>
                </div>
            </div>
        </>
    )

}
