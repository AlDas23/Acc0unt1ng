import { useEffect, useState } from "react";
import { HistoryTableWithEdit, DatePicker } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/TransferPageStyles.css'


export default function TransferPage() {
    useEffect(() => {
        document.title = "Transfer Records";
    }, []);

    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [historyADV, setHistoryADV] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editMode, setEditMode] = useState({ isEditing: false, id: null, type: null });
    const [selectedTable, setSelectedTable] = useState('standard')
    const [formData, setFormData] = useState({
        date: "",
        sender: "",
        receiver: "",
        sum: "",
        currency: "",
        comment: "",
        // for advanced form:
        rSum: "",
        rCurrency: "",
        currencyRate: ""
    });

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
        GetHistory('standard')
            .then(historyData => {
                setHistory(historyData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load history: ' + error.message);
                setLoading(false);
                console.error('Error loading history:', error);
            });
        GetHistory('advanced')
            .then(historyData => {
                setHistoryADV(historyData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load advanced history: ' + error.message);
                setLoading(false);
                console.error('Error loading advanced history:', error);
            });
    }, []);

    const ValidateForm = (event, Edit = false, id = null) => {
        let FormObject;
        let formData = new FormData(event);
        let endpoint;

        FormObject = Object.fromEntries(formData.entries());

        if (selectedTable === 'standard') {
            if (FormObject.inputDate === "" || FormObject.inputSender === "" || FormObject.inputReceiver === "" || FormObject.inputSum === "" || FormObject.inputCurrency === "") {
                alert("Please fill in all fields.");
                return false;
            }

            if (isNaN(parseFloat(FormObject.inputSum)) || parseFloat(FormObject.inputSum) <= 0) {
                alert("Please enter a valid sum.");
                return false;
            }

        } else if (selectedTable === 'advanced') {
            if (FormObject.inputDate === "" || FormObject.inputSender === "" || FormObject.inputSSum === "" || FormObject.inputSCurrency === "" || FormObject.inputReceiver === "" || FormObject.inputRSum === "" || FormObject.inputRCurrency === "") {
                alert("Please fill in all fields.");
                return false;
            }

            if (isNaN(parseFloat(FormObject.inputSSum)) || parseFloat(FormObject.inputSSum) <= 0 || isNaN(parseFloat(FormObject.inputRSum)) || parseFloat(FormObject.inputRSum) <= 0) {
                alert("Please enter valid sums.");
                return false;
            }

            if (FormObject.inputSCurrency === FormObject.inputRCurrency) {
                alert("Sender and Receiver currencies cannot be the same. Use standard transfer instead.");
                return false;
            }

            if (parseFloat(FormObject.inputCurrencyRate) <= 0) {
                alert("Please enter a valid currency rate.");
                return false;
            }
        }

        if (FormObject.inputSender === FormObject.inputReceiver) {
            alert("Sender and Receiver cannot be the same.");
            return false;
        }

        // Append transfer type to the FormObject
        FormObject.transferType = selectedTable;

        if (!Edit) {
            endpoint = 'http://localhost:5050/api/add/transfer';
        } else {
            endpoint = 'http://localhost:5050/api/edit/transfer/' + id;
        }

        // Send POST request
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(FormObject)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.message || 'Failed to add transfer'));
                }
            })
            .catch(error => {
                console.error('Unexpected error:', error);
                alert('Unexpected error occurred');
            });
    }


    const EditRecord = (element) => { // TODO: Find a way to correctly populate forms with edit records data
        const row = element.target.parentNode;
        const cells = row.getElementsByTagName("td");
        const id = cells[0].innerText;

        setEditMode({ isEditing: true, id, selectedTable });

        if (selectedTable === 'standard') {
            const clickedRow = element.target.closest('tr');
            const rows = document.querySelectorAll('.history-table tbody tr');

            rows.forEach(row => {
                if (row !== clickedRow) {
                    row.style.display = 'none';
                } else {
                    row.style.display = ''; // Ensure the clicked row remains visible
                }
            });

            // Hide advanced forms
            const advForm = document.querySelector('.form-advanced');
            advForm.style.display = 'none';

            // Populate form fields with the data from the selected row
            setFormData({
                date: cells[1].innerText,
                sender: cells[2].innerText,
                receiver: cells[3].innerText,
                sum: parseFloat(cells[4].innerText).toFixed(2),
                currency: cells[5].innerText,
                comment: cells[6].innerText
            });

            const submitButton = document.getElementById("SubmitButtonStandard");
            submitButton.innerText = "Edit";

        } else if (selectedTable === 'advanced') {
            const clickedRow = element.target.closest('tr');
            const rows = document.querySelectorAll('.history-table tbody tr');

            rows.forEach(row => {
                if (row !== clickedRow) {
                    row.style.display = 'none';
                } else {
                    row.style.display = ''; // Ensure the clicked row remains visible
                }
            });

            // Hide standard form
            const stdForm = document.querySelector('.form-standard');
            stdForm.style.display = 'none';

            // Populate form fields with the data from the selected row
            document.getElementById("inputADVDate").value = cells[1].innerText;
            document.getElementById("inputADVSender").value = cells[2].innerText;
            document.getElementById("inputADVSSum").value = parseFloat(cells[3].innerText).toFixed(2);
            document.getElementById("inputADVSCurrency").value = cells[4].innerText;
            document.getElementById("inputADVReceiver").value = cells[5].innerText;
            document.getElementById("inputADVRSum").value = parseFloat(cells[6].innerText).toFixed(2);
            document.getElementById("inputADVRCurrency").value = cells[7].innerText;
            document.getElementById("inputADVCurrencyRate").value = cells[8].innerText;
            document.getElementById("inputADVComment").value = cells[9].innerText;

            const submitButton = document.getElementById("SubmitButtonAdvanced");
            submitButton.innerText = "Edit";
        }
    }

    const GetOptions = () => {
        return fetch('http://localhost:5050/api/get/options/transfer')
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

    const GetHistory = (type) => {
        let endpoint;
        if (type === 'standard') {
            endpoint = 'http://localhost:5050/api/get/history/transfer'
        } else if (type === 'advanced') {
            endpoint = 'http://localhost:5050/api/get/history/transferADV'
        }
        return fetch(endpoint)
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

    const StandardTransferForm = ({ options, editMode }) => {
        return (
            <Form noValidate className="form" id="formStandard" onSubmit={(e) => {
                e.preventDefault();
                if (editMode.isEditing && editMode.type === 'standard') {
                    ValidateForm(e, true, editMode.id);
                } else {
                    ValidateForm(e);
                }
            }}
                style={editMode.isEditing && selectedTable === 'advanced' ? { display: 'none' } : null}
            >
                <Row>
                    <Col xl="2">
                        <Form.Label htmlFor="inputDate">
                            Date
                        </Form.Label>
                        <DatePicker id="inputDate" name="Date" value={formData.date} />
                    </Col>
                    <Col xl="2">
                        <Form.Label htmlFor="inputSender">
                            Sender
                        </Form.Label>
                        <Form.Select id="inputSender" name="Sender" defaultValue={""} value={formData.sender}>
                            <option value="" disabled></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </Form.Select>
                    </Col>
                    <Col xl="2">
                        <Form.Label htmlFor="inputReceiver">
                            Receiver
                        </Form.Label>
                        <Form.Select id="inputReceiver" name="Receiver" defaultValue={""} value={formData.receiver}>
                            <option value="" disabled></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </Form.Select>
                    </Col>
                    <Col xl="1">
                        <Form.Label htmlFor="inputSum">
                            Sum
                        </Form.Label>
                        <Form.Control type="text" id="inputSum" name="Sum" value={formData.sum} />
                    </Col>
                    <Col xl="1">
                        <Form.Label htmlFor="inputCurrency">
                            Currency
                        </Form.Label>
                        <Form.Select id="inputCurrency" name="Currency" defaultValue={""} value={formData.currency}>
                            <option value="" disabled></option>
                            {options.currency.map((currency, index) => (
                                <option value={currency} key={index}>{currency}</option>
                            ))}
                        </Form.Select>
                    </Col>
                    <Col xl="auto">
                        <Form.Label htmlFor="inputComment">
                            Comment
                        </Form.Label>
                        <Form.Control type="text" id="inputComment" name="Comment" value={formData.comment} />
                    </Col>
                </Row>
                <Row>
                    <Button type="submit" id="SubmitButtonStandard">Add Record</Button>
                </Row>
            </Form>
        )
    };

    const AdvancedTransferForm = ({ options, editMode }) => {
        return (
            <Form noValidate className="form" id="formAdvanced" onSubmit={(e) => {
                e.preventDefault();
                if (editMode.isEditing && editMode.type === 'advanced') {
                    ValidateForm(e, true, editMode.id);
                } else {
                    ValidateForm(e);
                }
            }}
                style={editMode.isEditing && selectedTable === 'standard' ? { display: 'none' } : null}
            >
                <Row className="adv1">
                    <Col xl="2">
                        <Form.Label htmlFor="inputADVDate">
                            Date
                        </Form.Label>
                        <DatePicker id="inputADVDate" name="Date" />
                    </Col>
                    <Col xl="auto">
                        <Form.Label htmlFor="inputADVSender">
                            Sender
                        </Form.Label>
                        <Form.Select id="inputADVSender" name="Sender" defaultValue={""}>
                            <option value="" disabled></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </Form.Select>
                    </Col>
                    <Col xl="auto">
                        <Form.Label htmlFor="inputADVSSum">
                            Sum
                        </Form.Label>
                        <Form.Control type="text" id="inputADVSSum" name="SSum" />
                    </Col>
                    <Col xl="auto">
                        <Form.Label htmlFor="inputADVSCurrency">
                            Currency
                        </Form.Label>
                        <Form.Select id="inputADVSCurrency" name="SCurrency" defaultValue={""}>
                            <option value="" disabled></option>
                            {options.currency.map((currency, index) => (
                                <option value={currency} key={index}>{currency}</option>
                            ))}
                        </Form.Select>
                    </Col>
                </Row>
                <Row className="adv2">
                    <Col xl="auto">
                        <Form.Label htmlFor="inputADVReceiver">
                            Receiver
                        </Form.Label>
                        <Form.Select id="inputADVReceiver" name="Receiver" defaultValue={""}>
                            <option value="" disabled></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </Form.Select>
                    </Col>
                    <Col xl="auto">
                        <Form.Label htmlFor="inputADVRSum">
                            Sum
                        </Form.Label>
                        <Form.Control type="text" id="inputADVRSum" name="RSum" />
                    </Col>
                    <Col xl="auto">
                        <Form.Label htmlFor="inputADVRCurrency">
                            Currency
                        </Form.Label>
                        <Form.Select id="inputADVRCurrency" name="RCurrency" defaultValue={""}>
                            <option value="" disabled></option>
                            {options.currency.map((currency, index) => (
                                <option value={currency} key={index}>{currency}</option>
                            ))}
                        </Form.Select>
                    </Col>
                </Row>
                <Row className="adv3">
                    <Col xl="2">
                        <Form.Label htmlFor="inputADVCurrencyRate">
                            Currency Rate
                        </Form.Label>
                        <Form.Control type="text" id="inputADVCurrencyRate" name="Currency rate" />
                    </Col>
                    <Col xl="3">
                        <Form.Label htmlFor="inputADVComment">
                            Comment
                        </Form.Label>
                        <Form.Control type="text" id="inputADVComment" name="Comment" />
                    </Col>
                </Row>
                <Row>
                    <Button type="submit" id="SubmitButtonAdvanced">Add Record</Button>
                </Row>
            </Form>
        )
    };

    const Forms = ({ options, editMode }) => {
        return (
            <div className="forms">
                <div className="form-standard row">
                    <div className="col-xl-12">
                        <h2 style={editMode.isEditing && selectedTable === 'advanced' ? { display: 'none' } : null}>Standard Transfer</h2>
                        <StandardTransferForm options={options} editMode={editMode} />
                    </div>
                </div>
                <br />
                <div className="form-advanced row">
                    <div className="col-xl-12">
                        <h2 style={editMode.isEditing && selectedTable === 'standard' ? { display: 'none' } : null}>Advanced Transfer</h2>
                        <AdvancedTransferForm options={options} editMode={editMode} />
                    </div>
                </div>
            </div>
        );
    }


    if (loading) {
        return (
            <>
                <Header />
                <div className="transfer-page">
                    <h1>Transfer Records</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="transfer-page">
                    <h1>Transfer Records</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="transfer-page container">
                <h1>Transfer Records</h1>
                <br />
                <div className="row">
                    {options && (<Forms options={options} editMode={editMode} />)}
                    <br />
                </div>
                <br />
                <div className="row">
                    <h3>History</h3>
                </div>
                <br />
                <div className="row">
                    <div className="col-xl-2">
                        <p
                            id="stdTitle"
                            onClick={() => setSelectedTable('standard')}
                            className={selectedTable === 'standard' ? 'selectedTable' : ''}>
                            Standard Transfers
                        </p>
                    </div>
                    <div className="col-xl-2">
                        <p
                            id="advTitle"
                            onClick={() => setSelectedTable('advanced')}
                            className={selectedTable === 'advanced' ? 'selectedTable' : ''}>
                            Advanced Transfers
                        </p>
                    </div>
                </div>
                <br />
                <div className="row">
                    <div className="col-xl-12">
                        {selectedTable === 'standard' && history && (<HistoryTableWithEdit
                            columns={["ID", "Date", "Sender", "Receiver", "Sum", "Currency", "Comment"]}
                            data={history}
                            EditRecord={EditRecord}
                            tableId={"StandardTransferTable"}
                        />)}
                        {selectedTable === 'advanced' && historyADV && (<HistoryTableWithEdit
                            columns={["ID", "Date", "Sender", "Sum", "Currency", "Receiver", "Sum", "Currency", "Currency Rate", "Comment"]}
                            data={historyADV}
                            EditRecord={EditRecord}
                            tableId={"AdvancedTransferTable"}
                        />)}
                    </div>
                </div>
            </div>
        </>
    )
}
