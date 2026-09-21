import { useEffect, useState } from "react";
import { HistoryTableWithEdit } from "../commonComponents/Common";
import { useOptions, useHistory } from "../commonComponents/CustomHooks";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Pagination from "react-bootstrap/Pagination";


const PAGE_SIZE = 30;

const initialFormData = {
    year: new Date().getFullYear().toString(),
    month: (new Date().getMonth() + 1).toString(),
    day: '',
    isSpecificDate: false,
    comment: '',
    personBank: '',
    sum: '',
    currency: ''
};

function Forms({ options, ValidateForm, DeleteRecord, handleInputChange, resetForm, editMode, formData, deleteConfirm }) {
    const yearsArr = Array.from({ length: 10 }, (_, i) => (new Date().getFullYear() + i).toString());
    const monthsArr = Array.from({ length: 12 }, (_, i) => (i + 1).toString());

    const formDate = [
        formData.year,
        String(formData.month).padStart(2, '0'),
        String(formData.day).padStart(2, '0')
    ].join('-');

    const handleFullDateChange = (e) => {
        const selectedDate = new Date(e.target.value);
        const year = selectedDate.getFullYear().toString();
        const month = (selectedDate.getMonth() + 1).toString();
        const day = selectedDate.getDate().toString();

        handleInputChange({ target: { name: 'inputYear', value: year } });
        handleInputChange({ target: { name: 'inputMonth', value: month } });
        handleInputChange({ target: { name: 'inputDay', value: day } });
        handleInputChange({ target: { name: 'inputIsSpecificDate', value: true } });
    }

    return (
        <Form noValidate className="form" id="planning-form" onSubmit={ValidateForm}>
            <Row>{formData.isSpecificDate !== true ? (
                <>
                    <Col md={1}>
                        <Form.Label htmlFor="inputYear">Year frame</Form.Label>
                        <Form.Select
                            id="inputYear"
                            name="Year"
                            value={formData.year}
                            onChange={handleInputChange}
                        >
                            {yearsArr.map((year) => (
                                <option key={year} value={year}>
                                    {year}
                                </option>
                            ))}
                        </Form.Select>
                    </Col>
                    <Col md={1}>
                        <Form.Label htmlFor="inputMonth">Month frame</Form.Label>
                        <Form.Select
                            id="inputMonth"
                            name="Month"
                            value={formData.month}
                            onChange={handleInputChange}
                        >
                            {monthsArr.map((month) => (
                                <option key={month} value={month}>
                                    {month}
                                </option>
                            ))}
                        </Form.Select>
                    </Col>
                </>
            )
                : (
                    <Col md={2}>
                        <Form.Label htmlFor="planningInputDate">Timeframe</Form.Label>
                        <input type="date"
                            id="planningInputDate"
                            name="FullDate"
                            value={formDate}
                            onChange={handleFullDateChange}
                        />
                    </Col>
                )}
                <Col md={3}>
                    <Form.Label htmlFor="inputComment">Comment</Form.Label>
                    <Form.Control
                        id="inputComment"
                        name="Comment"
                        value={formData.comment}
                        onChange={handleInputChange}
                    />
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
                <Col md={2}>
                    <Form.Label htmlFor="inputSum">Sum</Form.Label>
                    <Form.Control
                        id="inputSum"
                        name="Sum"
                        value={formData.sum}
                        onChange={handleInputChange}
                    />
                </Col>
                <Col md={2}>
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
                    <Form.Label htmlFor="ToggleSpecificDate">Specific Date?</Form.Label>
                    <Form.Check
                        type="switch"
                        id="ToggleSpecificDate"
                        checked={formData.isSpecificDate}
                        onChange={() =>
                            handleInputChange({
                                target: {
                                    name: 'inputIsSpecificDate',
                                    value: !formData.isSpecificDate
                                }
                            })
                        }
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
                        <Button type="button" onClick={DeleteRecord} id="DeleteButton">
                            {deleteConfirm ? "Confirm Delete?" : "Delete Record"}
                        </Button>
                    )}
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
    )
}

