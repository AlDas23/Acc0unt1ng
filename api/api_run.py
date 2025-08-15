from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
)
import base64
import io
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from db_scripts.script import *
from db_scripts.baseScripts import Add, MarkerRead, Re_Calculate_deposit, Read
from db_scripts.csvScripts import read_csv
from db_scripts.consts import *
from api.api_invest import investPage

app = Flask(__name__)
app.register_blueprint(investPage, url_prefix="/")


def plot_to_img_tag(df):
    plt.clf()

    plt.figure(figsize=(12, 6))

    # Plot each currency's rate over time
    for currency in df.columns[1:]:  # Skip the 'date' column
        plt.plot(df["date"], df[currency], marker="o", label=currency)

    plt.title("Currency Rates Over Time")
    plt.xlabel("Date")
    plt.ylabel("Rate")
    plt.legend()
    plt.grid(True)

    # Rotate and align the tick labels so they look better
    plt.xticks(rotation=45, ha="right")

    # Use automatic layout adjustment to prevent label overlap
    plt.tight_layout()

    # If still too crowded, show fewer x-axis ticks
    if len(df) > 20:
        # Show approximately 15 evenly spaced ticks
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)

    # Encode image to base64 string
    img_tag = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return img_tag


@app.route("/", methods=["POST", "GET"])
def main():
    Re_Calculate_deposit()
    return redirect("/add/expense")


@app.route("/api/get/options/<string:source>", methods=["GET"])
def GetOptions(source):
    try:
        if source == "expense":
            categories = read_csv(SPVcatExpPath)
            sub_categories = read_csv(SPVsubcatPath)
            currencies = read_csv(SPVcurrPath)
            person_banks = Read("retacc")
            payload = jsonify(
                {
                    "success": True,
                    "categories": categories,
                    "subcategories": sub_categories,
                    "currency": currencies,
                    "pb": person_banks,
                }
            )
        elif source == "income":
            categories = read_csv(SPVcatIncPath)
            currencies = read_csv(SPVcurrPath)
            person_banks = Read("retacc")
            payload = jsonify(
                {
                    "success": True,
                    "categories": categories,
                    "currency": currencies,
                    "pb": person_banks,
                }
            )
        elif source == "transfer":
            currencies = read_csv(SPVcurrPath)
            person_banks = Read("retacc")
            payload = jsonify(
                {
                    "success": True,
                    "currencies": currencies,
                    "pb": person_banks,
                }
            )
        elif source == "deposit":
            currencies = read_csv(SPVcurrPath)
            person_banks = Read("retacc")
            payload = jsonify(
                {
                    "success": True,
                    "currencies": currencies,
                    "pb": person_banks,
                }
            )

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        error_message = str(e)
        payload = (
            jsonify(
                {
                    "success": False,
                    "message": error_message,
                }
            ),
            400,
        )
    finally:
        return payload


@app.route("/api/get/history/<string:source>", methods=["GET"])
def GetHistory(source):
    try:
        if source == "expense":
            payload = GetTransactionHistory("expense")
        elif source == "income":
            payload = GetTransactionHistory("income")
        elif source == "transfer":
            payload = GetTransactionHistory("transfer")
        elif source == "transferADV":
            payload = GetTransactionHistory("advtransfer")
        elif source == "depositO":
            payload = GetTransactionHistory("depositO")
        elif source == "depositC":
            payload = GetTransactionHistory("depositC")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        error_message = str(e)
        payload = (
            jsonify(
                {
                    "success": False,
                    "message": error_message,
                }
            ),
            400,
        )
    finally:
        return payload


@app.route("/api/add/expense", methods=["POST"])
def AddExpense():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    # Parse JSON data into string line
    line = ",".join([str(content[key]) for key in content.keys()])

    try:
        Add(line, "main")
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        error_message = str(e)
        return (
            jsonify(
                {
                    "success": False,
                    "message": error_message,
                }
            ),
            400,
        )


@app.route("/api/edit/expense/<int:id>", methods=["POST"])
def EditExpense(id):
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    # Parse JSON data into string line
    line = ",".join([str(content[key]) for key in content.keys()])
    line = f"{id}," + line  # Prepend the ID to the line

    try:
        UpdateRecord(line, "main")
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        error_message = str(e)
        return (
            jsonify(
                {
                    "success": False,
                    "message": error_message,
                }
            ),
            400,
        )


@app.route("/api/add/income", methods=["POST"])
def AddIncome():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    # Parse JSON data into string line
    line = ",".join([str(content[key]) for key in content.keys()])

    try:
        Add(line, "main")
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        error_message = str(e)
        return (
            jsonify(
                {
                    "success": False,
                    "message": error_message,
                }
            ),
            400,
        )


