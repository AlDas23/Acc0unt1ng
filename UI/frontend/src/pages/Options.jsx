import { useState, useEffect } from "react";
import Header from "../commonComponents/Header";
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Modal from 'react-bootstrap/Modal';
import Button from "react-bootstrap/esm/Button";
import '../assets/styles/OptionsPageStyles.css';

export function OptionsPBPage() {
    const [personBanks, setPersonBanks] = useState([])
    const [markers, setMarkers] = useState({ owners: [], types: [] })
    const [currencyList, setCurrencyList] = useState([])
    const [useOwnerInput, setUseOwnerInput] = useState(false)
    const [useTypeInput, setUseTypeInput] = useState(false)
    const [personBankName, setPersonBankName] = useState('');
    const [submitStatus, setSubmitStatus] = useState('idle');

    useEffect(() => {
        document.title = "PB options"

        // Fetch person banks data
        fetch('/api/get/list/pb')
            .then(response => response.json())
            .then(data => {
                if (data.redirect) {
                    alert('Database is missing or corrupted. You will be redirected to the setup page.');
                    window.location.href = data.redirect;
                    return Promise.reject('Redirect initiated');
                }

                if (data.success) {
                    setPersonBanks(data.data);
                } else {
                    console.error('Failed to fetch person banks:', data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching person banks:', error);
            });

        // Fetch markers data
        fetch('/api/get/list/markers')
            .then(response => response.json())
            .then(data => {
                if (data.redirect) {
                    alert('Database is missing or corrupted. You will be redirected to the setup page.');
                    window.location.href = data.redirect;
                    return Promise.reject('Redirect initiated');
                }

                if (data.success) {
                    setMarkers({ owners: data.data.owners || [], types: data.data.types || [] });
                } else {
                    console.error('Failed to fetch markers:', data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching markers:', error);
            });

        // Fetch currency list
        fetch('/api/get/list/currency')
            .then(response => response.json())
            .then(data => {
                if (data.redirect) {
                    alert('Database is missing or corrupted. You will be redirected to the setup page.');
                    window.location.href = data.redirect;
                    return Promise.reject('Redirect initiated');
                }

                if (data.success) {
                    setCurrencyList(data.currencies);
                } else {
                    console.error('Failed to fetch markers:', data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching markers:', error);
            });
    }, []);

    const markPB = (e) => {
        e.preventDefault();
        // TODO: Form submission logic
        console.log('Form submitted');
    };

    const addPB = (e) => {
        e.preventDefault();

        const form = e.target;
        const formDataObj = new FormData(form);
        const formObject = Object.fromEntries(formDataObj.entries());
        const regex = /[!@#$%^&*()+={}[\]:;"'<>,.?/|\\]/;

        if (regex.test(formObject.PersonBank)) {
            alert("Person-bank name contains special characters!")
            return false;
        }
        if (isNaN(parseFloat(formObject.Sum))) {
            alert("Amount is Not A Number!")
            return false;
        }

        fetch("/api/spv/pb/add", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formObject)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    setSubmitStatus('success');
                    setTimeout(() => {
                        window.location.reload();
                    }, 3000);
                } else {
                    alert('Error: ' + (data.message || 'Failed to add Person-bank'));
                }
            })
            .catch(error => {
                console.error('Unexpected error:', error);
                alert('Unexpected error occurred');
            });
    };

    return (
        <>
            <Header />
            <div className="options-page container">
                <div className="row">
                    <h3>Modify markers</h3>
                    <br />
                    <p>
                        Markers are used by system to understand <b>WHO</b> owns the account and what <b>TYPE</b> of account it is.
                        Account without markers can be used, but it might not appear on balance sheet and be left out from calculation of some data.
                    </p>
                    <br />
                    <Form noValidate id="mark-form" onSubmit={markPB}>
                        <Row>
                            <Col xl="3">
                                <Form.Label htmlFor="select-pb">Person-Bank</Form.Label>
                                <Form.Select id="select-pb" name="person-bank-select">
                                    {personBanks && personBanks.map((pb, index) => (
                                        <option key={index} value={pb}>{pb}</option>
                                    ))}
                                </Form.Select>
                            </Col>
                            <Col xl="3">
                                <Form.Label htmlFor="select-owner">Owner</Form.Label>
                                <div className="d-flex align-items-center">
                                    {useOwnerInput ? (
                                        <Form.Control type="text" id="input-owner" name="owner-input" />
                                    ) : (
                                        <Form.Select id="select-owner" name="owner-select">
                                            {markers.owners.map((owner, index) => (
                                                <option key={index} value={owner}>{owner}</option>
                                            ))}
                                        </Form.Select>
                                    )}
                                    <Button
                                        variant="outline-secondary"
                                        className="ms-2 toggle-input"
                                        onClick={() => setUseOwnerInput(!useOwnerInput)}
                                    >
                                        {useOwnerInput ? 'Use Select' : 'Use Text'}
                                    </Button>
                                </div>
                            </Col>
                            <Col xl="3">
                                <Form.Label htmlFor="select-type">Type</Form.Label>
                                <div className="d-flex align-items-center">
                                    {useTypeInput ? (
                                        <Form.Control type="text" id="input-type" name="type-input" />
                                    ) : (
                                        <Form.Select id="select-type" name="type-select">
                                            {markers.types.map((type, index) => (
                                                <option key={index} value={type}>{type}</option>
                                            ))}
                                        </Form.Select>
                                    )}
                                    <Button
                                        variant="outline-secondary"
                                        className="ms-2 toggle-input"
                                        onClick={() => setUseTypeInput(!useTypeInput)}
                                    >
                                        {useTypeInput ? 'Use Select' : 'Use Text'}
                                    </Button>
                                </div>
                            </Col>
                        </Row>
                        <Row className="mt-3">
                            <Col>
                                <Button variant="primary" type="submit">
                                    Update Markers
                                </Button>
                            </Col>
                        </Row>
                    </Form>
                </div>
                <br />
                <div className="row">
                    <h3>Add Person-Bank</h3>
                    <p>
                        Person-Bank is name of account used for keeping balance.
                        Person-Bank name should generally follow <i>Person</i> - <i>Bank</i> name convention and be unique.
                        When adding Person-Bank, account must have a currency and initial sum for that currency.
                        You can add multiple currencies to each accout by writing it's name again and selecting new currency.
                    </p>
                    <Form noValidate id="pb-form" onSubmit={addPB}>
                        <Row>
                            <Col xl="3">
                                <Form.Label htmlFor="input-pb">
                                    Person-Bank account name
                                </Form.Label>
                                <Form.Control type="text" id="input-pb" name="PersonBank" autoComplete="off" value={personBankName}
                                    onChange={(e) => setPersonBankName(e.target.value)} />
                            </Col>
                            <Col xl="2">
                                <Form.Label htmlFor="input-sum">
                                    Initial amount
                                </Form.Label>
                                <Form.Control type="text" id="input-sum" name="Sum" autoComplete="off" />
                            </Col>
                            <Col xl="2">
                                <Form.Label htmlFor="input-curr">
                                    Currency for Person-Bank
                                </Form.Label>
                                <Form.Select type="text" id="input-curr" name="Currency">
                                    {currencyList.map((currency, index) => (
                                        <option value={currency} key={index}>{currency}</option>
                                    ))}
                                </Form.Select>
                            </Col>
                        </Row>
                        <br />
                        <Button
                            variant={submitStatus === 'success' ? 'success' : 'primary'}
                            type="submit"
                            id="btn-add-pb"
                            disabled={submitStatus === 'success'}
                        >
                            {submitStatus === 'success'
                                ? 'Success!'
                                : personBanks.some(pb => pb === personBankName)
                                    ? 'Update Person-Bank'
                                    : 'Add Person-Bank'}
                            {/* BUG: Button does not render "Update Person-Bank" when adding existing person-bank */}
                        </Button>
                    </Form>
                </div>
            </div>
        </>
    )
}

export function OptionsDBPage() {
    const [currentLists, setCurrentLists] = useState({ curr: [], incCat: [], expCat: [], subCat: [] });
    const [isDBExists, setIsDBExists] = useState(false);
    const [show, setShow] = useState(false);
    const [confirmationText, setConfirmationText] = useState('');
    const [currencyValues, setCurrencyValues] = useState('');
    const [incCatValues, setIncCatValues] = useState('');
    const [expCatValues, setExpCatValues] = useState('');
    const [subCatValues, setSubCatValues] = useState('');

    useEffect(() => {
        document.title = "Database options";

        fetch('/api/spv')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const curr = data.data.currency || [];
                    const incCat = data.data.incomeCategories || [];
                    const expCat = data.data.expenseCategories || [];
                    const subCat = data.data.subCategories || [];

                    setCurrentLists({ curr, incCat, expCat, subCat });
                    setCurrencyValues(curr.join("\n"));
                    setIncCatValues(incCat.join("\n"));
                    setExpCatValues(expCat.join("\n"));
                    setSubCatValues(subCat.join("\n"));
                } else {
                    console.error('Failed to fetch SPVs:', data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching SPVs:', error);
            });

        // Fetch DB status
        fetch('/api/database/status')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    setIsDBExists(true);
                } else if (data.corrupt) {
                    setIsDBExists(true); // DB exists but is corrupted
                } else if (!data.success && !data.corrupt) {
                    setIsDBExists(false); // DB does not exist
                } else {
                    console.error('Failed to fetch DB status:', data.message);
                }
            })
            .catch(error => {
                console.error('Error fetching DB status:', error);
            });
    }, []);

    const handleClose = () => {
        setShow(false);
        setConfirmationText('');
    };
    const handleShow = () => setShow(true);

    const handleDatabaseAction = () => {
        // Close the modal first
        handleClose();

        // Determine the action based on isDBExists
        const action = isDBExists ? 'recreate' : 'create';

        // Call the API to perform the database action
        fetch('/api/database/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the database status
                    setIsDBExists(action === 'create' || action === 'recreate');
                    alert(`Database ${action === 'create' ? 'created' : 'recreated'} successfully!`);
                } else {
                    alert('Error: ' + (data.message || `Failed to ${action} database`));
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert(`An error occurred while ${action === 'create' ? 'creating' : 'recreating'} the database.`);
            });
    };


    const saveChanges = (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);
        const updatedLists = {
            curr: formData.get("currency-values").split("\n").map(item => item.trim()).filter(item => item),
            incCat: formData.get("inccat-values").split("\n").map(item => item.trim()).filter(item => item),
            expCat: formData.get("expcat-values").split("\n").map(item => item.trim()).filter(item => item),
            subCat: formData.get("subcat-values").split("\n").map(item => item.trim()).filter(item => item),
        };

        fetch('/api/spv', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedLists),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.message || 'Failed to update special values'));
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    return (
        <>
            <Header />
            <div className="options-page container">
                <h2>Special Values Control</h2>
                <div className="row">
                    <Form noValidate id="spv-form" onSubmit={saveChanges}>
                        <Row>
                            <Col>
                                <Form.Label htmlFor="currency-values">Currency Values</Form.Label>
                                {currentLists &&
                                    (<textarea form="spv-form" value={currencyValues} onChange={(e) => setCurrencyValues(e.target.value)} id="currency-values" name="currency-values" rows="13" cols="25" />)}
                            </Col>
                            <Col>
                                <Form.Label htmlFor="inccat-values">Income Category Values</Form.Label>
                                {currentLists &&
                                    (<textarea form="spv-form" value={incCatValues} onChange={(e) => setIncCatValues(e.target.value)} id="inccat-values" name="inccat-values" rows="13" cols="25" />)}
                            </Col>
                            <Col>
                                <Form.Label htmlFor="expcat-values">Expense Category Values</Form.Label>
                                {currentLists &&
                                    (<textarea form="spv-form" value={expCatValues} onChange={(e) => setExpCatValues(e.target.value)} id="expcat-values" name="expcat-values" rows="13" cols="25" />)}
                            </Col>
                            <Col>
                                <Form.Label htmlFor="subcat-values">Subcategory Values</Form.Label>
                                {currentLists &&
                                    (<textarea form="spv-form" value={subCatValues} onChange={(e) => setSubCatValues(e.target.value)} id="subcat-values" name="subcat-values" rows="13" cols="25" />)}
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
                <div className="row" id="db-control-section">
                    <h2>Database Control</h2>
                    <Button
                        variant={isDBExists ? 'danger' : 'primary'}
                        id="db-cntrl-btn"
                        onClick={handleShow}
                    >
                        {isDBExists ? 'Re-create Database' : 'Create Database'}
                    </Button>

                    <Modal show={show} onHide={handleClose}>
                        <Modal.Header closeButton>
                            <Modal.Title>Confirm Database Action</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                            {isDBExists ? (
                                <div>
                                    <p>Are you sure you want to re-create the database? This will delete all existing data.</p>
                                    <p>Please type "I want to re-create database" to confirm:</p>
                                    <Form.Control
                                        type="text"
                                        value={confirmationText}
                                        onChange={(e) => setConfirmationText(e.target.value)}
                                        placeholder="I want to re-create database"
                                    />
                                </div>
                            ) : (
                                <p>Are you sure you want to create the database?</p>
                            )}
                        </Modal.Body>
                        <Modal.Footer>
                            <Button variant="secondary" onClick={handleClose}>
                                Cancel
                            </Button>
                            <Button
                                variant={isDBExists ? 'danger' : 'primary'}
                                onClick={handleDatabaseAction}
                                disabled={isDBExists && confirmationText !== "I want to re-create database"}
                            >
                                {isDBExists ? 'Re-create Database' : 'Create Database'}
                            </Button>
                        </Modal.Footer>
                    </Modal>
                </div>
            </div>
        </>
    )
}
