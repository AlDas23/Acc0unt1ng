import { useEffect, useState } from "react";
import { HistoryTable, HistoryTableWithClose } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Pagination from "react-bootstrap/Pagination";
import '../assets/styles/DepositPageStyles.css'

const PAGE_SIZE = 15;


function Forms({ options }) {
    return (
        <Form noValidate className="form" id="form" onSubmit={(e) => {
            e.preventDefault();
            const form = e.target;
            const formDataObj = new FormData(form);
            const formObject = Object.fromEntries(formDataObj.entries());

            if (!formObject.DateIn || !formObject.Name || !formObject.Owner || isNaN(formObject.Sum) || !formObject.Currency || !formObject.DateOut) {
                alert("Please fill in all reqired fields.\n Deposit date, name, owner, sum, currency, percent are required.");
                return false;
            }

            if (isNaN(formObject.Sum) || formObject.Sum <= 0) {
                alert("Please enter a valid sum.");
                return false;
            }

            if (!formObject.Months && (isNaN(formObject.Months) || formObject.Months <= 0)) {
                alert("Please enter a valid number of months.");
                return false;
            }

            if (isNaN(formObject.Percent) || formObject.Percent < 0 || formObject.Percent > 100) {
                alert("Please enter a valid percent.");
                return false;
            }

            if (formObject.CurrencyRate && (isNaN(formObject.CurrencyRate) || formObject.CurrencyRate <= 0)) {
                alert("Please enter a valid currency rate.");
                return false;
            }

            // Send POST request
            fetch(`/api/add/deposit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formObject)
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
                        alert('Error: ' + (data.message || 'Failed to add deposit'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}>
            <Row>
                <Col md={2}>
                    <Form.Label htmlFor="inputDateIn">
                        Deposit Date
                    </Form.Label>
                    <input type="date" id="inputDateIn" name="DateIn" defaultValue={new Date().toISOString().split('T')[0]} className="datePicker" />
                </Col>
                <Col md={3}>
                    <Form.Label htmlFor="inputName">
                        Deposit Name
                    </Form.Label>
                    <Form.Control type="text" id="inputName" name="Name" autoComplete="off" />
                </Col>
                <Col md={2}>
                    <Form.Label htmlFor="inputOwner">
                        Person-bank
                    </Form.Label>
                    <Form.Select id="inputOwner" name="Owner" defaultValue={""}>
                        <option value="" disabled></option>
                        {options.pb.map((pb, index) => (
                            <option value={pb} key={index}>{pb}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col md={1}>
                    <Form.Label htmlFor="inpuSum">
                        Sum
                    </Form.Label>
                    <Form.Control type="text" id="inpuSum" name="Sum" autoComplete="off" />
                </Col>
                <Col md={1}>
                    <Form.Label htmlFor="inputCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select id="inputCurrency" name="Currency" defaultValue={""}>
                        <option value="" disabled></option>
                        {options.currencies.map((currencies, index) => (
                            <option value={currencies} key={index}>{currencies}</option>
                        ))}
                    </Form.Select>
                </Col>
            </Row>
            <Row className="Deposit-middlerow">
                <Col md={1}>
                    <Form.Label htmlFor="inputMonths">
                        Months
                    </Form.Label>
                    <Form.Control type="text" id="inputMonths" name="Months" autoComplete="off" />
                </Col>
                <Col md={2}>
                    <Form.Label htmlFor="inputDateOut">
                        Closing Date
                    </Form.Label>
                    <input type="date" id="inputDateOut" name="DateOut" className="datePicker" />
                </Col>
                <Col md={1}>
                    <Form.Label htmlFor="inputPercent">
                        %
                    </Form.Label>
                    <Form.Control type="text" id="inputPercent" name="Percent" autoComplete="off" />
                </Col>
                <Col md={1}>
                    <Form.Label htmlFor="inputCurrencyRate">
                        Currency Rate
                    </Form.Label>
                    <Form.Control type="text" id="inputCurrencyRate" name="CurrencyRate" autoComplete="off" />
                </Col>
                <Col md={4}>
                    <Form.Label htmlFor="inputComment">
                        Comment
                    </Form.Label>
                    <Form.Control type="text" id="inputComment" name="Comment" autoComplete="off" />
                </Col>

            </Row>
            <Row>
                <Col md={2} xs={6}>
                    <Button type="submit" id="SubmitButton">Submit record</Button>
                </Col>
            </Row>
        </Form>
    );
}

export default function DepositPage() {
    const [options, setOptions] = useState(null);
    const [historyO, setHistoryO] = useState(null);
    const [historyC, setHistoryC] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);

    const totalPages = Math.ceil((historyC?.length || 0) / PAGE_SIZE);
    const firstRecordIndex = (currentPage - 1) * PAGE_SIZE;
    const visibleHistory = historyC?.slice(
        firstRecordIndex,
        firstRecordIndex + PAGE_SIZE
    ) || [];

    useEffect(() => {
        document.title = "Deposit Records";
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
        GetHistory(true)
            .then(historyData => {
                setHistoryO(historyData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load history: ' + error.message);
                setLoading(false);
                console.error('Error loading history:', error);
            });
        GetHistory(false)
            .then(historyData => {
                setHistoryC(historyData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load history: ' + error.message);
                setLoading(false);
                console.error('Error loading history:', error);
            });
        setCurrentPage(1);
    }, []);

    const GetOptions = () => {
        return fetch(`/api/get/options/deposit`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    return data.options;
                } else if (data.redirect) {
                    alert('Database is missng or corrupted. You will be redirected to the setup page.');
                    window.location.href = data.redirect;
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

    const GetHistory = (isActive) => {
        if (isActive) {
            return fetch(`/api/get/history/depositO`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        return data.history;
                    } else if (data.redirect) {
                        alert('Database is missng or corrupted. You will be redirected to the setup page.');
                        window.location.href = data.redirect;
                    } else {
                        throw new Error(data.message || 'Failed to load history');
                    }
                })
                .catch(error => {
                    console.error('Error fetching history:', error);
                    alert('Unexpected error occurred while fetching history: ' + error.message);
                    throw error;
                });
        } else {
            return fetch(`/api/get/history/depositC`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        return data.history;
                    } else if (data.redirect) {
                        alert('Database is missng or corrupted. You will be redirected to the setup page.');
                        window.location.href = data.redirect;
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

    const CloseDeposit = (e, rowIndex) => {
        e.preventDefault();
        const rowData = historyO[rowIndex];
        const depositName = rowData[1];

        if (!window.confirm(`Are you sure you want to close the deposit "${depositName}"?`)) {
            return;
        }

        // Send POST request
        fetch(`/api/edit/deposit/${depositName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
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

    if (loading) {
        return (
            <>
                <Header />
                <div className="deposit-page">
                    <h1>Deposit Records</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="deposit-page">
                    <h1>Deposit Records</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="deposit-page container-fluid">
                <h1>Deposit Records</h1>
                {options && (<Forms options={options} />)}
                <br />
                <Row>
                    <Col>
                        <h3>Active deposits</h3>
                        <div className="table-responsive">
                            {historyO && (<HistoryTableWithClose
                                columns={["Deposit Date", "Name", "Person-bank", "Sum", "Currency", "Months", "Closing Date", "%", "Currency rate", "Expected amount", "Comment"]}
                                data={historyO}
                                CloseFn={CloseDeposit}
                                tableId="openDepositsTable"
                                numberColumns={["3-2", "7-1", "8-4", "9-2"]}
                            />)}
                        </div>
                    </Col>
                </Row>
                <br />
                <Row>
                    <Col>
                        <h3>Closed deposits</h3>
                        <div className="table-responsive">
                            {historyC && (
                                <>
                                    <HistoryTable
                                        columns={["Deposit Date", "Name", "Person-bank", "Sum", "Currency", "Months", "Closing Date", "%", "Currency rate", "Expected amount", "Comment"]}
                                        data={visibleHistory}
                                        tableId="closedDepositsTable"
                                        numberColumns={["3-2", "7-1", "8-4", "9-2"]}
                                    />

                                    {totalPages > 1 && (
                                        <Pagination aria-label="Deposit closed history pages"
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
                                </>
                            )}
                        </div>
                    </Col>
                </Row>
            </div>
        </>
    )
}
