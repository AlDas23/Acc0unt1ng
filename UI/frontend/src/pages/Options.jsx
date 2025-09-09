import { useState, useEffect } from "react";
import Header from "../commonComponents/Header";
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from "react-bootstrap/esm/Button";

export function OptionsPB() {
    // TODO: Implement Person-Bank set-up page
}

export function OptionsDB() {
    const [currentLists, setCurrentLists] = useState({ curr: [], incCat: [], expCat: [], subCat: [] });
    const [isDBExists, setIsDBExists] = useState(false);
    const [show, setShow] = useState(false);
    const [confirmationText, setConfirmationText] = useState('');

    useEffect(() => {
        fetch('/api/spv')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    setCurrentLists({
                        curr: data.data.currency || [],
                        incCat: data.data.incomeCategories || [],
                        expCat: data.data.expenseCategories || [],
                        subCat: data.data.subCategories || []
                    });
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
                    setIsDBExists(data.exists);
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
                <div className="row">
                    <h2>Special Values Control</h2>
                    <Form noValidate id="spv-form" onSubmit={saveChanges}>
                        <div className="col">
                            <Form.Label htmlFor="currency-values">Currency Values</Form.Label>
                            {currentLists &&
                                (<textarea form="spv-form" id="currency-values" name="currency-values" rows="25" cols="30">
                                    {currentLists.curr.join("\n")}
                                </textarea>)}
                            <br />
                            <Button variant="primary" type="submit" id="save-spv-btn">
                                Save Changes
                            </Button>
                        </div>
                        <div className="col">
                            <Form.Label htmlFor="inccat-values">Income Category Values</Form.Label>
                            {currentLists &&
                                (<textarea form="spv-form" id="inccat-values" name="inccat-values" rows="25" cols="30">
                                    {currentLists.incCat.join("\n")}
                                </textarea>)}
                        </div>
                        <div className="col">
                            <Form.Label htmlFor="expcat-values">Expense Category Values</Form.Label>
                            {currentLists &&
                                (<textarea form="spv-form" id="expcat-values" name="expcat-values" rows="25" cols="30">
                                    {currentLists.expCat.join("\n")}
                                </textarea>)}
                        </div>
                        <div className="col">
                            <Form.Label htmlFor="subcat-values">Subcategory Values</Form.Label>
                            {currentLists &&
                                (<textarea form="spv-form" id="subcat-values" name="subcat-values" rows="25" cols="30">
                                    {currentLists.subCat.join("\n")}
                                </textarea>)}
                        </div>
                    </Form>
                </div>
                <div className="row">
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
