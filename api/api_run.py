from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
)
from db_scripts.script import *
from db_scripts.consts import *


app = Flask(__name__)


def read_csv(file_name):
    values = []
    with open(file_name, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                values.append(row[0])
    return values


@app.route("/", methods=["POST", "GET"])
def main():
    return redirect("/add/expense")


@app.route("/add/expense", methods=["POST", "GET"])
def Expense():
    if request.method == "GET":
        categories = read_csv(SPVcatExpPath)
        sub_categories = read_csv(SPVsubcatPath)
        person_banks = Read("retacc")
        currencies = read_csv(SPVcurrPath)

        options = {
            "categories": categories,
            "sub_categories": sub_categories,
            "person_banks": person_banks,
            "currencies": currencies,
        }

        data = Read("m-")
        columns = [
            "ID",
            "Date",
            "Category",
            "Sub-category",
            "Person bank",
            "Sum",
            "Currency",
            "Comment",
        ]

        return render_template(
            "addexp.html", options=options, columns=columns, data=data
        )

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
        sum = "-" + sum

        final_str = (
            f"{date},{category},{sub_category},{person_bank},{sum},{currency},{comment}"
        )

        try:
            Add(final_str, "main")
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("Expense"))


@app.route("/add/income", methods=["POST", "GET"])
def Income():
    if request.method == "GET":
        categories = read_csv(SPVcatIncPath)
        currencies = read_csv(SPVcurrPath)
        person_banks = Read("retacc")

        options = {
            "categories": categories,
            "person_banks": person_banks,
            "currencies": currencies,
        }

        data = Read("m+")
        columns = [
            "ID",
            "Date",
            "Category",
            "Person bank",
            "Sum",
            "Currency",
            "Comment",
        ]

        return render_template(
            "addinc.html", options=options, columns=columns, data=data
        )
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

        final_str = (
            f"{date},{category},{sub_category},{person_bank},{sum},{currency},{comment}"
        )

        try:
            Add(final_str, "main")
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("Income"))


@app.route("/transfer", methods=["POST", "GET"])
def Transfer():
    if request.method == "GET":
        currencies = read_csv(SPVcurrPath)
        person_banks = Read("retacc")

        options = {"person_banks": person_banks, "currencies": currencies}

        data = Read("alltran")
        columns = ["ID", "Date", "Sender", "Receiver", "Sum", "Currency", "Comment"]
        dataA = Read("alladvtran")
        columnsA = [
            "ID",
            "Date",
            "Sender",
            "Sum",
            "Currency",
            "Receiver",
            "Sum",
            "Currency",
            "Currency rate",
            "Comment",
        ]

        return render_template(
            "transfer.html",
            options=options,
            columns=columns,
            data=data,
            dataA=dataA,
            columnsA=columnsA,
        )
    else:
        form_id = request.form.get("form_type")
        if form_id == "transfer":
            date = request.form.get("Date", "")
            sender = request.form.get("Sender", "")
            receiver = request.form.get("Receiver", "")
            comment = request.form.get("Comment", "")
            sum = request.form.get("Sum", "")
            currency = request.form.get("Currency", "")

            # Check if comment is empty and assign a whitespace if it is
            if not comment:
                comment = " "

            final_str = f"{date},{sender},{receiver},{sum},{currency},{comment}"

            try:
                Add(final_str, "transfer")
            except Exception as e:
                # Capture the exception message
                error_message = str(e)
                # Return the error message in the response
                return render_template_string(
                    "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                    error_message=error_message,
                )

            return redirect(url_for("Transfer"))

        elif form_id == "advtransfer":
            date = request.form.get("Date", "")
            sender = request.form.get("Sender", "")
            ssum = request.form.get("SSum", "")
            scurr = request.form.get("SCurrency", "")
            receiver = request.form.get("Receiver", "")
            rsum = request.form.get("RSum", "")
            rcurr = request.form.get("RCurrency", "")
            curr_rate = request.form.get("Currency rate", "")
            comment = request.form.get("Comment", "")

            # Check if comment is empty and assign a whitespace if it is
            if not comment:
                comment = " "

            final_str = f"{date},{sender},{ssum},{scurr},{receiver},{rsum},{rcurr},{curr_rate},{comment}"

            try:
                Add(final_str, "advtransfer")
            except Exception as e:
                # Capture the exception message
                error_message = str(e)
                # Return the error message in the response
                return render_template_string(
                    "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                    error_message=error_message,
                )

            return redirect(url_for("Transfer"))