@app.route("/api/edit/income/<int:id>", methods=["POST"])
def EditIncome(id):
    if request.method == "POST":
        content = request.get_json()
        if content is None:
            return "Error: No JSON data received", 400

        # Parse JSON data into string line
        line = ",".join([str(content[key]) for key in content.keys()])
        line = f"{id}," + line  # Prepend the ID to the line

        try:
            UpdateRecord(line, "main")
            return jsonify({"success": True})
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            error_message = str(e)
            return (
                jsonify(
                    {
                        "success": False,
                        "message": error_message,
                    }
                ),
                400,
            )


@app.route("/api/add/transfer", methods=["POST"])
def AddTransfer():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    transferType = content.pop("transferType", "")
    # Parse JSON data into string line
    line = ",".join([str(content[key]) for key in content.keys()])
    if transferType == "standard":
        try:
            Add(line, "transfer")
            return jsonify({"success": True})
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            error_message = str(e)
            return (
                jsonify(
                    {
                        "success": False,
                        "message": error_message,
                    }
                ),
                400,
            )

    elif transferType == "advanced":
        try:
            Add(line, "advtransfer")
            return jsonify({"success": True})
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            error_message = str(e)
            return (
                jsonify(
                    {
                        "success": False,
                        "message": error_message,
                    }
                ),
                400,
            )


@app.route("/api/edit/transfer/<int:id>", methods=["POST"])
def EditTransfer(id):
    if request.method == "POST":
        content = request.get_json()
        if content is None:
            return "Error: No JSON data received", 400

        transferType = content.pop("transferType", "")
        # Parse JSON data into string line
        line = ",".join([str(content[key]) for key in content.keys()])
        line = f"{id}," + line

        if transferType == "standard":
            try:
                UpdateRecord(line, "transfer")
                return jsonify({"success": True})
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                error_message = str(e)
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": error_message,
                        }
                    ),
                    400,
                )

        elif transferType == "advanced":
            try:
                UpdateRecord(line, "advtransfer")
                return jsonify({"success": True})
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                error_message = str(e)
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": error_message,
                        }
                    ),
                    400,
                )


@app.route("/api/add/deposit", methods=["POST"])
def AddDeposit():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    # Parse JSON data into string line
    line = ",".join([str(content[key]) for key in content.keys()])

    try:
        Add(line, "deposit")
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        error_message = str(e)
        return (
            jsonify(
                {
                    "success": False,
                    "message": error_message,
                }
            ),
            400,
        )


@app.route("/view/rep", methods=["GET"])
def ViewReports():
    currencies = read_csv(SPVcurrPath)

    Ldata = GetYearlyData("yeartotalrep")
    Lcolumns = ["Month", "Incomes", "Expenses", "Balance"]
    Rdata = GetYearlyData("yearexprep")
    Rcolumns = ["Month"] + currencies + ["Total in RON"]
    Cdata = GetYearlyData("yearincrep")
    Ccolumns = ["Month"] + currencies + ["Total in RON"]

    return render_template(
        "viewrep.html",
        Lcolumns=Lcolumns,
        Ldata=Ldata,
        Ccolumns=Ccolumns,
        Cdata=Cdata,
        Rcolumns=Rcolumns,
        Rdata=Rdata,
    )


@app.route("/view/reports/table", methods=["GET", "POST"])
def Report():
    if request.method == "GET":
        try:
            expCategories = read_csv(SPVcatExpPath)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            error_message = str(e)
            return (
                jsonify(
                    {
                        "success": False,
                        "message": error_message,
                    }
                ),
                400,
            )

        return render_template("reports.html", categories=expCategories)

    elif request.method == "POST":
        content = request.get_json()
        if content is None:
            return "Error: No JSON data received", 400

        # Parse JSON data into string line
        params = ",".join([str(content[key]) for key in content.keys()])

        try:
            table_data = GenerateReport(params)
            return jsonify({"success": True, "table_data": table_data})
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            error_message = str(e)
            return (
                jsonify(
                    {
                        "success": False,
                        "message": error_message,
                    }
                ),
                400,
            )


