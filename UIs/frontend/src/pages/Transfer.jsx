import { useEffect } from "react";
import { HistoryTableWithEdit } from "../commonComponents/Common";

function ValidateForm(isAdvanced, Edit = false, id = null) {
    let FormObject;
    let formData;
    let endpoint;

    if (!isAdvanced) {
        const form = document.getElementById("FormStandard");
        formData = new FormData(form);
    } else {
        const form = document.getElementById("FormAdvanced");
        formData = new FormData(form);
    }

    FormObject = Object.fromEntries(formData.entries());

    if (!isAdvanced) {
        if (FormObject.Date === "" || FormObject.Sender === "" || FormObject.Receiver === "" || FormObject.Sum === "" || FormObject.Currency === "") {
            alert("Please fill in all fields.");
            return false;
        }

        if (isNaN(parseFloat(FormObject.Sum)) || parseFloat(FormObject.Sum) <= 0) {
            alert("Please enter a valid sum.");
            return false;
        }

    } else {
        if (FormObject.Date === "" || FormObject.Sender === "" || FormObject.SSum === "" || FormObject.SCurrency === "" || FormObject.Receiver === "" || FormObject.RSum === "" || FormObject.RCurrency === "") {
            alert("Please fill in all fields.");
            return false;
        }

        if (isNaN(parseFloat(FormObject.SSum)) || parseFloat(FormObject.SSum) <= 0 || isNaN(parseFloat(FormObject.RSum)) || parseFloat(FormObject.RSum) <= 0) {
            alert("Please enter valid sums.");
            return false;
        }

        if (FormObject.SCurrency === FormObject.RCurrency) {
            alert("Sender and Receiver currencies cannot be the same. Use standard transfer instead.");
            return false;
        }

        if (parseFloat(FormObject.CurrencyRate) <= 0) {
            alert("Please enter a valid currency rate.");
            return false;
        }
    }

    if (FormObject.Sender === FormObject.Receiver) {
        alert("Sender and Receiver cannot be the same.");
        return false;
    }

    // Append transfer type to the FormObject
    FormObject.transferType = isAdvanced ? 'advanced' : 'standard';

    if (!Edit) {
        endpoint = '/add/transfer';
    } else {
        endpoint = '/edit/transfer/' + id;
    }

    // Send POST request
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(FormObject)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert('Error: ' + (data.message || 'Failed to add transfer'));
            }
        })
        .catch(error => {
            console.error('Unexpected error:', error);
            alert('Unexpected error occurred');
        });
}

