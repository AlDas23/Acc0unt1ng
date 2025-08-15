import { useEffect } from "react";
import { HistoryTable } from "../commonComponents/Common";

function ValidateForm() {
    const date_in = document.getElementById("DateIn").value;
    const name = document.getElementById("Name").value;
    const owner = document.getElementById("Owner").value;
    const sum = document.getElementById("Sum").value;
    const curr = document.getElementById("Currency").value;
    const months = document.getElementById("Months").value;
    const date_out = document.getElementById("DateOut").value;
    const percent = document.getElementById("Percent").value;
    const curr_rate = document.getElementById("CurrencyRate").value;
    const comment = document.getElementById("Comment").value;

    if (date_in === "" || name === "" || owner === "" || isNaN(sum) || curr === "" || date_out === "") {
        alert("Please fill in all reqired fields.\n Deposit date, name, owner, sum, currency, percent are required.");
        return false;
    }

    if (isNaN(sum) || sum <= 0) {
        alert("Please enter a valid sum.");
        return false;
    }

    if (months !== "" && (isNaN(months) || months <= 0)) {
        alert("Please enter a valid number of months.");
        return false;
    }

    if (isNaN(percent) || percent < 0 || percent > 100) {
        alert("Please enter a valid percent.");
        return false;
    }

    if (curr_rate !== "" && (isNaN(curr_rate) || curr_rate <= 0)) {
        alert("Please enter a valid currency rate.");
        return false;
    }

    const FormData = {
        dateIn: date_in,
        name: name,
        owner: owner,
        sum: parseFloat(sum).toFixed(2),
        currency: curr,
        months: months ? parseFloat(months).toFixed(0) : " ",
        dateOut: date_out,
        percent: parseFloat(percent).toFixed(2),
        currencyRate: curr_rate ? parseFloat(curr_rate).toFixed(2) : " ",
        comment: comment
    };

    // Send POST request
    fetch('http://localhost:5050/api/add/deposit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(FormData)
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
}

function GetOptions() {
    return fetch('http://localhost:5050/api/get/options/deposit')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
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

function GetHistory(isActive) {
    if (isActive) {
        return fetch('http://localhost:5050/api/get/history/depositO')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
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
    } else {
        return fetch('http://localhost:5050/api/get/history/depositC')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
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
}

function Forms({ options }) {
    return (
        <div>
            <form className="forms" id="form" onSubmit={ValidateForm()}>
                <table>
                    <tr>
                        <th>Deposit Date</th>
                        <th>Name</th>
                        <th>Person-bank</th>
                        <th>Sum</th>
                        <th>Currency</th>
                        <th>Months</th>
                        <th>Closing Date</th>
                        <th>%</th>
                        <th>Currency rate</th>
                        <th>Comment</th>
                    </tr>
                    <tr>
                        <td class="fields_big">
                            <input type="date" id="DateIn" name="DateIn" class="standardWidth" />
                        </td>
                        <td class="fields_big">
                            <input type="text" id="Name" name="Name" autocomplete="off" class="standardWidth" />
                        </td>
                        <td class="fields_small">
                            <select id="Owner" name="Owner" class="standardWidth">
                                <option value="" disabled selected></option>
                                {options.pb.map((pb, index) => (
                                    <option value={pb} key={index}>{pb}</option>
                                ))}
                            </select>
                        </td>
                        <td class="fields_small">
                            <input type="text" id="Sum" name="Sum" autocomplete="off" class="standardWidth" />
                        </td>
                        <td class="fields_small">
                            <select id="Currency" name="Currency" class="standardWidth">
                                <option value="" disabled selected></option>
                                {options.currency.map((currency, index) => (
                                    <option value={currency} key={index}>{currency}</option>
                                ))}
                            </select>
                        </td>
                        <td class="fields_small">
                            <input type="text" id="Months" name="Months" autocomplete="off" class="standardWidth" />
                        </td>
                        <td class="fields_big">
                            <input type="date" id="DateOut" name="DateOut" class="standardWidth" />
                        </td>
                        <td class="fields_small">
                            <input type="text" id="Percent" name="Percent" class="standardWidth" autocomplete="off" />
                        </td>
                        <td class="fields_small">
                            <input type="text" id="CurrencyRate" name="Currency rate" autocomplete="off" class="standardWidth" />
                        </td>
                        <td class="fields_comment">
                            <input type="text" id="Comment" name="Comment" autocomplete="off" class="standardWidth" />
                        </td>
                    </tr>
                </table><br />
                <input type="submit" value="Add" id="submitButton" class="submitrec" />
            </form>
        </div>
    );
}

export default function DepositPage() {
    useEffect(() => {
        document.title = "Deposit Records";
    }, []);


    return (
        <div className="deposit-page">
            <h1>Deposit Records</h1>
            <Forms options={GetOptions()} />
            <br />
            <div className="history-table-container">
                <div className="history-table-deposits-active">
                    <h3>Active deposits</h3>
                    <HistoryTable
                        columns={["Deposit Date", "Name", "Person-bank", "Sum", "Currency", "Months", "Closing Date", "%", "Currency rate", "Comment"]}
                        data={GetHistory(true)}
                    />
                </div>
                <br />
                <div className="history-table-deposits-closed">
                    <HistoryTable
                        columns={["Deposit Date", "Name", "Person-bank", "Sum", "Currency", "Months", "Closing Date", "%", "Currency rate", "Comment"]}
                        data={GetHistory(false)}
                    />
                </div>
            </div>
        </div>
    )

}
