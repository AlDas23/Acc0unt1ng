import { useEffect, useState } from "react";
import { HistoryTableWithEdit } from "../commonComponents/Common";
import { useNavigate } from "react-router-dom";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/TransferPageStyles.css'

const initialFormDataSTD = {
    date: new Date().toISOString().split('T')[0],
    sender: '',
    receiver: '',
    sum: '',
    currency: '',
    comment: ''
};

const initialFormDataADV = {
    date: new Date().toISOString().split('T')[0],
    sender: '',
    sSum: '',
    sCurrency: '',
    receiver: '',
    rSum: '',
    rCurrency: '',
    currencyRate: '',
    comment: ''
};

function StandardTransferForm({ options, formData, handleInputChange, editMode, resetForm, ValidateForm }) {
    return (
        <Form noValidate className="form" id="formStandard" onSubmit={ValidateForm}
            style={editMode.isEditing && editMode.type === 'advanced' ? { display: 'none' } : null}
        >
            <Row>
                <Col xl="2">
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input
                        type="date"
                        id="inputDate"
                        name="Date"
                        value={formData.date}
                        onChange={handleInputChange}
                    />
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputSender">
                        Sender
                    </Form.Label>
                    <Form.Select
                        id="inputSender"
                        name="Sender"
                        value={formData.sender}
                        onChange={handleInputChange}
                    >
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
                    <Form.Select
                        id="inputReceiver"
                        name="Receiver"
                        value={formData.receiver}
                        onChange={handleInputChange}
                    >
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
                    <Form.Control
                        type="text"
                        id="inputSum"
                        name="Sum"
                        value={formData.sum}
                        onChange={handleInputChange}
                        autoComplete="off"
                    />
                </Col>
                <Col xl="1">
                    <Form.Label htmlFor="inputCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select
                        id="inputCurrency"
                        name="Currency"
                        value={formData.currency}
                        onChange={handleInputChange}
                    >
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
                    <Form.Control
                        type="text"
                        id="inputComment"
                        name="Comment"
                        value={formData.comment}
                        onChange={handleInputChange}
                        autoComplete="off"
                    />
                </Col>
            </Row>
            <Row>
                <Button type="submit" id="SubmitButtonStandard">
                    {editMode.isEditing && editMode.type === 'standard' ? "Update Record" : "Add Record"}
                </Button>
            </Row>
            <Row>
                {editMode.isEditing && editMode.type === 'standard' && (
                    <Button type="button" onClick={resetForm} id="CancelButtonStandard">
                        Cancel Edit
                    </Button>
                )}
            </Row>
        </Form>
    )
};