export default function PlanningPage() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState(initialFormData);
    const [editMode, setEditMode] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [deleteConfirm, setDeleteConfirm] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);

    const { options, error: optionsError } = useOptions("");
    const { history, error: historyError } = useHistory("", null);
    const { history: expiredHistory, error: expiredHistoryError } = useHistory("", null);

    const totalPages = Math.ceil((expiredHistory?.length || 0) / PAGE_SIZE);
    const firstRecordIndex = (currentPage - 1) * PAGE_SIZE;
    const visibleExpiredHistory = expiredHistory?.slice(
        firstRecordIndex,
        firstRecordIndex + PAGE_SIZE
    ) || [];

    useEffect(() => {
        document.title = "Planning";
    }, []);

    useEffect(() => {
        // Fetch options error
        if (optionsError) {
            setError('Failed to load options: ' + optionsError);
            setLoading(false);
            console.error('Error loading options:', optionsError);
            return;
        }

        // Fetch history error
        if (historyError) {
            setError('Failed to load history: ' + historyError);
            setLoading(false);
            console.error('Error loading history:', historyError);
            return;
        }
        if (expiredHistoryError) {
            setError('Failed to load expired history: ' + expiredHistoryError);
            setLoading(false);
            console.error('Error loading expired history:', expiredHistoryError);
            return;
        }

        // If both options and histories are loaded, set loading to false
        if (options !== null && history !== null && expiredHistory !== null) {
            setLoading(false);
        }
        setCurrentPage(1);
    }, [history, historyError, expiredHistory, expiredHistoryError, options, optionsError]);

    const ValidateForm = async (e) => {
        e.preventDefault();

        const { month, year, day, comment,  personBank, sum, currency } = formData;

        if (!year || !month || !comment || !sum || !currency) {
            alert("Please fill in all required fields. Timeframe, Comment, Amount and Currency are required.");
            return false;
        }

        if (isNaN(sum)) {
            alert("Please enter a valid sum.");
            return false;
        }

        const requestData = {
            date: `${year}-${month}${day ? `-${day}` : ''}`,
            comment: comment,
            personBank: personBank,
            sum: parseFloat(sum).toFixed(2),
            currency: currency
        };

        const endpoint = editMode
            ? `/api/edit/planning/${editingId}`
            : `/api/add/planning`;

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
        const year = cells[1].innerText.split('-')[0];
        const month = cells[1].innerText.split('-')[1];
        const day = cells[1].innerText.split('-')[2] || '';
        const isSpecificDate = day !== '';

        // Populate form by calling setFormData
        setFormData({
            year: year,
            month: month,
            day: day,
            isSpecificDate: isSpecificDate,
            personBank: cells[4].innerText,
            sum: Math.abs(parseFloat(cells[5].innerText)).toFixed(2),
            currency: cells[6].innerText,
            comment: cells[7].innerText
        });

        setEditMode(true);
        setEditingId(id);
    }

    const DeleteRecord = () => {
        if (!deleteConfirm) {
            setDeleteConfirm(true);
            return;
        }

        const requestData = {
            toDelete: true,
        };

        // Send POST request
        fetch(`/api/edit/planning/${editingId}`, {
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

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    function getPageItems(currentPage, totalPages) {
        if (totalPages <= 7) {
            return Array.from({ length: totalPages }, (_, index) => index + 1);
        }

        const visiblePages = new Set([
            1,
            2,
            currentPage - 2,
            currentPage - 1,
            currentPage,
            currentPage + 1,
            currentPage + 2,
            totalPages - 1,
            totalPages
        ]);

        const pages = [...visiblePages]
            .filter(page => page >= 1 && page <= totalPages)
            .sort((a, b) => a - b);

        const items = [];

        pages.forEach((page, index) => {
            if (index > 0 && page - pages[index - 1] > 1) {
                items.push(`ellipsis-${page}`);
            }

            items.push(page);
        });

        return items;
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

    if (loading) {
        return (
            <>
                <Header />
                <div className="planning-page">
                    <h1>Planning</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="planning-page">
                    <h1>Planning</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="planning-page container-fluid">
                <h1>Planning</h1>
                <Row>
                    <Col>
                        {options && (<Forms
                            options={options}
                            ValidateForm={ValidateForm}
                            DeleteRecord={DeleteRecord}
                            handleInputChange={handleInputChange}
                            resetForm={resetForm}
                            editMode={editMode}
                            formData={formData}
                            deleteConfirm={deleteConfirm}
                        />)}
                        <br />
                    </Col>
                </Row>
                <br />
                <Row>
                    <Col>
                        <h3>Active plans</h3>
                        {history && (
                            <>
                                <HistoryTableWithEdit
                                    columns={
                                        ["ID", "Timeframe", "Comment",
                                            "Person-Bank", "Amount", "Currency",
                                            "Converted to Main Currency"]
                                    }
                                    history={history.data}
                                    EditRecord={EditRecord}
                                    tableId={"active-plans-table"}
                                    numberColumns={["5-2", "7-2"]}
                                />
                                <h5>Total converted amount: {(history.total).toFixed(2)}</h5>
                            </>
                        )}
                    </Col>
                </Row>
                <br />
                <Row>
                    <Col>
                        <h3>Expired plans</h3>
                        {visibleExpiredHistory && (
                            <>
                                <HistoryTableWithEdit
                                    columns={
                                        ["ID", "Timeframe", "Comment",
                                            "Person-Bank", "Amount", "Currency"]
                                    }
                                    history={visibleExpiredHistory}
                                    EditRecord={EditRecord}
                                    tableId={"expired-plans-table"}
                                    numberColumns={["5-2"]}
                                />

                                {totalPages > 1 && (
                                    <Pagination aria-label="Planning expired pages"
                                        className="flex-wrap">
                                        <Pagination.First
                                            disabled={currentPage === 1}
                                            onClick={() => handlePageChange(1)}
                                        />
                                        <Pagination.Prev
                                            disabled={currentPage === 1}
                                            onClick={() => handlePageChange(currentPage - 1)}
                                        />

                                        {getPageItems(currentPage, totalPages).map(item =>
                                            typeof item === "number" ? (
                                                <Pagination.Item
                                                    key={item}
                                                    active={item === currentPage}
                                                    onClick={() => handlePageChange(item)}
                                                >
                                                    {item}
                                                </Pagination.Item>
                                            ) : (
                                                <Pagination.Ellipsis key={item} disabled />
                                            )
                                        )}

                                        <Pagination.Next
                                            disabled={currentPage === totalPages}
                                            onClick={() => handlePageChange(currentPage + 1)}
                                        />
                                        <Pagination.Last
                                            disabled={currentPage === totalPages}
                                            onClick={() => handlePageChange(totalPages)}
                                        />
                                    </Pagination>
                                )}
                            </>)}
                    </Col>
                </Row>
            </div>
        </>
    );
}