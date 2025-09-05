import { memo } from 'react';

export const backendURL = "backend-service:5050";

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