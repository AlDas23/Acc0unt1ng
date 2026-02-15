import { memo } from 'react';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Button from "react-bootstrap/esm/Button";

function TableBody({ data, EditRecord, numberColumns = [] }) {
    // Parse number column settings
    const formatSettings = numberColumns.reduce((acc, setting) => {
        const [colIndex, decimals] = setting.split('-').map(Number);
        acc[colIndex] = decimals;
        return acc;
    }, {});

    return (
        <tbody>
            {data.map((row, rowIndex) => (
                <tr key={`row-${rowIndex}`}>
                    {row.map((cell, cellIndex) => (
                        <td
                            className={`ht-cell ${EditRecord && cellIndex === 0 ? 'editable-cell' : ''}`}
                            key={`cell-${rowIndex}-${cellIndex}`}
                            {...(EditRecord && cellIndex === 0 ? { onClick: (e) => EditRecord(e) } : {})}
                        >
                            {cellIndex in formatSettings && !isNaN(cell)
                                ? Number(cell).toFixed(formatSettings[cellIndex])
                                : cell}
                        </td>
                    ))}
                </tr>
            ))}
        </tbody>
    );
}

export const HistoryTable = memo(function HistoryTable({ columns, data, tableId, numberColumns }) {
    return (
        <table className="history-table table-bordered" id={tableId || undefined}>
            <thead>
                <tr>
                    {columns.map((col, index) => (
                        <th className="ht-cell" key={`col-${index}`}>{col}</th>
                    ))}
                </tr>
            </thead>
            <TableBody data={data} numberColumns={numberColumns} />
        </table>
    );
});

export const HistoryTableWithEdit = memo(function HistoryTableWithEdit({ columns, data, EditRecord, tableId, numberColumns }) {
    return (
        <table className="history-table table-bordered" id={tableId || undefined}>
            <thead>
                <tr>
                    {columns.map((col, index) => (
                        <th className="ht-cell" key={`col-${index}`}>{col}</th>
                    ))}
                </tr>
            </thead>
            <TableBody data={data} EditRecord={EditRecord} numberColumns={numberColumns} />
        </table>
    );
});

export function YearSelector({ yearsList, selectedYear, onYearSubmit, id }) {
    return (
        <Form noValidate className="year-select" id={id} onSubmit={onYearSubmit}>
            <Row>
                <Form.Select id="yearSelect" name="YearSelect" defaultValue={selectedYear}>
                    {yearsList.map((year, index) => (
                        <option value={year} key={index}>{year}</option>
                    ))}
                </Form.Select>
            </Row>
            <Row>
                <Button type="submit" variant="primary">Load Year</Button>
            </Row>
        </Form>
    )
}

export function YearSelectorOnChange({ yearsList, selectedYear, onYearChange, id }) {
    return (
        <Form noValidate className="year-select" id={id}>
            <Form.Select id="yearSelect" name="YearSelect" defaultValue={selectedYear} onChange={onYearChange}>
                {yearsList.map((year, index) => (
                    <option value={year} key={index}>{year}</option>
                ))}
            </Form.Select>
        </Form>
    )
}

export const CheckLegacy = () => {
    return fetch(`/api/database/status`)
        .then(response => response.json())
        .then(data => data.legacy || false)
        .catch(error => {
            console.error('Error fetching db status:', error);
            alert('Unexpected error occurred while fetching db status: ' + error.message);
            throw error;
        });
};

export const MobileViewUnAvailableModal = ({ props }) => {
    return (
        <Modal {...props} size='lg' aria-labelledby="contained-modal-title-vcenter"
            centered>
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Mobile view is unavailable
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <p>
                    The mobile version for this page is unavailable. Please consider using desktop version.
                </p>
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={props.onHide}>I understand</Button>
            </Modal.Footer>
        </Modal>
    )
}