function AdvancedTransferForm({ options, formData, handleInputChange, editMode, resetForm, ValidateForm }) {
    return (
        <Form noValidate className="form" id="formAdvanced" onSubmit={ValidateForm}
            style={editMode.isEditing && editMode.type === 'standard' ? { display: 'none' } : null}
        >
            <Row className="adv1">
                <Col xl="2">
                    <Form.Label htmlFor="inputADVDate">
                        Date
                    </Form.Label>
                    <input
                        type="date"
                        id="inputADVDate"
                        name="ADVDate"
                        value={formData.date}
                        onChange={handleInputChange}
                    />
                </Col>
                <Col xl="auto">
                    <Form.Label htmlFor="inputADVSender">
                        Sender
                    </Form.Label>
                    <Form.Select
                        id="inputADVSender"
                        name="ADVSender"
                        value={formData.sender}
                        onChange={handleInputChange}
                    >
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
                    <Form.Control
                        type="text"
                        id="inputADVSSum"
                        name="SSum"
                        value={formData.sSum}
                        onChange={handleInputChange}
                        autoComplete="off"
                    />
                </Col>
                <Col xl="auto">
                    <Form.Label htmlFor="inputADVSCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select
                        id="inputADVSCurrency"
                        name="SCurrency"
                        value={formData.sCurrency}
                        onChange={handleInputChange}
                    >
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
                    <Form.Select
                        id="inputADVReceiver"
                        name="ADVReceiver"
                        value={formData.receiver}
                        onChange={handleInputChange}
                    >
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
                    <Form.Control
                        type="text"
                        id="inputADVRSum"
                        name="RSum"
                        value={formData.rSum}
                        onChange={handleInputChange}
                        autoComplete="off"
                    />
                </Col>
                <Col xl="auto">
                    <Form.Label htmlFor="inputADVRCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select
                        id="inputADVRCurrency"
                        name="RCurrency"
                        value={formData.rCurrency}
                        onChange={handleInputChange}
                    >
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
                    <Form.Control
                        type="text"
                        id="inputADVCurrencyRate"
                        name="CurrencyRate"
                        value={formData.currencyRate}
                        onChange={handleInputChange}
                        autoComplete="off"
                    />
                </Col>
                <Col xl="3">
                    <Form.Label htmlFor="inputADVComment">
                        Comment
                    </Form.Label>
                    <Form.Control
                        type="text"
                        id="inputADVComment"
                        name="ADVComment"
                        value={formData.comment}
                        onChange={handleInputChange}
                        autoComplete="off"
                    />
                </Col>
            </Row>
            <Row>
                <Button type="submit" id="SubmitButtonAdvanced">
                    {editMode.isEditing && editMode.type === 'advanced' ? "Update Record" : "Add Record"}
                </Button>
            </Row>
            <Row>
                {editMode.isEditing && editMode.type === 'advanced' && (
                    <Button type="button" onClick={resetForm} id="CancelButtonAdvanced">
                        Cancel Edit
                    </Button>
                )}
            </Row>
        </Form>
    )
};

function Forms({ options, formDataSTD, formDataADV, handleInputChangeSTD, handleInputChangeADV, editMode, resetForm, selectedTable, ValidateFormADV, ValidateFormSTD }) {
    return (
        <div className="forms">
            <div className="form-standard row">
                <div className="col-xl-12">
                    <h2 style={editMode.isEditing && selectedTable === 'advanced' ? { display: 'none' } : null}>Standard Transfer</h2>
                    <StandardTransferForm
                        options={options}
                        formData={formDataSTD}
                        handleInputChange={handleInputChangeSTD}
                        editMode={editMode}
                        resetForm={resetForm}
                        ValidateForm={ValidateFormSTD}
                    />
                </div>
            </div>
            <br />
            <div className="form-advanced row">
                <div className="col-xl-12">
                    <h2 style={editMode.isEditing && selectedTable === 'standard' ? { display: 'none' } : null}>Advanced Transfer</h2>
                    <AdvancedTransferForm
                        options={options}
                        formData={formDataADV}
                        handleInputChange={handleInputChangeADV}
                        editMode={editMode}
                        resetForm={resetForm}
                        ValidateForm={ValidateFormADV}
                    />
                </div>
            </div>
        </div>
    );
}


