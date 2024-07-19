from flask import Flask, request, render_template
from db_scripts.script import *


app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def main():
    if (request.method == "GET"):
        return render_template("main.html")
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
        return render_template("main.html")
    
@app.route("/transfer", methods = ["POST", "GET"])
def transfer():
    if (request.method == "GET"):
        return render_template("transfer.html")
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
        return render_template("transfer.html")
        
@app.route("/viewrep", methods = ["POST", "GET"])
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
        elif report_type == 'allacc':
            data = Read(report_type)
            columns = ["Person bank", "Sum", "Currency"]
        
        return render_template('viewrep.html', columns=columns, data=data, selected_option=report_type)
    
    
def api_start():
    app.run(debug=True)