@app.route("/view/reports/legacy", methods=["POST", "GET"])
def ViewAdvReports():
    if request.method == "GET":
        return render_template(
            "viewrepadv.html", columns=[], data=[], columns2=[], data2=[]
        )
    else:
        report_type = request.form["View Report"]
        if report_type != "None":
            month = request.form["Month"]
            if report_type == "catpbrep":
                data = ReadAdv(report_type, month)
                columns = ["Category", "Person bank", "Currency", "Sum"]
            if report_type == "catincrep":
                data = ReadAdv(report_type, month)
                columns = ["Category", "Sum RON", "%"]
            if report_type == "catexprep":
                data = ReadAdv(report_type, month)
                columns = ["Category", "Sum RON", "%"]
            if report_type == "subcatrep":
                data = ReadAdv(report_type, month)
                columns = ["Sub-category", "Sum RON", "%"]
            if report_type == "catincbankrep":
                data = ReadAdv(report_type, month)
                columns = ["Category", "Person bank", "Currency", "Sum"]

        report_type2 = request.form["View Report2"]
        if report_type2 != "None":
            month2 = request.form["Month2"]
            if report_type2 == "catpbrep":
                data2 = ReadAdv(report_type2, month2)
                columns2 = ["Category", "Person bank", "Currency", "Sum"]
            if report_type2 == "catincrep":
                data2 = ReadAdv(report_type2, month2)
                columns2 = ["Category", "Sum RON", "%"]
            if report_type2 == "catexprep":
                data2 = ReadAdv(report_type2, month2)
                columns2 = ["Category", "Sum RON", "%"]
            if report_type2 == "subcatrep":
                data2 = ReadAdv(report_type2, month2)
                columns2 = ["Sub-category", "Sum RON", "%"]
            if report_type2 == "catincbankrep":
                data2 = ReadAdv(report_type2, month2)
                columns2 = ["Category", "Person bank", "Currency", "Sum"]

        if report_type == "None" and report_type2 == "None":
            return render_template(
                "viewrepadv.html",
                selected_option=report_type,
                selected_option2=report_type2,
            )
        elif report_type != "None" and report_type2 == "None":
            return render_template(
                "viewrepadv.html",
                columns=columns,
                data=data,
                selected_option=report_type,
                selected_option2=report_type2,
                selected_month=month,
            )
        elif report_type == "None" and report_type2 != "None":
            return render_template(
                "viewrepadv.html",
                columns2=columns2,
                data2=data2,
                selected_option=report_type,
                selected_option2=report_type2,
                selected_month2=month2,
            )
        elif report_type != "None" and report_type2 != "None":
            return render_template(
                "viewrepadv.html",
                columns=columns,
                data=data,
                columns2=columns2,
                data2=data2,
                selected_option=report_type,
                selected_option2=report_type2,
                selected_month=month,
                selected_month2=month2,
            )


@app.route("/view/acc", methods=["GET", "POST"])
def ViewAcc():
    data_curr1 = ConvRead("norm", "allcurr", True)
    data_curr2 = Read("allcurr")
    data = MarkerRead("none")

    # Combine the two data sets

    data_curr = []
    for curr1 in data_curr1:
        for curr2 in data_curr2:
            if curr1[0] == curr2[0]:  # Match on currency name
                data_curr.append(
                    (
                        curr1[0],  # Currency name
                        curr2[1],  # Original sum
                        curr1[1],  # Converted sum
                        curr1[2],  # Percent
                    )
                )
                break
    columns_curr = ["Currency", "Sum", "Sum RON", "%"]
    owners = ConvReadPlus("norm", "allmowner")
    columns_owner = ["Owner", "Currency", "Sum", "Sum RON"]
    types = ConvRead("norm", "allmtype", True)
    columns_type = ["Type", "Sum RON", "%"]
    currType = GenerateTable("currType+%")
    currType_columns = ["Currency", "Type", "Sum", "%"]
    ownersList = Read("retmowner")
    typesList = Read("retmtype")
    options = {"owners": ownersList, "types": typesList}

    tables = {
        "owner": owners,
        "owner_columns": columns_owner,
        "type": types,
        "type_columns": columns_type,
        "curr": data_curr,
        "curr_columns": columns_curr,
        "currType": currType,
        "currType_columns": currType_columns,
    }

    if request.method == "GET":
        return render_template(
            "viewacc.html",
            tables=tables,
            columns=["Person bank", "Currency", "Sum"],
            data=data,
            options=options,
        )
    elif request.method == "POST":
        owner = request.form["Acc owner"]
        type = request.form["Acc type"]

        if type == " " and owner != " ":
            data = MarkerRead("byowner", owner)

        elif owner == " " and type != " ":
            data = MarkerRead("bytype", type)

        elif owner != " " and type != " ":
            all = owner + "," + type
            data = MarkerRead("byall", all)
        else:
            data = MarkerRead("none")

        return render_template(
            "viewacc.html",
            tables=tables,
            options=options,
            columns=["Person bank", "Currency", "Sum"],
            data=data,
            selected_owner=owner,
            selected_type=type,
        )


@app.route("/currency", methods=["GET", "POST"])
def Currencies():
    if request.method == "GET":
        data = Read("allcurrrate")
        columns = ["Date", "RON", "UAH", "EUR", "USD", "GBP", "CHF", "HUF"]
        df = Read("retcurrr")
        plot1 = plot_to_img_tag(df)

        return render_template(
            "currencies.html", columns=columns, data=data, plot1=plot1
        )

    else:
        date = request.form["Date"]
        ron = request.form["RON"]
        eur = request.form.get("EUR", " ")
        usd = request.form.get("USD", " ")
        gbp = request.form.get("GBP", " ")
        chf = request.form.get("CHF", " ")
        huf = request.form.get("HUF", " ")

        final_str = f"{date},{ron},{eur},{usd},{gbp},{chf},{huf}"

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
    # app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1200
    app.run(debug=True, port=5050)
