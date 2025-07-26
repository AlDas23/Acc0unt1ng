function TableBody({ data, EditRecord }) {
    return (
        <tbody>
            {data.map((row, rowIndex) => (
                <tr key={`row-${rowIndex}`}>
                    {row.map((cell, cellIndex) => (
                        <td
                            className="ht-cell"
                            key={`cell-${rowIndex}-${cellIndex}`}
                            {...(EditRecord && cellIndex === 0 ? { onClick: () => EditRecord(row[0]) } : {})}
                        >
                            {cell}
                        </td>
                    ))}
                </tr>
            ))}
        </tbody>
    );
}

export function HistoryTable({ columns, data }) {
    return (
        <table className="history-table">
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
}

export function HistoryTableWithEdit({ columns, data, EditRecord }) {
    return (
        <table className="history-table">
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
}