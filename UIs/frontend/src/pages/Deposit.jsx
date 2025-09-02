import { useEffect, useState } from "react";
import { HistoryTable } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/DepositPageStyles.css'




function Forms({ options }) {
    return (
        <Form noValidate className="form" id="form" onSubmit={(e) => {
            e.preventDefault();
            const form = e.target;
            const formDataObj = new FormData(form);
            const formObject = Object.fromEntries(formDataObj.entries());

            if (!formObject.DateIn || !formObject.Name || !formObject.Owner || isNaN(formObject.Sum) || !formObject.Currency || !formObject.DateOut) {
                alert("Please fill in all reqired fields.\n Deposit date, name, owner, sum, currency, percent are required.");
                return false;
            }

            if (isNaN(formObject.Sum) || formObject.Sum <= 0) {
                alert("Please enter a valid sum.");
                return false;
            }

            if (!formObject.Months && (isNaN(formObject.Months) || formObject.Months <= 0)) {
                alert("Please enter a valid number of months.");
                return false;
            }

            if (isNaN(formObject.Percent) || formObject.Percent < 0 || formObject.Percent > 100) {
                alert("Please enter a valid percent.");
                return false;
            }

            if (formObject.CurrencyRate && (isNaN(formObject.CurrencyRate) || formObject.CurrencyRate <= 0)) {
                alert("Please enter a valid currency rate.");
                return false;
            }

            // Send POST request
            fetch('http://localhost:5050/api/add/deposit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formObject)
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
                        alert('Error: ' + (data.message || 'Failed to add deposit'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}>
            <Row>
                <Col>
                    <Form.Label htmlFor="inputDateIn">
                        Deposit Date
                    </Form.Label>
                    <input type="date" id="inputDateIn" name="DateIn" defaultValue={new Date().toISOString().split('T')[0]} className="datePicker" />
                </Col>
                <Col>
                    <Form.Label htmlFor="inputName">
                        Deposit Name
                    </Form.Label>
                    <Form.Control type="text" id="inputName" name="Name" autoComplete="off" />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputOwner">
                        Person-bank
                    </Form.Label>
                    <Form.Select id="inputOwner" name="Owner" defaultValue={""}>
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
                    <Form.Control type="text" id="inpuSum" name="Sum" autoComplete="off" />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select id="inputCurrency" name="Currency" defaultValue={""}>
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
                    <Form.Control type="text" id="inputMonths" name="Months" autoComplete="off" />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputDateOut">
                        Closing Date
                    </Form.Label>
                    <input type="date" id="inputDateOut" name="DateOut" className="datePicker" />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputPercent">
                        %
                    </Form.Label>
                    <Form.Control type="text" id="inputPercent" name="Percent" autoComplete="off" />
                </Col>
                <Col >
                    <Form.Label htmlFor="inputCurrencyRate">
                        Currency Rate
                    </Form.Label>
                    <Form.Control type="text" id="inputCurrencyRate" name="CurrencyRate" autoComplete="off" />
                </Col>
                <Col>
                    <Form.Label htmlFor="inputComment">
                        Comment
                    </Form.Label>
                    <Form.Control type="text" id="inputComment" name="Comment" autoComplete="off" />
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
        return fetch('http://localhost:5050/api/get/options/deposit')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
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

    const GetHistory = (isActive) => {
        if (isActive) {
            return fetch('http://localhost:5050/api/get/history/depositO')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
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
        } else {
            return fetch('http://localhost:5050/api/get/history/depositC')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
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
                {options && (<Forms options={options} />)}
                <br />
                <div className="row">
                    <div className="col xl-12">
                        <h3>Active deposits</h3>
                        {historyO && (<HistoryTable
                            columns={["Deposit Date", "Name", "Person-bank", "Sum", "Currency", "Months", "Closing Date", "%", "Currency rate", "Expected amount", "Comment"]}
                            data={historyO}
                            tableId="openDepositsTable"
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
                        />)}
                    </div>
                </div>
            </div>
        </>
    )

}
