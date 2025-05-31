function validateTransactionForm() {
    // Get all form elements
    const type = document.getElementById('type').value;
    const date = document.getElementById('date').value;
    const pb = document.getElementById('pb').value;
    let amount = parseFloat(document.getElementById('amount').value).toFixed(2);
    const currency = document.getElementById('currency').value;
    const ipb = document.getElementById('ipb').value;
    let stockAmount = parseFloat(document.getElementById('stockAmount').value).toFixed(6);
    const stock = document.getElementById('stock').value;
    let fee = parseFloat(document.getElementById('fee').value).toFixed(2);

    // Validate required fields
    if (date === '' || pb === 'none' || amount === NaN || currency === 'none' || ipb === 'none' || stockAmount === NaN || stock === 'none') {
        alert("All fields except fee are required!");
        return false;
    }

    if (stockAmount <= 0 || amount <= 0) {
        alert('Buy/sell amount must be greater than 0');
        return false;
    }
    if (fee === "NaN") {
        fee = 0; // Default fee to 0 if not provided
    }
    else if (fee < 0) {
        alert('Fee must be greater than 0');
        return false;
    }

    if (type === 'pos') {
        amount = amount * -1; // Convert to negative for buy transactions
    } else if (type === 'neg') {
        stockAmount = stockAmount * -1; // Convert to negative for sell transactions
    }

    // Prepare form data
    const formData = {
        investmentDate: date,
        pb: pb,
        amount: amount,
        currency: currency,
        ipb: ipb,
        stockAmount: stockAmount,
        stock: stock,
        fee: fee
    };

    // Send POST request
    fetch('/invest/add/transaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
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

function validateStockForm() {
    // Get all form elements
    const date = document.getElementById('date').value;
    const stock = document.getElementById('stock').value;
    const price = parseFloat(document.getElementById('price').value).toFixed(4);

    // Validate required fields
    if (date === '' || stock === 'none' || price === NaN) {
        alert("All fields are required!");
        return false;
    }

    // Validate stock price
    if (price <= 0) {
        alert('Stock price must be greater than 0');
        return false;
    }

    // Prepare form data
    const formData = {
        date: date,
        stock: stock,
        price: price,
    };

    // Send POST request
    fetch('/invest/add/stockPrice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert('Error: ' + (data.message || 'Failed to add stock price'));
            }
        })
        .catch(error => {
            console.error('Unexpected error:', error);
            alert('Unexpected error occurred');
        });
}