function GetOptions() {
    return fetch('http://localhost:5050/api/get/options/transfer')
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

function GetHistory(type) {
    let endpoint;
    if (type === 'standard') {
        endpoint = 'http://localhost:5050/api/get/history/transfer'
    } else {
        endpoint = 'http://localhost:5050/api/get/history/transferADV'
    }
    return fetch(endpoint)
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

function StandardTransferForm({ options }) {
    return (
        <form action="/transfer" method="post" id="FormStandard" onsubmit="ValidateTransfer(isAdvanced = false)">
            <table>
                <tr>
                    <th>Date</th>
                    <th>Sender</th>
                    <th>Receiver</th>
                    <th>Sum</th>
                    <th>Currency</th>
                    <th>Comment</th>
                </tr>
                <tr>
                    <td class="fields_big"><input type="date" id="Date" name="Date" class="standardWidth" /></td>
                    <td class="fields_big">
                        <select id="Sender" name="Sender" class="standardWidth">
                            <option value="" disabled selected></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </select>
                    </td>
                    <td class="fields_big">
                        <select id="Receiver" name="Receiver" class="standardWidth">
                            <option value="" disabled selected></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </select>
                    </td>
                    <td class="fields_small"><input type="text" id="Sum" name="Sum" autocomplete="off" class="standardWidth" />
                    </td>
                    <td class="fields_small">
                        <select id="Currency" name="Currency" class="standardWidth">
                            <option value="" disabled selected></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </select>
                    </td>
                    <td class="fields_comment"><input type="text" id="Comment" name="Comment" autocomplete="off"
                        class="standardWidth" /></td>
                </tr>
            </table><br />
            <input type="submit" value="Add" class="submitrec" />
        </form>
    )
};

function AdvancedTransferForm({ options }) {
    return (
        <form action="/transfer" method="post" id="FormAdvanced" onsubmit="ValidateTransfer(isAdvanced = true)">
            <table>
                <tr>
                    <th>Date</th>
                    <th>Sender</th>
                    <th>Sum</th>
                    <th>Currency</th>
                    <th>Receiver</th>
                    <th>Sum</th>
                    <th>Currency</th>
                    <th>Currency Rate</th>
                    <th>Comment</th>
                </tr>
                <tr>
                    <td class="fields_big"><input type="date" id="ADVDate" name="Date" class="standardWidth" /></td>
                    <td class="fields">
                        <select id="ADVSender" name="Sender" class="standardWidth">
                            <option value="" disabled selected></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </select>
                    </td>
                    <td class="fields_small"><input type="text" id="ADVSSum" name="SSum" class="standardWidth" autocomplete="off" /></td>
                    <td class="fields_big">
                        <select id="ADVSCurrency" name="SCurrency" class="standardWidth">
                            <option value="" disabled selected></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </select>
                    </td>
                    <td class="fields_big">
                        <select id="ADVReceiver" name="Receiver" class="standardWidth">
                            <option value="" disabled selected></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </select>
                    </td>
                    <td class="fields_small"><input type="text" id="ADVRSum" name="RSum" autocomplete="off"
                        class="standardWidth" /></td>
                    <td class="fields_small">
                        <select id="ADVRCurrency" name="RCurrency" class="standardWidth">
                            <option value="" disabled selected></option>
                            {options.pb.map((pb, index) => (
                                <option value={pb} key={index}>{pb}</option>
                            ))}
                        </select>
                    </td>
                    <td class="fields_small">
                        <input type="text" id="ADVCurrencyRate" name="Currency rate" autocomplete="off" class="standardWidth" />
                    </td>
                    <td class="fields_comment"><input type="text" id="ADVComment" name="Comment" autocomplete="off"
                        class="standardWidth" /></td>
                </tr>
            </table><br />
            <input type="submit" value="Add" class="submitrec" />
        </form>
    )
};

function Forms({ options }) {
    return (
        <div className="forms">
            <h2>Standard Transfer</h2>
            <StandardTransferForm options={options} />
            <br />
            <h2>Advanced Transfer</h2>
            <AdvancedTransferForm options={options} />
        </div>
    );
}

export default function TransferPage() {
    useEffect(() => {
        document.title = "Transfer Records";
    }, []);

    const EditRecord = (element) => {       // TODO: Implement Edit functionality
        const row = element.target.parentNode;
        const cells = row.getElementsByTagName("td");
        const id = cells[0].innerText;

        // Populate form fields with the data from the selected row
        document.getElementById("Date").value = cells[1].innerText;
        document.getElementById("Category").value = cells[2].innerText;
        document.getElementById("Person-Bank").value = cells[3].innerText;
        document.getElementById("Sum").value = parseFloat(cells[4].innerText).toFixed(2);
        document.getElementById("Currency").value = cells[5].innerText;
        document.getElementById("Comment").value = cells[6].innerText;

        const form = document.getElementById("form");
        form.setAttribute("onsubmit", `ValidateForm(true, ${id});`);
    }

    // TODO: Implement History for Transfer
    return (
        <div className="income-page">
            <h1>Income Records</h1>
            <Forms options={GetOptions()} />
            <br />
            <h3>History</h3>
            <br />
            <HistoryTableWithEdit
                columns={["ID", "Date", "Category", "Sub-category", "Person-Bank", "Sum", "Currency", "Comment"]}
                data={GetHistory()} />
        </div>
    )

}
