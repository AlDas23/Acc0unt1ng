import { useEffect, useState } from "react";
import { HistoryTableWithEdit, YearSelectorOnChange } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
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

function StandardTransferForm({ options, formData, handleInputChange, editMode, resetForm }) {
    return (
        <Form noValidate className="form" id="formStandard" onSubmit={(e) => {
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
                        window.location.reload();
                    } else {
                        alert('Error: ' + (data.message || 'Failed to add transfer'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}
            style={editMode.isEditing && editMode.type === 'advanced' ? { display: 'none' } : null}
        >
            <Row>
                <Col md={2}>
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input
                        type="date"
                        id="TransferStdInputDate"
                        name="Date"
                        value={formData.date}
                        onChange={handleInputChange}
                    />
                </Col>
                <Col md={2}>
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
                <Col md={2}>
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
                <Col md={2}>
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
                <Col md={1}>
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
                <Col md={3}>
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
                <Col xs={4} md={2}>
                    <Button type="submit" id="SubmitButtonStandard">
                        {editMode.isEditing && editMode.type === 'standard' ? "Update Record" : "Add Record"}
                    </Button>
                </Col>
                <Col xs={4} md={2}>
                    {editMode.isEditing && editMode.type === 'standard' && (
                        <Button type="button" onClick={resetForm} id="CancelButtonStandard">
                            Cancel Edit
                        </Button>
                    )}
                </Col>
            </Row>
        </Form>
    )
};

function AdvancedTransferForm({ options, formData, handleInputChange, editMode, resetForm }) {
    return (
        <Form noValidate className="form" id="formAdvanced" onSubmit={(e) => {
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

            if ((formObject.ADVSender === formObject.ADVReceiver) && (formObject.SCurrency === formObject.RCurrency)) {
                alert("Sender and Receiver with same currency is prohibited.");
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
                        window.location.reload();
                    } else {
                        alert('Error: ' + (data.message || 'Failed to add transfer'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}
            style={editMode.isEditing && editMode.type === 'standard' ? { display: 'none' } : null}
        >
            <Row>
                <Col md={2}>
                    <Form.Label htmlFor="inputADVDate">
                        Date
                    </Form.Label>
                    <input
                        type="date"
                        id="TransferAdvInputDate"
                        name="ADVDate"
                        value={formData.date}
                        onChange={handleInputChange}
                    />
                </Col>
                <Col md={2}>
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
                <Col md={1}>
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
                <Col md={1}>
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
            <Row>
                <Col md={2}>

                </Col>
                <Col md={2}>
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
                <Col md={1}>
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
                <Col md={1}>
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
            <Row>
                <Col md={2}>
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
                <Col md={4}>
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
                <Col xs={4} md={2}>
                    <Button type="submit" id="SubmitButtonAdvanced">
                        {editMode.isEditing && editMode.type === 'advanced' ? "Update Record" : "Add Record"}
                    </Button>
                </Col>
                <br />
                <Col xs={4} md={2}>
                    {editMode.isEditing && editMode.type === 'advanced' && (
                        <Button type="button" onClick={resetForm} id="CancelButtonAdvanced">
                            Cancel Edit
                        </Button>
                    )}
                </Col>
            </Row>
        </Form>
    )
};

function Forms({ options, formDataSTD, formDataADV, handleInputChangeSTD, handleInputChangeADV, editMode, resetForm, selectedTable }) {
    return (
        <Container>
            <Row className="form-standard">
                <Col>
                    <h2 style={editMode.isEditing && selectedTable === 'advanced' ? { display: 'none' } : null}>Standard Transfer</h2>
                    <StandardTransferForm
                        options={options}
                        formData={formDataSTD}
                        handleInputChange={handleInputChangeSTD}
                        editMode={editMode}
                        resetForm={resetForm}
                    />
                </Col>
            </Row>
            <br />
            <Row className="form-advanced">
                <Col>
                    <h2 style={editMode.isEditing && selectedTable === 'standard' ? { display: 'none' } : null}>Cross-currency Transfer</h2>
                    <AdvancedTransferForm
                        options={options}
                        formData={formDataADV}
                        handleInputChange={handleInputChangeADV}
                        editMode={editMode}
                        resetForm={resetForm}
                    />
                </Col>
            </Row>
        </Container>
    );
}


export default function TransferPage() {
    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [historyADV, setHistoryADV] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formDataSTD, setFormDataSTD] = useState(initialFormDataSTD);
    const [formDataADV, setFormDataADV] = useState(initialFormDataADV);
    const [editMode, setEditMode] = useState({ isEditing: false, id: null, type: null });
    const [selectedTable, setSelectedTable] = useState('standard');
    const [yearsList, setYearsList] = useState([]);
    const [selectedYear, setSelectedYear] = useState(null);


    useEffect(() => {
        document.title = "Transfer Records";

        // Fetch options
        GetOptions()
            .then(optionsData => {
                setOptions(optionsData);
            })
            .catch(error => {
                setError('Failed to load options: ' + error.message);
                console.error('Error loading options:', error);
            });

        // Fetch years list
        GetYearsList()
            .then(yearsData => {
                setYearsList(yearsData);
                setSelectedYear(yearsData[0]);
            })
            .catch(error => {
                setError('Failed to load years list: ' + error.message);
                console.error('Error loading years list:', error);
            });
    }, []);

    useEffect(() => {
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
    }, [selectedYear]);

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

    const GetYearsList = () => {
        return fetch(`/api/get/list/exYears`)
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
                    return data.data.years;
                } else {
                    throw new Error(data.message || 'Failed to load years list');
                }
            })
            .catch(error => {
                console.error('Error fetching years list:', error);
                alert('Unexpected error occurred while fetching years list: ' + error.message);
            });
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

    const OnYearChange = (event) => {
        const selectedYear = event.target.value;
        setSelectedYear(selectedYear);
    }

    const GetHistory = (type) => {
        let endpoint;
        if (type === 'standard') {
            endpoint = `/api/get/history/transfer/${selectedYear}`;
        } else if (type === 'advanced') {
            endpoint = `/api/get/history/transferADV/${selectedYear}`;
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
            <div className="transfer-page container-fluid">
                <h1>Transfer Records</h1>
                <br />
                <Row>
                    {options && (<Forms
                        options={options}
                        formDataSTD={formDataSTD}
                        formDataADV={formDataADV}
                        handleInputChangeSTD={handleInputChangeSTD}
                        handleInputChangeADV={handleInputChangeADV}
                        editMode={editMode}
                        resetForm={resetForm}
                        selectedTable={selectedTable}
                    />)}
                    <br />
                </Row>
                <br />
                <Row>
                    <h3>History</h3>
                </Row>
                <br />
                <Row>
                    <Col md={2}>
                        <h3
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
                        </h3>
                    </Col>
                    <Col md={3}>
                        <h3
                            id="advTitle"
                            onClick={() => {
                                setSelectedTable('advanced');
                                // Reset form when switching tables during edit mode
                                if (editMode.isEditing) {
                                    resetForm();
                                }
                            }}
                            className={selectedTable === 'advanced' ? 'selectedTable' : ''}>
                            Cross-currency Transfers
                        </h3>
                    </Col>
                </Row>
                <Col md={1}>
                    <YearSelectorOnChange
                        yearsList={yearsList}
                        selectedYear={selectedYear}
                        onYearChange={OnYearChange}
                        id="transfer-year-selector"
                    />
                </Col>
                <Row>
                    <div className="table-responsive">
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
                </Row>
            </div>
        </>
    )
}
