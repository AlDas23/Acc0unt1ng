from flask import Flask, request, render_template, redirect, url_for
from db_scripts.script import *
from db_scripts.consts import *


app = Flask(__name__)

def read_csv(file_name):
    values = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                values.append(row[0])
    return values

@app.route("/", methods = ["POST", "GET"])
def main():
    return redirect("/add/expense")

@app.route("/add/expense", methods = ["POST", "GET"])
def Expense():
    if (request.method == "GET"):
        categories = read_csv(SPVcatPath)
        sub_categories = read_csv(SPVsubcatPath)
        person_banks = Read('retacc')
        currencies = read_csv(SPVcurrPath)
        
        options = {
        'categories': categories,
        'sub_categories': sub_categories,
        'person_banks': person_banks,
        'currencies': currencies
    }
        return render_template("addexp.html", options=options)
    
    else:
        date = request.form.get("Date", "")
        category = request.form.get("Category", "")
        sub_category = request.form.get("Sub-category", "")
        person_bank = request.form.get("Person-Bank", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")

        # Check if comment is empty and assign a whitespace if it is
        if not comment:
            comment = " "
        
        # Insert minus to expense sum
        sum = '-' + sum

        final_str = f"{date},{category},{sub_category},{person_bank},{comment},{sum},{currency}"

        try:
            Add(final_str,'main')
        except:
            return 'Failed to add record!'
        return redirect(url_for("Expense"))
    
@app.route("/add/income", methods = ["POST", "GET"])
def Income():
    if (request.method == "GET"):
        categories = read_csv(SPVcatPath)
        currencies = read_csv(SPVcurrPath)
        person_banks = Read('retacc')
        
        options = {
        'categories': categories,
        'person_banks': person_banks,
        'currencies': currencies
    }
        return render_template("addinc.html", options=options)
    else:
        date = request.form.get("Date", "")
        category = request.form.get("Category", "")
        sub_category = request.form.get("Sub-category", "")
        person_bank = request.form.get("Person-Bank", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")

        # Check if comment is empty and assign a whitespace if it is
        if not comment:
            comment = " "

        final_str = f"{date},{category},{sub_category},{person_bank},{comment},{sum},{currency}"

        try:
            Add(final_str,'main')
        except:
            return 'Failed to add record!'
        return redirect(url_for("Income"))
    
@app.route("/transfer", methods = ["POST", "GET"])
def Transfer():
    if (request.method == "GET"):
        currencies = read_csv(SPVcurrPath)
        person_banks = Read('retacc')
        
        options = {
        'person_banks': person_banks,
        'currencies': currencies
    }
        return render_template("transfer.html", options=options)
    else:
        date = request.form.get("Date", "")
        sender = request.form.get("Sender", "")
        receiver = request.form.get("Receiver", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")

        if not comment:
            comment = " "
            
        final_str = f"{date},{sender},{receiver},{comment},{sum},{currency}"

        try:
            Add(final_str, 'transfer')
        except:
            return 'Failed to add record!'
        return redirect(url_for("Transfer"))
        
@app.route("/view/rep", methods = ["POST", "GET"])
def ViewReports():
    if (request.method == "GET"):
        return render_template('viewrep.html', columns=[], data=[])
    else:
        report_type = request.form['View Report']
        if report_type == 'allm':
            data = Read(report_type)
            columns = ["ID", "Date", "Category", "Sub-category", "Person bank", "Comment", "Sum", "Currency"]
        elif report_type == 'alltran':
            data = Read(report_type)
            columns = ["ID", "Date", "Sender", "Receiver", "Comment" ,"Sum", "Currency"]
        
        return render_template('viewrep.html', columns=columns, data=data, selected_option=report_type)
    
@app.route("/view/acc", methods = ["GET"])
def ViewAcc():
    if (request.method == "GET"):
        data = Read('allacc')
        return render_template('viewacc.html', columns=["Person bank", "Sum", "Currency"], data=data)    
    
def api_start():
    app.run(debug=True)