import { useEffect, useState } from "react";
import { HistoryTableWithEdit, YearSelectorOnChange } from "../commonComponents/Common";
import { useOptions, useHistory } from "../commonComponents/CustomHooks";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/CurrRatePageStyles.css'
import OverlayTrigger from "react-bootstrap/esm/OverlayTrigger";
import Tooltip from 'react-bootstrap/Tooltip';
import Pagination from "react-bootstrap/Pagination";

const initialFormData = {
    date: new Date().toISOString().split('T')[0],
    currency_M: "",
    currency_S: "",
    rate: "",
    isReverse: false
};

const PAGE_SIZE = 30;

function Forms({ options, DeleteRecord, handleInputChange, resetForm, formData, editMode, deleteConfirm, editingId }) {
    return (
        <Form noValidate className="form" id="CurrecyRateForm" onSubmit={(e) => {
            e.preventDefault();
            var { date, currency_M, currency_S, rate } = formData;
            const isReverseCheckbox = document.getElementById('checkReverse');
            var isReverse = isReverseCheckbox.checked;

            if (currency_S === "" && currency_M === "") {
                alert("Currency cannot be empty!")
                return false;
            }

            if (currency_S === currency_M) {
                alert("Selected currencies cannot be same!")
                return false;
            }

            if (isNaN(rate) || rate <= 0) {
                alert("Rate is not a number!")
                return false;
            }

            const payload = {
                date: date,
                currency_M: currency_M,
                currency_S: currency_S,
                rate: rate,
                isReverse: isReverse
            }

            const endpoint = editMode
                ? `/api/edit/currencyrates/${editingId}`
                : `/api/add/currencyrates`;

            // Send POST request
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        alert('Error: ' + (data.message || 'Failed to add currency rate'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}>
            <Row>
                <Col md={2} xs={11}>
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input type="date" id="CurrRateInputDate" name="Date" value={formData.date}
                        onChange={handleInputChange} />
                </Col>
                <Col md={1} xs={11}>
                    <Form.Label htmlFor="inputCurrency_M">
                        Currency Sell
                    </Form.Label>
                    <Form.Select id="inputCurrency_M" name="Currency_M"
                        value={formData.currency_M}
                        onChange={handleInputChange}
                    >
                        <option value="" disabled></option>
                        {options.currency.map((currency, index) => (
                            <option value={currency} key={index}>{currency}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col md={1} xs={11}>
                    <Form.Label htmlFor="inputCurrency_S">
                        Currency Buy
                    </Form.Label>
                    <Form.Select id="inputCurrency_S" name="Currency_S"
                        value={formData.currency_S}
                        onChange={handleInputChange}
                    >
                        <option value="" disabled></option>
                        {options.currency.map((currency, index) => (
                            <option value={currency} key={index}>{currency}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col md={1} xs={11}>
                    <Form.Label htmlFor="inputRate">
                        Rate
                    </Form.Label>
                    <Form.Control type="text" id="inputRate" name="Rate" autoComplete="off"
                        value={formData.rate}
                        onChange={handleInputChange}
                    />
                </Col>
            </Row>
            <Row>
                <Col md={1} xs={2}>
                    <Button type="submit" value="Submit" id="SubmitButton">Submit</Button>
                </Col>
                {editMode ? (
                    <>
                        <Col xs={4} md={2}>
                            <Button type="button" onClick={DeleteRecord} id="DeleteButton">
                                {deleteConfirm ? "Confirm Delete?" : "Delete Record"}
                            </Button>
                        </Col>
                        <Col xs={4} md={2}>
                            <Button type="button" onClick={resetForm} id="CancelButton">
                                Cancel Edit
                            </Button>
                        </Col>
                    </>) : (
                    <>
                        <Col md={1} xs={4}>
                            <OverlayTrigger
                                placement="left"
                                overlay={
                                    <Tooltip id="tooltip-reverse-currrate">
                                        If checked, two currency rates will be recorded.
                                        One with original rate, and one with reversed rate.
                                    </Tooltip>
                                }
                            >
                                <Form.Check
                                    type="switch"
                                    id="checkReverse"
                                    name="IsReverse"
                                />
                            </OverlayTrigger>
                        </Col>
                        <Col md={2} xs={4}>
                            <Form.Label htmlFor="checkReverse" id="checkReverseLabel">
                                Reverse rate
                            </Form.Label>
                        </Col>
                    </>
                )}
            </Row>
        </Form>
    );
};

function PlotComponent({ currencyList, onFilterChange, FetchFilteredPlot, imageUrl }) {
    const rows = [];
    for (let i = 0; i < currencyList.length; i += 4) {
        rows.push(currencyList.slice(i, i + 4));
    }

    return (
        <div className="CurrRate-plotComponent">
            <h3 className="currPlotText">Currency dynamics plot</h3>
            <br />
            <p className="currPlotText">Select currencies to display on the plot:</p>
            <Form noValidate className="form" id="plotFilters" onSubmit={FetchFilteredPlot}>
                {rows.map((row, rowIndex) => (
                    <Row key={`row-${rowIndex}`}>
                        {row.map((name, nameIndex) => {
                            const idx = rowIndex * 4 + nameIndex;
                            return (
                                <Col key={`chk-${idx}`} xs={3}>
                                    <div className="checkbox-container">
                                        <input
                                            type="checkbox"
                                            name={name}
                                            id={`checkbox-${idx}`}
                                            value={name}
                                            onChange={(e) => onFilterChange && onFilterChange(name, e.target.checked)} />
                                        <label htmlFor={`checkbox-${idx}`} className="checkboxLabel">{name}</label>
                                    </div>
                                </Col>
                            );
                        })}
                    </Row>
                ))}
                <br />
                <Button type="submit" value="Submit" id="ApplyFiltersButton">Apply Filters</Button>
            </Form>
            <br />
            <img id="CurrRatePlot" src={imageUrl} alt="Currency dynamics plot" />
        </div>
    )
};

export default function CurrencyRatesPage() {
    const [formData, setFormData] = useState(initialFormData);
    const [editMode, setEditMode] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [deleteConfirm, setDeleteConfirm] = useState(false);
    const [plotOptions, setPlotOptions] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedCurrencies, setSelectedCurrencies] = useState([]);
    const [yearsList, setYearsList] = useState([]);
    const [selectedYear, setSelectedYear] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const { options, error : optionsError } = useOptions("currencyrates");
    const { history, historyError } = useHistory("currencyrates", selectedYear);

    const totalPages = Math.ceil((history?.length || 0) / PAGE_SIZE);
    const firstRecordIndex = (currentPage - 1) * PAGE_SIZE;
    const visibleHistory = history?.slice(
        firstRecordIndex,
        firstRecordIndex + PAGE_SIZE
    ) || [];


    useEffect(() => {
        document.title = "Currency Rates";

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

        // Fetch plot options
        GetPlotOptions()
            .then(plotOptionsData => {
                setPlotOptions(plotOptionsData);
            })
            .catch(error => {
                setError('Failed to load plot options: ' + error.message);
                console.error('Error loading plot options:', error);
            });

        // Fetch initial plot
        GetPlot()
            .then(plotUrl => {
                setImageUrl(plotUrl);
            })
            .catch(error => {
                setError('Failed to load initial plot: ' + error.message);
                console.error('Error loading initial plot:', error);
            });
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

        // If both options and history are loaded, set loading to false
        if (options !== null && history !== null) {
            setLoading(false);
        }

        setCurrentPage(1);
    }, [optionsError, historyError, selectedYear, options, history]);

    const GetPlotOptions = () => {
        return fetch(`/api/get/list/currrateplotnames`)
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
                    return data.cuurrateplotnames;
                } else {
                    throw new Error(data.message || 'Failed to load plot options');
                }
            })
            .catch(error => {
                console.error('Error fetching plot options:', error);
                alert('Unexpected error occurred while fetching plot options: ' + error.message);
                throw error;
            });
    }

    const GetPlot = () => {
        const filters = selectedCurrencies.length > 0 ? selectedCurrencies.join("|") : "None";

        return fetch(`/api/get/plot/currencyrates/${filters}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
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
                    return data.plot;
                } else {
                    throw new Error(data.message || 'Failed to load plot');
                }
            })
            .catch(error => {
                console.error('Error fetching plot:', error);
                alert('Unexpected error occurred while fetching plot: ' + error.message);
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

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        const key = name.replace('input', '');
        setFormData(prevData => ({
            ...prevData,
            [key.charAt(0).toLowerCase() + key.slice(1)]: value
        }));
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
        resetForm();
    };

    function getPageItems(currentPage, totalPages) {
        if (totalPages <= 7) {
            return Array.from({ length: totalPages }, (_, index) => index + 1);
        }

        const visiblePages = new Set([
            1,
            2,
            currentPage - 1,
            currentPage,
            currentPage + 1,
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

    const OnYearChange = (event) => {
        const selectedYear = event.target.value;
        setSelectedYear(selectedYear);
    }

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
            currency_M: cells[2].innerText,
            currency_S: cells[3].innerText,
            rate: cells[4].innerText,
            isReverse: false
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
        fetch(`/api/edit/currencyrates/${editingId}`, {
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

    const onFilterChange = (currency, isChecked) => {
        if (isChecked) {
            setSelectedCurrencies(prev => [...prev, currency]);
        } else {
            setSelectedCurrencies(prev => prev.filter(c => c !== currency));
        }
    }

    const FetchFilteredPlot = (e) => {
        e.preventDefault();

        GetPlot()
            .then(plotUrl => {
                setImageUrl(plotUrl);
            })
            .catch(error => {
                console.error('Error fetching filtered plot:', error);
                alert('Unexpected error occurred while fetching filtered plot: ' + error.message);
            });
    }

    if (loading) {
        return (
            <>
                <Header />
                <div className="currency-rates-page">
                    <h1>Currency Rates</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="currency-rates-page">
                    <h1>Currency Rates</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        <>
            <Header />
            <div className="currency-rates-page container-fluid">
                <h1>Currency Rates</h1>
                <Row>
                    {options && (<Forms options={options}
                        DeleteRecord={DeleteRecord}
                        handleInputChange={handleInputChange}
                        resetForm={resetForm}
                        editMode={editMode}
                        editingId={editingId}
                        formData={formData}
                        deleteConfirm={deleteConfirm}
                    />)}
                </Row>
                <br />
                <Row>
                    <Col md={4}>
                        <h3>Currency Rates History</h3>
                        
                        <Col md={3}>
                            <YearSelectorOnChange
                                yearsList={yearsList}
                                selectedYear={selectedYear}
                                onYearChange={OnYearChange}
                                id="currency-rates-year-selector"
                            />
                        </Col>
                        <br/>
                        <div className="table-responsive">
                            {history && (
                                <> <HistoryTableWithEdit
                                    columns={["ID", "Date", "Currency Sell", "Currency Buy", "Rate"]}
                                    data={visibleHistory}
                                    tableId="CurrRateHistoryTable"
                                    EditRecord={EditRecord}
                                    numberColumns={["4-4"]}
                                />

                                    {totalPages > 1 && editMode !== true && (
                                        <Pagination aria-label="CurrencyRates history pages"
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
                        </div>
                    </Col>
                    <Col md={8}>
                        {(imageUrl && options && <PlotComponent
                            currencyList={plotOptions}
                            onFilterChange={onFilterChange}
                            FetchFilteredPlot={FetchFilteredPlot}
                            imageUrl={imageUrl}
                        />)}
                    </Col>
                </Row>
            </div>
        </>
    );
}
