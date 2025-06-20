function ValidateExp(Edit = false, id = null) {
    const date = document.getElementById("Date").value;
    const cat = document.getElementById("Category").value;
    const subCat = document.getElementById("Sub-category").value;
    const pb = document.getElementById("Person-Bank").value;
    let sum = document.getElementById("Sum").value;
    const curr = document.getElementById("Currency").value;
    const comment = document.getElementById("Comment").value;

    let endpoint;

    if (date === "" || cat === "" || subCat === "" || pb === "" || sum === "" || curr === "") {
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
        subCategory: subCat,
        personBank: pb,
        sum: parseFloat(-sum).toFixed(2),
        currency: curr,
        comment: comment
    };

    if (!Edit) {
        endpoint = '/add/expense';
    } else {
        endpoint = '/edit/expense/' + id;
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

function ValidateInc(Edit = false, id = null) {
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
        subCategory: " ",
        personBank: pb,
        sum: parseFloat(sum).toFixed(2),
        currency: curr,
        comment: comment
    };

    if (!Edit) {
        endpoint = '/add/income';
    } else {
        endpoint = '/edit/income/' + id;
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

function ValidateTransfer(isAdvanced, Edit = false, id = null) {
    let FormObject;
    let formData;

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

function ValidateDeposit() {
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
    fetch('/add/deposit', {
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
                alert('Error: ' + (data.message || 'Failed to add deposit'));
            }
        })
        .catch(error => {
            console.error('Unexpected error:', error);
            alert('Unexpected error occurred');
        });
}


function EditRecordExp(element) {
    const id = element.getAttribute('id').substring(3);

    const clickedRow = element.closest('tr');
    const rows = document.querySelectorAll('.historytable tbody tr');

    rows.forEach(row => {
        if (row !== clickedRow) {
            row.style.display = 'none';
        } else {
            row.style.display = ''; // Ensure the clicked row remains visible
        }
    });

    // Populate the form with the clicked row's data
    const cells = clickedRow.querySelectorAll('td');
    document.getElementById("Date").value = cells[1].textContent.trim();
    document.getElementById("Category").value = cells[2].textContent.trim();
    document.getElementById("Sub-category").value = cells[3].textContent.trim();
    document.getElementById("Person-Bank").value = cells[4].textContent.trim();
    document.getElementById("Sum").value = Math.abs(cells[5].textContent.trim());
    document.getElementById("Currency").value = cells[6].textContent.trim();
    document.getElementById("Comment").value = cells[7].textContent.trim();

    // Change the form's submit button to call ValidateExp with Edit=true
    const submitButton = document.querySelector('.submitrec');
    submitButton.setAttribute('onclick', 'ValidateExp(Edit=true, ' + id + ')');
}

function EditRecordInc(element) {
    const id = element.getAttribute('id').substring(3);

    const clickedRow = element.closest('tr');
    const rows = document.querySelectorAll('.historytable tbody tr');

    rows.forEach(row => {
        if (row !== clickedRow) {
            row.style.display = 'none';
        } else {
            row.style.display = ''; // Ensure the clicked row remains visible
        }
    });

    // Populate the form with the clicked row's data
    const cells = clickedRow.querySelectorAll('td');
    document.getElementById("Date").value = cells[1].textContent.trim();
    document.getElementById("Category").value = cells[2].textContent.trim();
    document.getElementById("Person-Bank").value = cells[3].textContent.trim();
    document.getElementById("Sum").value = Math.abs(cells[4].textContent.trim());
    document.getElementById("Currency").value = cells[5].textContent.trim();
    document.getElementById("Comment").value = cells[6].textContent.trim();

    // Change the form's submit button to call ValidateInc with Edit=true
    const submitButton = document.querySelector('.submitrec');
    submitButton.setAttribute('onclick', 'ValidateInc(Edit=true, ' + id + ')');
}

function EditRecordTransfer(element, isAdvanced = false) {
    const id = element.getAttribute('id').substring(3);

    const clickedRow = element.closest('tr');
    const parentTable = clickedRow.closest('table');
    const rows = parentTable.querySelectorAll('tbody tr');

    rows.forEach(row => {
        if (row !== clickedRow) {
            row.style.display = 'none';
        } else {
            row.style.display = ''; // Ensure the clicked row remains visible
        }
    });

    if (!isAdvanced) {
        document.getElementById("FormAdvanced").style.display = 'none';
        document.getElementById("AdvancedHistory").style.display = 'none';

        // Populate the form with the clicked row's data
        const cells = clickedRow.querySelectorAll('td');
        document.getElementById("Date").value = cells[1].textContent.trim();
        document.getElementById("Sender").value = cells[2].textContent.trim();
        document.getElementById("Receiver").value = cells[3].textContent.trim();
        document.getElementById("Sum").value = Math.abs(cells[4].textContent.trim());
        document.getElementById("Currency").value = cells[5].textContent.trim();
        document.getElementById("Comment").value = cells[6].textContent.trim();

        // Change the form's submit button to call ValidateTransfer with Edit=true
        const submitButton = document.getElementById('Submit');
        submitButton.setAttribute('onclick', 'ValidateTransfer(isAdvanced = false, Edit=true, ' + id + ')');
    }

    else {
        document.getElementById("FormStandard").style.display = 'none';
        document.getElementById("StandardHistory").style.display = 'none';

        // Populate the form with the clicked row's data
        const cells = clickedRow.querySelectorAll('td');
        document.getElementById("ADVDate").value = cells[1].textContent.trim();
        document.getElementById("ADVSender").value = cells[2].textContent.trim();
        document.getElementById("ADVSSum").value = Math.abs(cells[3].textContent.trim());
        document.getElementById("ADVSCurrency").value = cells[4].textContent.trim();
        document.getElementById("ADVReceiver").value = cells[5].textContent.trim();
        document.getElementById("ADVRSum").value = Math.abs(cells[6].textContent.trim());
        document.getElementById("ADVRCurrency").value = cells[7].textContent.trim();
        document.getElementById("ADVCurrencyRate").value = cells[8].textContent.trim();
        document.getElementById("ADVComment").value = cells[8].textContent.trim();

        // Change the form's submit button to call ValidateTransfer with Edit=true
        const submitButton = document.getElementById('ADVSubmit');
        submitButton.setAttribute('onclick', 'ValidateTransfer(isAdvanced = true, Edit=true, ' + id + ')');
    }
}

function createReportTable(tableData) {
    // Create container
    const container = document.createElement('div');

    // Add heading
    const heading = document.createElement('h3');
    heading.textContent = tableData.type;
    container.appendChild(heading);

    // Create table
    const table = document.createElement('table');

    // Create thead
    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');
    const thMonths = document.createElement('th');
    thMonths.textContent = 'Months';
    headRow.appendChild(thMonths);

    for (let i = 1; i <= 12; i++) {
        const th = document.createElement('th');
        th.textContent = i;
        headRow.appendChild(th);
    }
    thead.appendChild(headRow);
    table.appendChild(thead);

    // Create tbody
    const tbody = document.createElement('tbody');

    // Total row
    const totalRow = document.createElement('tr');
    const tdTotal = document.createElement('td');
    tdTotal.textContent = 'Total';
    totalRow.appendChild(tdTotal);

    tableData.total.forEach(val => {
        const td = document.createElement('td');
        td.textContent = val;
        totalRow.appendChild(td);
    });
    tbody.appendChild(totalRow);

    // Data rows
    for (const [rowName, rowData] of Object.entries(tableData.table_dict)) {
        const row = document.createElement('tr');
        const tdName = document.createElement('td');
        tdName.textContent = rowName;
        row.appendChild(tdName);

        rowData.forEach(val => {
            const td = document.createElement('td');
            td.textContent = val;
            row.appendChild(td);
        });
        tbody.appendChild(row);
    }

    table.appendChild(tbody);
    container.appendChild(table);

    return container;
}

function validateReport() {
    const report_type = document.getElementById("rep_type").value;
    const report_format = document.getElementById("rep_format").value;

    if (report_type === "None") {
        alert("Please select a report type.");
        return false;
    }

    FormData = {
        report_type: report_type,
        report_format: report_format
    };

    // Send POST request
    fetch("/report", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(FormData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const reportDiv = document.querySelector('.report_table');
                reportDiv.innerHTML = "";
                reportDiv.appendChild(createReportTable(data.table_data));
            } else {
                alert('Error: ' + (data.message || 'Failed to build table'));
            }
        })
        .catch(error => {
            console.error('Unexpected error:', error);
            alert('Unexpected error occurred');
        });
}