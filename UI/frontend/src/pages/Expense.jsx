import { useEffect, useState } from "react";
import { HistoryTableWithEdit, YearSelectorOnChange } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/ExpensePageStyles.css'

const initialFormData = {
    date: new Date().toISOString().split('T')[0],
    category: '',
    subCategory: '',
    personBank: '',
    sum: '',
    currency: '',
    comment: ''
};

function Forms({ options, ValidateForm, handleInputChange, resetForm, editMode, formData }) {
    return (
        <Form noValidate className="form" id="expense-form" onSubmit={ValidateForm}>
            <Row>
                <Col md={2}>
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input type="date"
                        id="ExpenseInputDate"
                        name="Date"
                        value={formData.date}
                        onChange={handleInputChange}
                    />
                </Col>
                <Col md={2}>
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
                <Col md={2}>
                    <Form.Label htmlFor="inputSubCategory">
                        Sub-Category
                    </Form.Label>
                    <Form.Select
                        id="inputSubCategory"
                        name="SubCategory"
                        value={formData.subCategory}
                        onChange={handleInputChange}
                    >
                        <option value="" disabled ></option>
                        {options.subcategories.map((subcategory, index) => (
                            <option value={subcategory} key={index}>{subcategory}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col md={2}>
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
                <Col md={1}>
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
                <Col md={2}>
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
                    <Button type="submit" id="SubmitButton">
                        {editMode ? "Update Record" : "Add Record"}
                    </Button>
                </Col>
                <Col xs={4} md={2}>
                    {editMode && (
                        <Button type="button" onClick={resetForm} id="CancelButton">
                            Cancel Edit
                        </Button>
                    )}
                </Col>
            </Row>
        </Form>
    );
}

export default function ExpensePage() {
    const [options, setOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState(initialFormData);
    const [editMode, setEditMode] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [yearsList, setYearsList] = useState([]);
    const [selectedYear, setSelectedYear] = useState(null);

    useEffect(() => {
        document.title = "Expense Records";

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
    }, [selectedYear]);

    const ValidateForm = async (e) => {
        e.preventDefault();

        const { date, category, subCategory, personBank, sum, currency, comment } = formData;

        if (!date || !category || !subCategory || !personBank || !sum || !currency) {
            alert("Please fill in all required fields.");
            return false;
        }

        if (isNaN(sum) || parseFloat(sum) <= 0) {
            alert("Please enter a valid sum.");
            return false;
        }

        const requestData = {
            date: date,
            category: category,
            subCategory: subCategory,
            personBank: personBank,
            sum: parseFloat(-sum).toFixed(2),
            currency: currency,
            comment: comment
        };

        const endpoint = editMode
            ? `/api/edit/expense/${editingId}`
            : `/api/add/expense`;

        // Send POST request
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    resetForm();
                    window.location.reload();
                } else {
                    alert('Error: ' + (data.message || 'Failed to process transaction'));
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

    const GetOptions = () => {
        return fetch(`/api/get/options/expense`)
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

    const GetHistory = () => {
        return fetch(`/api/get/history/expense/${selectedYear}`)
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

    const OnYearChange = (event) => {
        const selectedYear = event.target.value;
        setSelectedYear(selectedYear);
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
            subCategory: cells[3].innerText,
            personBank: cells[4].innerText,
            sum: Math.abs(parseFloat(cells[5].innerText)).toFixed(2),
            currency: cells[6].innerText,
            comment: cells[7].innerText
        });

        setEditMode(true);
        setEditingId(id);
    }

    if (loading) {
        return (
            <>
                <Header />
                <div className="expense-page">
                    <h1>Expense Records</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="expense-page">
                    <h1>Expense Records</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="expense-page container-fluid">
                <Row>
                    <Col xs={12} md={11}>
                        <h1>Expense Records</h1>
                        {options && (<Forms
                            options={options}
                            ValidateForm={ValidateForm}
                            handleInputChange={handleInputChange}
                            resetForm={resetForm}
                            editMode={editMode}
                            formData={formData}
                        />)}
                        <br />
                    </Col>
                </Row>
                <br />
                <Row>
                    <h3>History</h3>
                    <br />
                    <Col md={10}>
                    <br />
                    </Col>
                    <Col md={1}>
                        <YearSelectorOnChange
                            yearsList={yearsList}
                            selectedYear={selectedYear}
                            onYearChange={OnYearChange}
                            id="expense-year-selector"
                        />
                    </Col>
                    <Col xs={12}>
                        <div className="table-responsive">
                            {history && (
                                <HistoryTableWithEdit
                                    columns={["ID", "Date", "Category", "Sub-category", "Person-Bank", "Sum", "Currency", "Comment"]}
                                    data={history}
                                    EditRecord={EditRecord}
                                    tableId={"expenseHistoryTable"}
                                    numberColumns={["5-2"]}
                                />
                            )}
                        </div>
                    </Col>
                </Row>
            </div>
        </>
    )
}
