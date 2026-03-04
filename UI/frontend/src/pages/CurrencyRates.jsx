import { useEffect, useState } from "react";
import { HistoryTableWithEdit } from "../commonComponents/Common";
import Header from "../commonComponents/Header";
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import '../assets/styles/CurrRatePageStyles.css'
import { CheckLegacy } from '../commonComponents/Common'
import OverlayTrigger from "react-bootstrap/esm/OverlayTrigger";
import Tooltip from 'react-bootstrap/Tooltip';

const initialFormData = {
    date: new Date().toISOString().split('T')[0],
    currency_M: "",
    currency_S: "",
    rate: "",
    isReverse: false
};

function LegacyPlotComponent({ imageUrl }) {
    return (
        <>
            <h3>Currency dynamics plot</h3>
            <img id="CurrRatePlot" src={imageUrl} alt="Currency dynamics plot" />
        </>
    );
}

function FormsLegacy({ options }) {
    return (
        <Form noValidate className="form" id="form" onSubmit={(e) => {
            e.preventDefault();

            const form = e.target;
            const formDataObj = new FormData(form);
            const formObject = Object.fromEntries(formDataObj.entries());

            if (formObject.currency === "") {
                alert("Currency cannot be empty!")
                return false;
            }

            if (isNaN(formObject.Rate) || formObject.Rate <= 0) {
                alert("Rate is not a number!")
                return false;
            }

            // Send POST request
            fetch("/api/add/currencyrates", {
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
                        alert('Error: ' + (data.message || 'Failed to add currency rate'));
                    }
                })
                .catch(error => {
                    console.error('Unexpected error:', error);
                    alert('Unexpected error occurred');
                });
        }}>
            <Row>
                <Col xl="2">
                    <Form.Label htmlFor="inputDate">
                        Date
                    </Form.Label>
                    <input type="date" id="inputDate" name="Date" defaultValue={new Date().toISOString().split('T')[0]} />
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputCurrency">
                        Currency
                    </Form.Label>
                    <Form.Select id="inputCurrency" name="Currency" defaultValue={""}>
                        <option value="" disabled></option>
                        {options.currency.map((currency, index) => (
                            <option value={currency} key={index}>{currency}</option>
                        ))}
                    </Form.Select>
                </Col>
                <Col xl="2">
                    <Form.Label htmlFor="inputRate">
                        Rate
                    </Form.Label>
                    <Form.Control type="text" id="inputRate" name="Rate" autoComplete="off" />
                </Col>
            </Row>
            <Row>
                <Button type="submit" value="Submit" id="SubmitButton">Submit</Button>
            </Row>
        </Form>
    );
};

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
    const [options, setOptions] = useState(null);
    const [formData, setFormData] = useState(initialFormData);
    const [editMode, setEditMode] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [deleteConfirm, setDeleteConfirm] = useState(false);
    const [plotOptions, setPlotOptions] = useState(null);
    const [history, setHistory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [isLegacy, setIsLegacy] = useState(null);
    const [selectedCurrencies, setSelectedCurrencies] = useState([]);

    useEffect(() => {
        document.title = "Currency Rates";

        const initializeApp = async () => {
            try {
                // Check if DB is legacy
                const isLegacyResult = await CheckLegacy();
                if (isLegacyResult) {
                    console.info("Legacy DB schema used! Switching to legacy mode");
                    setIsLegacy(true);
                } else {
                    setIsLegacy(false);
                }

                const promises = [
                    GetOptions(),
                    GetHistory(),
                    GetPlot()
                ];

                // Only add GetPlotOptions if not legacy
                if (!isLegacyResult) {
                    promises.push(GetPlotOptions());
                }

                const results = await Promise.all(promises);

                const [optionsData, historyData, plotUrl] = results;
                const plotOptions = !isLegacyResult ? results[3] : null;

                setOptions(optionsData);
                setHistory(historyData);
                setImageUrl(plotUrl);
                if (!isLegacyResult) {
                    setPlotOptions(plotOptions);
                }
                setLoading(false);

            } catch (error) {
                setError('Failed to initialize page: ' + error.message);
                setLoading(false);
                console.error('Error initializing page:', error);
            }
        };

        initializeApp();
    }, []);


    const GetOptions = () => {
        return fetch(`/api/get/options/currencyrates`)
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

    const GetHistory = () => {
        return fetch(`/api/get/history/currencyrates`)
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

    const GetPlot = () => {
        if (isLegacy) {
            return fetch(`/api/get/plot/currencyrates`)
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
        } else {
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
                    {options && (isLegacy ? (<FormsLegacy
                        options={options}
                    />) : (<Forms options={options}
                        DeleteRecord={DeleteRecord}
                        handleInputChange={handleInputChange}
                        resetForm={resetForm}
                        editMode={editMode}
                        editingId={editingId}
                        formData={formData}
                        deleteConfirm={deleteConfirm}
                    />))}
                </Row>
                <br />
                <Row>
                    <Col md={4}>
                        <h3>Currency Rates History</h3>
                        <div className="table-responsive">
                            {history && (<HistoryTableWithEdit
                                columns={isLegacy ?
                                    ["Date", "Currency", "Rate"]
                                    : ["ID", "Date", "Currency Sell", "Currency Buy", "Rate"]}
                                data={history}
                                tableId="CurrRateHistoryTable"
                                EditRecord={EditRecord}
                                numberColumns={isLegacy ? ["2-4"] : ["4-4"]}
                            />)}
                        </div>
                    </Col>
                    <Col md={8}>
                        {isLegacy ? (imageUrl && <LegacyPlotComponent imageUrl={imageUrl} />)
                            : (imageUrl && options && <PlotComponent
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
