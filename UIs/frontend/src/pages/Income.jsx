import { useEffect } from "react";
import { HistoryTableWithEdit } from "../commonComponents/Common";

function ValidateForm(Edit = false, id = null) {
    const date = document.getElementById("Date").value;
    const cat = document.getElementById("Category").value;
    const pb = document.getElementById("Person-Bank").value;
    let sum = document.getElementById("Sum").value;
    const curr = document.getElementById("Currency").value;
    const comment = document.getElementById("Comment").value;

    let endpoint;

    if (date === "" || cat === "" || pb === "" || sum === "" || curr === "") {
        alert("Please fill in all fields.");
        return false;
    }

    if (isNaN(sum) || parseFloat(sum) <= 0) {
        alert("Please enter a valid sum.");
        return false;
    }

    const FormData = {
        date: date,
        category: cat,
        personBank: pb,
        sum: parseFloat(sum).toFixed(2),
        currency: curr,
        comment: comment
    };

    if (!Edit) {
        endpoint = 'http://localhost:5050/api/add/income';
    } else {
        endpoint = 'http://localhost:5050/api/edit/income/' + id;
    }

    // Send POST request
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(FormData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert('Error: ' + (data.message || 'Failed to add transaction'));
            }
        })
        .catch(error => {
            console.error('Unexpected error:', error);
            alert('Unexpected error occurred');
        });
}

function GetOptions() {
    return fetch('http://localhost:5050/api/get/options/income')
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

function GetHistory() {
    return fetch('http://localhost:5050/api/get/history/income')
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

function Forms({ options }) {
    return (
        <div>
            <form className="forms" id="form" onSubmit={ValidateForm()}>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Category</th>
                        <th>Person-Bank</th>
                        <th>Sum</th>
                        <th>Currency</th>
                        <th>Comment</th>
                    </tr>
                    <tr>
                        <td class="fields_big">
                            <input type="date" id="Date" name="Date" class="standardWidth" />
                        </td>
                        <td class="fields_big">
                            <select id="Category" name="Category" class="standardWidth">
                                <option value="" disabled selected></option>
                                {options.categories.map((category, index) => (
                                    <option value={category} key={index}>{category}</option>
                                ))}
                            </select>
                        </td>
                        <td class="fields_big">
                            <select id="Person-Bank" name="Person-Bank" class="standardWidth">
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

export default function IncomePage() {
    useEffect(() => {
        document.title = "Income Records";
    }, []);

    const EditRecord = (element) => {
        const row = element.target.parentNode;
        const cells = row.getElementsByTagName("td");
        const id = cells[0].innerText;

        const clickedRow = element.closest('tr');
        const rows = document.querySelectorAll('.history-table tbody tr');

        rows.forEach(row => {
            if (row !== clickedRow) {
                row.style.display = 'none';
            } else {
                row.style.display = ''; // Ensure the clicked row remains visible
            }
        });

        // Populate form fields with the data from the selected row
        document.getElementById("Date").value = cells[1].innerText;
        document.getElementById("Category").value = cells[2].innerText;
        document.getElementById("Person-Bank").value = cells[3].innerText;
        document.getElementById("Sum").value = parseFloat(cells[4].innerText).toFixed(2);
        document.getElementById("Currency").value = cells[5].innerText;
        document.getElementById("Comment").value = cells[6].innerText;

        const form = document.getElementById("form");
        form.setAttribute("onsubmit", `ValidateForm(true, ${id});`);

        const submitButton = document.getElementById("submitButton");
        submitButton.value = "Edit";
    }

    return (
        <div className="income-page">
            <h1>Income Records</h1>
            <Forms options={GetOptions()} />
            <br />
            <h3>History</h3>
            <br />
            <HistoryTableWithEdit
                columns={["ID", "Date", "Category", "Person-Bank", "Sum", "Currency", "Comment"]}
                data={GetHistory()} />
        </div>
    )

}