export default function TransferPage() {
    useEffect(() => {
        document.title = "Transfer Records";
    }, []);

    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [historyADV, setHistoryADV] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formDataSTD, setFormDataSTD] = useState(initialFormDataSTD);
    const [formDataADV, setFormDataADV] = useState(initialFormDataADV);
    const [editMode, setEditMode] = useState({ isEditing: false, id: null, type: null });
    const [selectedTable, setSelectedTable] = useState('standard');

    const navigate = useNavigate();

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

    const handleInputChangeSTD = (e) => {
        const { name, value } = e.target;
        const key = name.replace('input', '');
        setFormDataSTD(prevData => ({
            ...prevData,
            [key.charAt(0).toLowerCase() + key.slice(1)]: value
        }));
    };

    const handleInputChangeADV = (e) => {
        const { name, value } = e.target;
        let key;

        // Handle the special case for ADVComment
        if (name === 'ADVComment') {
            key = 'comment';
        } else {
            key = name.replace('input', '').replace('ADV', '');
        }

        setFormDataADV(prevData => ({
            ...prevData,
            [key.charAt(0).toLowerCase() + key.slice(1)]: value
        }));
    };

    const resetForm = () => {
        if (selectedTable === 'standard') {
            setFormDataSTD(initialFormDataSTD);
        } else {
            setFormDataADV(initialFormDataADV);
        }
        setEditMode({ isEditing: false, id: null, type: null });

        // Show all rows again
        const rows = document.querySelectorAll('.history-table tbody tr');
        rows.forEach(row => {
            row.style.display = '';
        });

        // Show both forms again
        const stdForm = document.querySelector('.form-standard');
        const advForm = document.querySelector('.form-advanced');
        if (stdForm) stdForm.style.display = '';
        if (advForm) advForm.style.display = '';
    }

    const EditRecord = (element) => {
        const row = element.target.parentNode;
        const cells = row.getElementsByTagName("td");
        const id = cells[0].innerText;

        const clickedRow = element.target.closest('tr');
        const rows = document.querySelectorAll('.history-table tbody tr');

        rows.forEach(row => {
            if (row !== clickedRow) {
                row.style.display = 'none';
            } else {
                row.style.display = ''; // Ensure the clicked row remains visible
            }
        });

        if (selectedTable === 'standard') {
            // Hide advanced forms
            const advForm = document.querySelector('.form-advanced');
            if (advForm) advForm.style.display = 'none';

            // Populate form fields with the data from the selected row
            setFormDataSTD({
                date: cells[1].innerText,
                sender: cells[2].innerText,
                receiver: cells[3].innerText,
                sum: Math.abs(parseFloat(cells[4].innerText)).toFixed(2),
                currency: cells[5].innerText,
                comment: cells[6].innerText
            });

            setEditMode({ isEditing: true, id: id, type: 'standard' });

        } else if (selectedTable === 'advanced') {
            // Hide standard form
            const stdForm = document.querySelector('.form-standard');
            if (stdForm) stdForm.style.display = 'none';

            // Populate form fields with the data from the selected row
            setFormDataADV({
                date: cells[1].innerText,
                sender: cells[2].innerText,
                sSum: Math.abs(parseFloat(cells[3].innerText)).toFixed(2),
                sCurrency: cells[4].innerText,
                receiver: cells[5].innerText,
                rSum: Math.abs(parseFloat(cells[6].innerText)).toFixed(2),
                rCurrency: cells[7].innerText,
                currencyRate: cells[8].innerText,
                comment: cells[9].innerText
            });

            setEditMode({ isEditing: true, id: id, type: 'advanced' });
        }
    }

    const GetOptions = () => {
        return fetch(`/api/get/options/transfer`)
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

    const GetHistory = (type) => {
        let endpoint;
        if (type === 'standard') {
            endpoint = `/api/get/history/transfer`
        } else if (type === 'advanced') {
            endpoint = `/api/get/history/transferADV`
        }
        return fetch(endpoint)
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

    const ValidateFormSTD = (e) => {
        e.preventDefault();
        const form = e.target;
        const formDataObj = new FormData(form);
        const formObject = Object.fromEntries(formDataObj.entries());

        // Validate form
        if (formObject.Date === "" || formObject.Sender === "" || formObject.Receiver === "" || formObject.Sum === "" || formObject.Currency === "") {
            alert("Please fill in all fields.");
            return false;
        }

        if (isNaN(parseFloat(formObject.Sum)) || parseFloat(formObject.Sum) <= 0) {
            alert("Please enter a valid sum.");
            return false;
        }

        if (formObject.Sender === formObject.Receiver) {
            alert("Sender and Receiver cannot be the same.");
            return false;
        }

        // Append transfer type to the formObject
        formObject.transferType = 'standard';

        let endpoint;
        if (editMode && editMode.isEditing && editMode.type === 'standard') {
            endpoint = `/api/edit/transfer/${editMode.id}`;
        } else {
            endpoint = `/api/add/transfer`;
        }

        // Send POST request
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formObject)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resetForm()
                    GetHistory("advanced")
                        .then(historyData => {
                            setHistory(historyData);
                        })
                } else {
                    alert('Error: ' + (data.message || 'Failed to add transfer'));
                }
            })
            .catch(error => {
                console.error('Unexpected error:', error);
                alert('Unexpected error occurred');
            });
    }

    const ValidateFormADV = (e) => {
        e.preventDefault();
        const form = e.target;
        const formDataObj = new FormData(form);
        const formObject = Object.fromEntries(formDataObj.entries());

        // Validate form
        if (formObject.ADVDate === "" || formObject.ADVSender === "" || formObject.ADVSSum === "" || formObject.ADVSCurrency === "" || formObject.ADVReceiver === "" || formObject.ADVRSum === "" || formObject.ADVRCurrency === "") {
            alert("Please fill in all fields.");
            return false;
        }

        if (isNaN(parseFloat(formObject.SSum)) || parseFloat(formObject.SSum) <= 0 || isNaN(parseFloat(formObject.RSum)) || parseFloat(formObject.RSum) <= 0) {
            alert("Please enter valid sums.");
            return false;
        }

        if (formObject.SCurrency === formObject.RCurrency) {
            alert("Sender and Receiver currencies cannot be the same. Use standard transfer instead.");
            return false;
        }

        if (parseFloat(formObject.ADVCurrencyRate) <= 0) {
            alert("Please enter a valid currency rate.");
            return false;
        }

        if (formObject.ADVSender === formObject.ADVReceiver) {
            alert("Sender and Receiver cannot be the same.");
            return false;
        }

        // Append transfer type to the formObject
        formObject.transferType = 'advanced';

        let endpoint;
        if (editMode && editMode.isEditing && editMode.type === 'advanced') {
            endpoint = `/api/edit/transfer/${editMode.id}`;
        } else {
            endpoint = `/api/add/transfer`;
        }

        // Send POST request
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formObject)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resetForm()
                    GetHistory("standard")
                        .then(historyData => {
                            setHistoryADV(historyData);
                        })
                } else {
                    alert('Error: ' + (data.message || 'Failed to add transfer'));
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
                    {options && (<Forms
                        options={options}
                        formDataSTD={formDataSTD}
                        formDataADV={formDataADV}
                        handleInputChangeSTD={handleInputChangeSTD}
                        handleInputChangeADV={handleInputChangeADV}
                        editMode={editMode}
                        resetForm={resetForm}
                        selectedTable={selectedTable}
                        ValidateFormSTD={ValidateFormSTD}
                        ValidateFormADV={ValidateFormADV}
                    />)}
                    <br />
                </div>
                <br />
                <div className="row">
                    <h3>History</h3>
                </div>
                <br />
                <div className="row">
                    <div className="col-md-2">
                        <p
                            id="stdTitle"
                            onClick={() => {
                                setSelectedTable('standard');
                                // Reset form when switching tables during edit mode
                                if (editMode.isEditing) {
                                    resetForm();
                                }
                            }}
                            className={selectedTable === 'standard' ? 'selectedTable' : ''}>
                            Standard Transfers
                        </p>
                    </div>
                    <div className="col-md-2">
                        <p
                            id="advTitle"
                            onClick={() => {
                                setSelectedTable('advanced');
                                // Reset form when switching tables during edit mode
                                if (editMode.isEditing) {
                                    resetForm();
                                }
                            }}
                            className={selectedTable === 'advanced' ? 'selectedTable' : ''}>
                            Advanced Transfers
                        </p>
                    </div>
                </div>
                <br />
                <div className="row">
                    <div className="col-md-12">
                        {selectedTable === 'standard' && history && (<HistoryTableWithEdit
                            columns={["ID", "Date", "Sender", "Receiver", "Sum", "Currency", "Comment"]}
                            data={history}
                            EditRecord={EditRecord}
                            tableId={"StandardTransferTable"}
                            numberColumns={["4-2"]}
                        />)}
                        {selectedTable === 'advanced' && historyADV && (<HistoryTableWithEdit
                            columns={["ID", "Date", "Sender", "Sum", "Currency", "Receiver", "Sum", "Currency", "Currency Rate", "Comment"]}
                            data={historyADV}
                            EditRecord={EditRecord}
                            tableId={"AdvancedTransferTable"}
                            numberColumns={["3-2", "6-2", "8-4"]}
                        />)}
                    </div>
                </div>
            </div>
        </>
    )
}