@app.route("/add/deposit", methods=["POST", "GET"])
def AddDeposit():
    if request.method == "GET":
        Re_calculate()

        currencies = read_csv(SPVcurrPath)
        person_banks = Read("retacc")

        options = {"person_banks": person_banks, "currencies": currencies}

        data = Read("alldepacc")
        columns = ["Name", "Owner", "Sum", "Currency"]

        dataA = Read("opendep")
        columnsH = [
            "Date in",
            "Name",
            "Owner",
            "Sum",
            "Currency",
            "Months",
            "Date out",
            "Percent",
            "Currency rate",
            "Expected amount",
            "Comment",
        ]
        dataC = Read("closeddep")

        return render_template(
            "adddeposit.html",
            options=options,
            columns=columns,
            data=data,
            columnsA=columnsH,
            dataA=dataA,
            columnsC=columnsH,
            dataC=dataC,
        )
    else:
        dateIn = request.form.get("DateIn", "")
        name = request.form.get("Name", "")
        owner = request.form.get("Owner", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")
        months = request.form.get("Months", "")
        dateOut = request.form.get("DateOut", "")
        percent = request.form.get("Percent", "")
        currRate = request.form.get("Currency rate", "")

        # Check fields if empty and assign a whitespace if they are
        if not comment:
            comment = " "
        if not months:
            months = " "
        if not dateOut:
            dateOut = " "
        if not currRate:
            currRate = " "

        final_str = f"{dateIn},{name},{owner},{sum},{currency},{months},{dateOut},{percent},{currRate},{comment}"

        try:
            Add(final_str, "deposit")
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("AddDeposit"))


@app.route("/view/rep", methods=["POST", "GET"])
def ViewReports():
    if request.method == "GET":
        return render_template("viewrep.html", columns=[], data=[])
    else:
        report_type = request.form["View Report"]
        if report_type == "catincrep":
            data = Read(report_type)
            columns = ["Category", "Currency", "Sum"]
        elif report_type == "catexprep":
            data = Read(report_type)
            columns = ["Category", "Currency", "Sum"]

        return render_template(
            "viewrep.html", columns=columns, data=data, selected_option=report_type
        )


@app.route("/view/advrep", methods=["POST", "GET"])
def ViewAdvReports():
    if request.method == "GET":
        return render_template("viewrepadv.html", columns=[], data=[])
    else:
        report_type = request.form["View Report"]
        month = request.form["Month"]
        if report_type == "catpbrep":
            data = ReadAdv(report_type, month)
            columns = ["Category", "Person bank", "Currency", "Sum"]
        if report_type == "catincrep":
            data = ReadAdv(report_type, month)
            columns = ["Category", "Currency", "Sum"]
        if report_type == "catexprep":
            data = ReadAdv(report_type, month)
            columns = ["Category", "Currency", "Sum"]

        return render_template(
            "viewrepadv.html",
            columns=columns,
            data=data,
            selected_option=report_type,
            selected_month=month,
        )


@app.route("/view/acc", methods=["GET", "POST"])
def ViewAcc():
    data_curr = Read("allcurr")
    columns_curr = ["Currency", "Sum"]
    data_owner = Read("allmowner")
    columns_owner = ["Owner", "Sum", "Currency"]
    data_type = Read("allmtype")
    columns_type = ["Type", "Sum", "Currency"]
    owners = Read("retmowner")
    types = Read("retmtype")
    options = {"owners": owners, "types": types}

    if request.method == "GET":
        return render_template(
            "viewacc.html",
            data_curr=data_curr,
            columns_curr=columns_curr,
            data_owner=data_owner,
            columns_owner=columns_owner,
            data_type=data_type,
            columns_type=columns_type,
            options=options,
        )
    else:
        owner = request.form["Acc owner"]
        type = request.form["Acc type"]

        if type == " " and owner != " ":
            data = MarkerRead(owner, "byowner")

        elif owner == " " and type != " ":
            data = MarkerRead(type, "bytype")

        elif owner != " " and type != " ":
            temp = owner + "," + type
            data = MarkerRead(temp, "byall")
        else:
            return redirect(url_for("ViewAcc"))

        return render_template(
            "viewacc.html",
            data_curr=data_curr,
            columns_curr=columns_curr,
            data_owner=data_owner,
            columns_owner=columns_owner,
            data_type=data_type,
            columns_type=columns_type,
            options=options,
            columns=["Person bank", "Sum", "Currency"],
            data=data,
            selected_owner=owner,
            selected_type=type,
        )


@app.route("/currency", methods=["GET", "POST"])
def Currencies():
    if request.method == "GET":
        data = Read("allcurrrate")
        columns = ["Date", "RON", "UAH", "EUR", "USD", "GBP", "CHF", "HUF", "AUR"]

        return render_template("currencies.html", columns=columns, data=data)

    else:
        date = request.form["Date"]
        ron = request.form["RON"]
        eur = request.form["EUR"]
        usd = request.form["USD"]
        gbp = request.form["GBP"]
        chf = request.form["CHF"]
        huf = request.form["HUF"]
        aur = request.form["AUR"]

        final_str = f"{date},{ron},{eur},{usd},{gbp},{chf},{huf},{aur}"

        try:
            Add(final_str, "currrate")
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to currency rate!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("Currencies"))


def api_start():
    app.run(debug=True)
