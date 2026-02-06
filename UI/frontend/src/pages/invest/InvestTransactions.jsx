import { useEffect, useState } from "react";
import Header from "../commonComponents/Header"
import { CheckLegacy } from '../commonComponents/Common'
import { HistoryTable } from "../../commonComponents/Common";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';

function Forms({ options }) {
    return (
        <Form noValidate className="invest-transaction-form" id="i-t-form" onSubmit={(e) => {
            e.preventDefault();
            const form = e.target;
            const formDataObj = new FormData(form);
            const formObject = Object.fromEntries(formDataObj.entries());

            if (formObject.date === '' || formObject.pb === '' || isNaN(formObject.amount) || formObject.currency === '' || formObject.ipb === '' || isNaN(formObject.stockAmount) || formObject.stock === '') {
                alert("All fields except fee are required!");
                return false;
            }

            if (formObject.stockAmount <= 0 || formObject.amount <= 0) {
                alert('Buy/sell amount must be greater than 0');
                return false;
            }
            if (formObject.fee === '') {
                formObject.fee = 0; // Default fee to 0 if not provided
            } else if (isNaN(formObject.fee)) {
                alert('Fee must be a valid number');
                return false;
            }
            else if (formObject.fee < 0) {
                alert('Fee must be greater than 0');
                return false;
            }

            if (formObject.type === 'buy') {
                formObject.amount = formObject.amount * -1; // Convert amount to negative for buy transactions
            } else if (formObject.type === 'sell') {
                formObject.stockAmount = formObject.stockAmount * -1; // Convert invest amount to negative for sell transactions
            }

            // Send POST request
            fetch(`/api/add/invest/transaction`, {
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
                    <Form.Label>Buy/Sell</Form.Label>
                </Col>
                <Col>
                    <Form.Select id="i-t-type" name="type" defaultValue={"buy"}>
                        <option value="buy">Buy</option>
                        <option value="sell">Sell</option>
                    </Form.Select>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Date</Form.Label>
                </Col>
                <Col>
                    <Form.Control type="date" id="i-t-date" name="date" defaultValue={new Date().toISOString().split('T')[0]} />
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Person-Bank</Form.Label>
                </Col>
                <Col>
                    <Form.Select id="i-t-person-bank" name="pb" defaultValue="">
                        <option value="" disabled></option>
                        {options.personBanks.map((pb, index) => (
                            <option key={index} value={pb.id}>{pb.name}</option>
                        ))}
                    </Form.Select>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Amount</Form.Label>
                </Col>
                <Col>
                    <Form.Control type="text" id="i-t-amount" name="amount" autoComplete="off" />
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Currency</Form.Label>
                </Col>
                <Col>
                    <Form.Select id="i-t-currency" name="currency" defaultValue="">
                        <option value="" disabled></option>
                        {options.currencies.map((currency, index) => (
                            <option key={index} value={currency.code}>{currency.code}</option>
                        ))}
                    </Form.Select>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Invest Person-Bank</Form.Label>
                </Col>
                <Col>
                    <Form.Select id="i-t-invest-person-bank" name="ipb" defaultValue="">
                        <option value="" disabled></option>
                        {options.investPersonBanks.map((ipb, index) => (
                            <option key={index} value={ipb.id}>{ipb.name}</option>
                        ))}
                    </Form.Select>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Stock amount</Form.Label>
                </Col>
                <Col>
                    <Form.Control type="text" id="i-t-stock-amount" name="stockAmount" autoComplete="off" />
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Stock</Form.Label>
                </Col>
                <Col>
                    <Form.Select id="i-t-stock" name="stock" defaultValue="">
                        <option value="" disabled></option>
                        {options.stocks.map((stock, index) => (
                            <option key={index} value={stock.id}>{stock.name} ({stock.symbol})</option>
                        ))}
                    </Form.Select>
                </Col>
            </Row>
            <Row className="mb-3">
                <Col>
                    <Form.Label>Fee</Form.Label>
                </Col>
                <Col>
                    <Form.Control type="text" id="i-t-fee" name="fee" autoComplete="off" />
                </Col>
            </Row>

            <Row><Col md={2}>
                <Button variant="primary" type="submit" id="i-t-submit">
                    Add Transaction
                </Button>
            </Col>
                <Col md={2}>
                    <OverlayTrigger
                        placement="right"
                        overlay={
                            <Tooltip id="tooltip-reflect-transaction">
                                If checked, the transaction will be reflected in the main balance. Otherwise, it will only affect the invest balance.
                            </Tooltip>
                        }
                    >
                        <Form.Check
                            type="checkbox"
                            id="i-t-isReflective"
                            name="isReflective"
                            label="Reflect transaction in main balance"
                            defaultChecked={true}
                        />
                    </OverlayTrigger>
                </Col>
            </Row>
        </Form>
    )
}

export default function InvestTransactionsPage() {
    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        document.title = "Invest Transactions";

        const isLegacyResult = CheckLegacy();
        if (isLegacyResult) {
            setError("The current database is in legacy mode and does not support invest transactions.");
            setLoading(false);
        } else {
            const InitApp = async () => {
                const promises = [
                    GetOptions(),
                    GetHistory()
                ];

                const results = await Promise.all(promises)

                setOptions(results[0]);
                setHistory(results[1])
                setLoading(false);
            }
            InitApp();
        }
    }, []);

    const GetOptions = () => {
        return fetch(`/api/get/options/invest-transaction`)
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
        return fetch(`/api/get/invest/history/transactions`)
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

    if (loading) {
        return (
            <>
                <Header />
                <div className="invest-transactionsPage container">
                    <h1>Invest Transactions</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="invest-transactionsPage container">
                    <h1>Invest Transactions</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="invest-transactionsPage container">
                <h1>Invest Transactions</h1>
                <div className="row">
                    <div className="col-md-5">
                        <h2>Add transaction</h2>
                        {options && (<Forms options={options} />)}
                    </div>
                    <div className="col-md-6">
                        <h2>Transactions history</h2>
                        {history && (<HistoryTable
                            columns={
                                ["ID", "Date", "Person-Bank", "Amount", "Currency",
                                    "Invest Person-Bank", "Stock amount", "Stock", "Fee", "Stock price"]}
                            data={history}
                            tableId="investTransactionsHistoryTable"
                            numberColumns={["3-2", "6-6", "8-2", "9-2"]}
                        />)}
                    </div>
                </div>
            </div>
        </>
    )
}