import { useEffect, useState } from "react";
import { HistoryTable } from "../commonComponents/Common";
import { useIsMobile } from "../commonComponents/CustomHooks";
import Header from "../commonComponents/Header";
import AccordionHeader from "react-bootstrap/esm/AccordionHeader";
import Accordion from 'react-bootstrap/Accordion';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import "../assets/styles/BalancePageStyles.css";

function FilterBalance({ options, filters, handleFilterChange }) {
    return (
        <Row>
            <Col md={6} xs={12}>
                <label htmlFor="owner-filter">Filter by Owner:</label>
                <select
                    id="owner-filter"
                    name="owner"
                    onChange={handleFilterChange}
                    value={filters.owner}
                >
                    <option value="None">None</option>
                    {options.owner.map((owner, index) => (
                        <option value={owner} key={index}>
                            {owner}
                        </option>
                    ))}
                </select>
            </Col>
            <Col md={6} xs={12}>
                <label htmlFor="type-filter">Filter by Type:</label>
                <select
                    id="type-filter"
                    name="type"
                    onChange={handleFilterChange}
                    value={filters.type}
                >
                    <option value="None">None</option>
                    {options.type.map((type, index) => (
                        <option value={type} key={index}>
                            {type}
                        </option>
                    ))}
                </select>
            </Col>
        </Row>)
};

