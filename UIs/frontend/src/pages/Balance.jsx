import { useEffect, useState } from "react";
import { HistoryTable } from "../commonComponents/Common";
import Header from "../commonComponents/Header";

export default function BalancePage() {
    const [data, setData] = useState([]);
    const [filters, setFilters] = useState({ owner: "None", type: "None" });
    const [options, setOptions] = useState({ owner: [], type: [] });
    const [groupedData, setGroupedData] = useState({});

    // Fetch data based on mode
    const GetData = (mode, table = null) => {
        const endpointStandard = `http://localhost:5050/api/get/balance/tables`;
        const endpointBalance = `http://localhost:5050/api/get/balance/balance`;

        if (mode === "standard") {
            return fetch(endpointStandard, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(table),
            })
                .then((response) => response.json())
                .then((data) =>
                    setGroupedData((prev) => ({
                        ...prev,
                        [table]: data,
                    }))
                )
                .catch((error) => console.error("Error fetching data:", error));
        } else if (mode === "balance") {
            return fetch(endpointBalance, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(filters),
            })
                .then((response) => response.json())
                .then((data) => setData(data))
                .catch((error) => console.error("Error fetching data:", error));
        }
    };

    // Fetch filter options
    const GetOptions = () => {
        fetch("http://localhost:5050/api/get/options/balance")
            .then((response) => response.json())
            .then((data) => setOptions({ owner: data.owner, type: data.type }))
            .catch((error) => console.error("Error fetching options:", error));
    };

    // Handle filter changes
    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters((prevFilters) => ({
            ...prevFilters,
            [name]: value,
        }));
    };

    // Fetch initial data and options
    useEffect(() => {
        document.title = "Balance Sheet";
        GetOptions();
        GetData("balance");
        ["curr-table", "owner-table", "type-table", "curr-type-table"].forEach((table) =>
            GetData("standard", table)
        );
    }, []);

    // Fetch data whenever filters change
    useEffect(() => {
        GetData("balance");
    }, [filters]);


    const FilterBalance = () => (
        <>
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
        </>
    );

    const toggleTable = (id) => {
        const table = document.getElementById(id);
        if (table) {
            table.style.display = table.style.display === "none" ? "table" : "none";
        }
    };

    return (
        <>
            <Header />
            <div className="balance-page">
                <div className="info-tables">
                    <h2 onClick={() => toggleTable("curr-table")}>Group by currency</h2>
                    <br />
                    <HistoryTable
                        columns={["Currency", "Sum", "Sum RON", "%"]}
                        data={groupedData["curr-table"] || []}
                        tableId="curr-table"
                    />
                    <br />
                    <h2 onClick={() => toggleTable("owner-table")}>Group by Owner</h2>
                    <br />
                    <HistoryTable
                        columns={["Owner", "Currency", "Sum", "Sum RON"]}
                        data={groupedData["owner-table"] || []}
                        tableId="owner-table"
                    />
                    <br />
                    <h2 onClick={() => toggleTable("type-table")}>Group by Type</h2>
                    <br />
                    <HistoryTable
                        columns={["Type", "Sum RON", "%"]}
                        data={groupedData["type-table"] || []}
                        tableId="type-table"
                    />
                    <br />
                    <h2 onClick={() => toggleTable("curr-type-table")}>
                        Group by currency and type
                    </h2>
                    <br />
                    <HistoryTable
                        columns={["Currency", "Type", "Sum", "%"]}
                        data={groupedData["curr-type-table"] || []}
                        tableId="curr-type-table"
                    />
                </div>
                <div className="balance-content">
                    <h2>Balance Sheet</h2>
                    <br />
                    <FilterBalance />
                    <br />
                    <HistoryTable
                        columns={["Person bank", "Currency", "Sum"]}
                        data={data}
                        tableId="balance-table"
                    />
                </div>
            </div>
        </>
    );
}
