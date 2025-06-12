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

function ValidateTransfer(isAdvanced) {
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

    // Send POST request
    fetch('/transfer', {
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

