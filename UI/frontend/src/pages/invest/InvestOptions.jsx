import { useEffect, useState } from "react";
import Header from "../../commonComponents/Header"
import { CheckLegacy } from '../../commonComponents/Common'
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import "../../assets/styles/InvestOptionsStyles.css"


export default function InvestOptionsPage() {
    const [stocks, setStocks] = useState([]);
    const [stockList, setStockList] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        document.title = "Invest Options";

        const isLegacyResult = !CheckLegacy();
        if (isLegacyResult) {
            setError("The current database is in legacy mode and does not support invest transactions.");
        } else {
            fetch('/api/spv/invest')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        setStocks(data.data.stocks);
                        setStockList(data.data.stocks.join('\n'));
                    }
                })
                .catch(() => {
                    setError("Failed to fetch invest options.");
                });
        }
    }, []);

    const submitInvestSPV = (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);
        const stockListUpdated = {
            stocks: formData.get("stock-values").split("\n").map(item => item.trim()).filter(item => item)
        }

        fetch('/api/spv/invest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(stockListUpdated),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.message || 'Failed to update stocks spv'));
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    const submitInvestPB = (e) => {
        e.preventDefault();

        const form = e.target;
        const formDataObj = new FormData(form);
        const formObject = Object.fromEntries(formDataObj.entries());
        const regex = /[!@#$%^&*()+={}[\]:;"'<>,.?/|\\]/;

        if (regex.test(formObject.InvestPB)) {
            alert("Invest PB name contains special characters!")
            return false;
        }

        if (formObject.Stock === "") {
            alert("Stock name cannot be empty!")
            return false;
        }

        fetch('/api/spv/ipb/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formObject),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.message || 'Failed to update IPB'));
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="invest-optionsPage">
                    <h1>Invest Options</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        )
    }

    return (
        <>
            <Header />
            <div className="invest-optionsPage container-fluid">
                <h1>Invest Options</h1>
                <div className="row">
                    <div className="col-md-12">
                        <Form noValidate id="invest-spv-form" onSubmit={submitInvestSPV}>
                            <Row>
                                <Col md={4}></Col>
                                <Col md={3}>
                                    <Form.Label htmlFor="stock-values" id="stock-label">Stock Values</Form.Label>
                                    <br />
                                    {stockList &&
                                        (<textarea value={stockList} onChange={(e) => setStockList(e.target.value)} id="stock-values" name="stock-values" rows="13" cols="20" autoComplete="off" />)}
                                </Col>
                            </Row>
                            <br />
                            <Row>
                                <Button variant="primary" type="submit" id="save-spv-btn">
                                    Save Changes
                                </Button>
                            </Row>
                        </Form>
                    </div>
                </div>
                <br />
                <hr />
                <br />
                <div className="row">
                    <Form noValidate onSubmit={submitInvestPB}>
                        <Row>
                            <Col md={3} xs={8}>
                                <h3>Add Invest PB</h3>
                            </Col>
                        </Row>
                        <Row>
                            <Col md={3}>
                                <Form.Label htmlFor="input-ipb">
                                    Invest PB name
                                </Form.Label>
                                <Form.Control type="text" id="input-ipb" name="InvestPB" autoComplete="off" />
                            </Col>
                            <Col md={2}>
                                <Form.Label htmlFor="input-stock">
                                    Stock name
                                </Form.Label>
                                <Form.Select type="text" id="input-stock" name="Stock">
                                    {stocks.map((stock, index) => (
                                        <option value={stock} key={index}>{stock}</option>
                                    ))}
                                </Form.Select>
                            </Col>
                        </Row>
                        <br />
                        <Row>
                            <Col md={3} xs={8}>
                                <Button variant="primary" type="submit" id="add-ipb-btn">
                                    Add Invest PB
                                </Button>
                            </Col>
                        </Row>
                    </Form>
                </div>
            </div>
        </>
    )
}