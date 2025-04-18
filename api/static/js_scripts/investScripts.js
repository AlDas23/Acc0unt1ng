function validateTransactionForm() {
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

    if (type === 'buy') {
        amount = amount * -1; // Convert to negative for buy transactions
    } else if (type === 'sell') {
        stockAmount = stockAmount * -1; // Convert to negative for sell transactions
    }

    // Round amount to 2 decimal places and stockAmount to 6 decimal places
    amount = parseFloat(amount).toFixed(2);
    stockAmount = parseFloat(stockAmount).toFixed(6);

    // Prepare form data
    const formData = {
        investmentDate: date,
        pb: pb,
        amount: amount,
        currency: currency,
        ipb: ipb,
        stockAmount: stockAmount,
        stock: stock
    };

    // Send POST request
    fetch('/invest/add/transaction', {
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

function validateStockForm() {
    // Get all form elements
    const date = document.getElementById('date').value;
    const stock = document.getElementById('stock').value;
    const price = document.getElementById('price').value;

    // Validate stock price
    if (price <= 0) {
        alert('Stock price must be greater than 0');
        return false;
    }
    // Round price to 2 decimal places
    price = parseFloat(price).toFixed(2);

    // Prepare form data
    const formData = {
        stock: stock,
        price: price,
        date: date
    };

    // Send POST request
    fetch('/invest/add/stockPrice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.ok) {
            alert('Stock price added successfully');
            window.location.href = '/invest/add/stockPrice';
        } else {
            response.json().then(data => {
                alert('Error: ' + (data.message || 'Failed to add stock price'));
            });
        }
    })
}