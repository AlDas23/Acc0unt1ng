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

    // Change the form's submit button to call ValidateExpEdit
    const submitButton = document.querySelector('.submitrec');
    submitButton.setAttribute('onclick', 'ValidateExp(Edit=true, ' + id + ')');
}
