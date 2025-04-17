function validateForm() {
    // Get all form elements
    const type = document.getElementById('type').value;
    const date = document.getElementById('date').value;
    const pb = document.getElementById('pb').value;
    const amount = document.getElementById('amount').value;
    const currency = document.getElementById('currency').value;
    const ipb = document.getElementById('ipb').value;
    const stockAmount = document.getElementById('stockAmount').value;
    const stock = document.getElementById('stock').value;

    if (stockAmount <= 0 || amount <= 0) {
        alert('Buy/sell amount must be greater than 0');
        return false;
    }

    // Prepare form data
    const formData = {
        type: type,
        investmentDate: date,
        pb: pb,
        amount: amount,
        currency: currency,
        ipb: ipb,
        stockAmount: stockAmount,
        stock: stock
    };

    // Send POST request
    fetch('/invest/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.ok) {
            alert('Investment record added successfully');
            window.location.href = '/invest/add';
        } else {
            response.json().then(data => {
                alert('Error: ' + (data.message || 'Failed to add investment record'));
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error occurred while submitting the form');
    });
}