export default function BalancePage() {
    const [balanceData, setBalanceData] = useState([]);
    const [filters, setFilters] = useState({ owner: "None", type: "None" });
    const [options, setOptions] = useState(null);
    const [groupedData, setGroupedData] = useState({ currTable: [], ownerTable: [], typeTable: [], currTypeTable: [] });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const isMobile = useIsMobile(768);

    // Fetch initial data and options
    useEffect(() => {
        document.title = "Balance Sheet";

        GetOptions()
            .then(optionsData => {
                setOptions(optionsData);
            })
            .catch(error => {
                setError('Failed to load options: ' + error.message);
                console.error('Error loading options:', error);
            });


        // Create a mapping of table names to their state keys
        const tableMapping = {
            'curr-table': 'currTable',
            'owner-table': 'ownerTable',
            'type-table': 'typeTable',
            'curr-type-table': 'currTypeTable'
        };

        // Get balance data
        GetData("balance")
            .then(data => {
                setBalanceData(data);
            })
            .catch(error => {
                setError('Failed to load balance data: ' + error.message);
                console.error('Error loading balance data:', error);
            });

        // Get all table data in parallel
        Promise.all(
            Object.keys(tableMapping).map(tableName =>
                GetData("standard", tableName)
                    .then(tableData => ({ [tableMapping[tableName]]: tableData }))
            )
        )
            .then(results => {
                const newGroupedData = results.reduce((acc, curr) => ({ ...acc, ...curr }), {});
                setGroupedData(newGroupedData);
                setLoading(false);
            })
            .catch(error => {
                setError('Failed to load table data: ' + error.message);
                console.error('Error loading table data:', error);
                setLoading(false);
            });
    }, []);

    // Fetch data whenever filters change
    useEffect(() => {
        GetData("balance")
            .then(data => {
                setBalanceData(data);
            })
            .catch(error => {
                setError('Failed to load filtered balance data: ' + error.message);
                console.error('Error loading filtered balance data:', error);
            });
    }, [filters]);

    // Fetch data based on mode
    const GetData = (mode, table = null) => {
        const endpointStandard = `/api/get/balance/tables`;
        const endpointBalance = `/api/get/balance/balance`;

        if (mode === "standard") {
            return fetch(endpointStandard, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ table: table }),
            })
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
                        return data.table;
                    } else {
                        throw new Error(data.message || 'Failed to load table data');
                    }
                })
                .catch(error => {
                    console.error('Error fetching options:', error);
                    alert('Unexpected error occurred while fetching options: ' + error.message);
                    throw error;
                });

        } else if (mode === "balance") {
            return fetch(endpointBalance, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(filters),
            })
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
                        return data.data;
                    } else {
                        throw new Error(data.message || 'Failed to load balance data');
                    }
                })
                .catch(error => {
                    console.error('Error fetching options:', error);
                    alert('Unexpected error occurred while fetching options: ' + error.message);
                    throw error;
                });
        }
    };

    // Fetch filter options
    const GetOptions = () => {
        return fetch("/api/get/options/balance")
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
    };

    // Handle filter changes
    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters((prevFilters) => ({
            ...prevFilters,
            [name]: value,
        }));
    };


    // const toggleTable = (id) => {
    //     const table = document.getElementById(id);
    //     if (table) {
    //         table.style.display = table.style.display === "none" ? "table" : "none";
    //     }
    // };

    if (loading) {
        return (
            <>
                <Header />
                <div className="balance-page">
                    <h1>Balance Sheet</h1>
                    <p>Loading...</p>
                </div>
            </>
        );
    }

    if (error) {
        return (
            <>
                <Header />
                <div className="balance-page">
                    <h1>Balance Sheet</h1>
                    <p>Error: {error}</p>
                </div>
            </>
        );
    }

    return (
        // TODO: Apply Accordion to tables
        <>
            <Header />
            <div className="balance-page container-fluid">
                <h1>Balance Sheet</h1>
                <br />
                <Row>
                    <Col md={6}>
                        <Accordion defaultActiveKey="0">
                            <Accordion.Item eventKey="0">
                                <AccordionHeader>Balance Filter</AccordionHeader>
                                <Accordion.Body>
                                    {options && (<FilterBalance
                                        options={options}
                                        filters={filters}
                                        handleFilterChange={handleFilterChange}
                                    />)}
                                    <br />
                                    <div className="table-responsive">
                                        {balanceData && (<HistoryTable
                                            columns={["Person bank", "Currency", "Sum"]}
                                            data={balanceData}
                                            tableId="balance-table"
                                            numberColumns={["2-2"]}
                                        />)}
                                    </div>
                                </Accordion.Body>
                            </Accordion.Item>
                        </Accordion>
                    </Col>
                    <Col md={6}>
                        <Accordion defaultActiveKey={isMobile ? [] : ["0", "1", "2", "3"]} alwaysOpen={!isMobile}>
                            <Accordion.Item eventKey="0">
                                <Accordion.Header>Group by currency</Accordion.Header>
                                <Accordion.Body>
                                    <div className="table-responsive">
                                        {groupedData && (<HistoryTable
                                            columns={["Currency", "Sum", "in Main currency", "%"]}
                                            data={groupedData.currTable || []}
                                            tableId="curr-table"
                                            numberColumns={["1-2", "3-1"]}
                                        />)}
                                    </div>
                                </Accordion.Body>
                            </Accordion.Item>
                            <Accordion.Item eventKey="1">
                                <Accordion.Header>Group by owner</Accordion.Header>
                                <Accordion.Body>
                                    <div className="table-responsive">
                                        {groupedData && (<HistoryTable
                                            columns={["Owner", "Currency", "Sum", "in Main currency"]}
                                            data={groupedData.ownerTable || []}
                                            tableId="owner-table"
                                            numberColumns={["2-2"]}
                                        />)}
                                    </div>
                                </Accordion.Body>
                            </Accordion.Item>
                            <Accordion.Item eventKey="2">
                                <Accordion.Header>Group by Type</Accordion.Header>
                                <Accordion.Body>
                                    <div className="table-responsive">
                                        {groupedData && (<HistoryTable
                                            columns={["Type", "Sum in Main currency", "%"]}
                                            data={groupedData.typeTable || []}
                                            tableId="type-table"
                                            numberColumns={["2-1"]}
                                        />)}
                                    </div>
                                </Accordion.Body>
                            </Accordion.Item>
                            <Accordion.Item eventKey="3">
                                <Accordion.Header>Group by currency and type</Accordion.Header>
                                <Accordion.Body>
                                    <div className="table-responsive">
                                        {groupedData && (<HistoryTable
                                            columns={["Currency", "Type", "Sum", "%"]}
                                            data={groupedData.currTypeTable || []}
                                            tableId="curr-type-table"
                                            numberColumns={["2-2", "3-1"]}
                                        />)}
                                    </div>
                                </Accordion.Body>
                            </Accordion.Item>
                        </Accordion>
                    </Col>
                </Row>
            </div>
        </>
    );
}
