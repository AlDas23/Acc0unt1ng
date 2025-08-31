import { memo } from 'react';

function TableBody({ data, EditRecord }) {
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
                            {cell}
                        </td>
                    ))}
                </tr>
            ))}
        </tbody>
    );
}

export const HistoryTable = memo(function HistoryTable({ columns, data, tableId }) {
    return (
        <table className="history-table table-bordered" id={tableId || undefined}>
            <thead>
                <tr>
                    {columns.map((col, index) => (
                        <th className="ht-cell" key={`col-${index}`}>{col}</th>
                    ))}
                </tr>
            </thead>
            <TableBody data={data} />
        </table>
    );
});

export const HistoryTableWithEdit = memo(function HistoryTableWithEdit({ columns, data, EditRecord, tableId }) {
    return (
        <table className="history-table table-bordered"  id={tableId || undefined}>
            <thead>
                <tr>
                    {columns.map((col, index) => (
                        <th className="ht-cell" key={`col-${index}`}>{col}</th>
                    ))}
                </tr>
            </thead>
            <TableBody data={data} EditRecord={EditRecord} />
        </table>
    );
});
