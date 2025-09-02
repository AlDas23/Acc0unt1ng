import { useEffect, useState } from "react";
import { HistoryTableWithEdit } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/IncomePageStyles.css';

const initialFormData = {
    date: new Date().toISOString().split('T')[0],
    category: '',
    personBank: '',
    sum: '',
    currency: '',
    comment: ''
};

function Forms({ options, ValidateForm, handleInputChange, resetForm, editMode, formData }) {
    return (
        <Form noValidate className="form" id="form" onSubmit={ValidateForm}>
            <Row>
                <Col xl="2">
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input type="date"
                        id={"inputDate"}
                        name={"Date"}
                        value={formData.date}
                        onChange={handleInputChange}
                    />
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputCategory">
                        Category
                    </Form.Label>
                    <Form.Select
                        id="inputCategory"
                        name="Category"
                        value={formData.category}
                        onChange={handleInputChange}
                    >
                        <option value="" disabled></option>
                        {options.categories.map((category, index) => (
                            <option value={category} key={index}>{category}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputPersonBank">
                        Person-Bank
                    </Form.Label>
                    <Form.Select
                        id="inputPersonBank"
                        name="PersonBank"
                        value={formData.personBank}
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
                        Amount
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
                <Button type="submit" id="SubmitButton">
                    {editMode ? "Update Record" : "Add Record"}
                </Button>
            </Row>
            <Row>
                {editMode && (
                    <Button type="button" onClick={resetForm} id="CancelButton">
                        Cancel Edit
                    </Button>
                )}
            </Row>
        </Form>
    );
}

export default function IncomePage() {
    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState(initialFormData);
    const [editMode, setEditMode] = useState(false);
    const [editingId, setEditingId] = useState(null);

    useEffect(() => {
        document.title = "Income Records";
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
        GetHistory()
            .then(historyData => {
                setHistory(historyData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load history: ' + error.message);
                setLoading(false);
                console.error('Error loading history:', error);
            });
    }, []);

    const GetOptions = () => {
        return fetch('http://localhost:5050/api/get/options/income')
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

    const GetHistory = () => {
        return fetch('http://localhost:5050/api/get/history/income')
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

    const ValidateForm = async (e) => {
        e.preventDefault();

        const { date, category, personBank, sum, currency, comment } = formData;

        if (!date || !category || !personBank || !sum || !currency) {
            alert("Please fill in all required fields.");
            return false;
        }

        const RequestData = {
            date: date,
            category: category,
            subCategory: "",
            personBank: personBank,
            sum: parseFloat(sum).toFixed(2),
            currency: currency,
            comment: comment
        };

        const endpoint = editMode
            ? `http://localhost:5050/api/edit/income/${editingId}`
            : 'http://localhost:5050/api/add/income';

        // Send POST request
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(FormData)
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
                    alert('Error: ' + (data.message || 'Failed to add transaction'));
                }
            })
            .catch(error => {
                console.error('Unexpected error:', error);
                alert('Unexpected error occurred');
            });
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        const key = name.replace('input', '');
        setFormData(prevData => ({
            ...prevData,
            [key.charAt(0).toLowerCase() + key.slice(1)]: value
        }));
    };

    const resetForm = () => {
        setFormData(initialFormData);
        setEditMode(false);
        setEditingId(null);

        // Show all rows again
        const rows = document.querySelectorAll('.history-table tbody tr');
        rows.forEach(row => {
            row.style.display = '';
        });
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

        // Populate form by calling setFormData
        setFormData({
            date: cells[1].innerText,
            category: cells[2].innerText,
            personBank: cells[3].innerText,
            sum: Math.abs(parseFloat(cells[4].innerText)).toFixed(2),
            currency: cells[5].innerText,
            comment: cells[6].innerText
        });

        setEditMode(true);
        setEditingId(id);
    }

    if (loading) {
        return (
            <>
                <Header />
                <div className="income-page">
                    <h1>Income Records</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="income-page">
                    <h1>Income Records</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="income-page container">
                <div className="row">
                    <div className="col-bg-12">
                        <h1>Income Records</h1>
                        {options && (<Forms
                            options={options}
                            ValidateForm={ValidateForm}
                            handleInputChange={handleInputChange}
                            resetForm={resetForm}
                            editMode={editMode}
                            formData={formData}
                        />)}
                        <br />
                    </div>
                </div>
                <br />
                <div className="row">
                    <h3>History</h3>
                    <br />
                    {history && (<HistoryTableWithEdit
                        columns={["ID", "Date", "Category", "Person-Bank", "Sum", "Currency", "Comment"]}
                        data={history}
                        EditRecord={EditRecord}
                    />)}
                </div>
            </div>
        </>
    )

}
