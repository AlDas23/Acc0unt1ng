import { useState, useEffect } from "react";
import Header from "../commonComponents/Header";
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Modal from 'react-bootstrap/Modal';
import Button from "react-bootstrap/esm/Button";
import '../assets/styles/OptionsPageStyles.css';

export function OptionsPBPage() {
    return (
        <>
            <Header />
            <div className="options-page container">
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
        fetch('/api/database/' + action, {
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
            </div >
        </>
    )
}
