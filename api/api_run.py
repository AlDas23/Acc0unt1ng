from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
)

from db_scripts.script import *
from db_scripts.baseScripts import Add, MarkerRead, Re_Calculate_deposit, Read
from db_scripts.csvScripts import read_csv
from db_scripts.consts import *
from helpers.genPlot import plot_to_img_tag
from api.api_invest import investPage

app = Flask(__name__)
app.register_blueprint(investPage, url_prefix="/")


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

        elif source == "currencyrates":
            currencies = read_csv(SPVcurrPath)
            payload = jsonify(
                {
                    "success": True,
                    "currency": currencies,
                }
            )

        elif source == "balance":
            ownersList = Read("retmowner")
            typesList = Read("retmtype")
            payload = jsonify(
                {"success": True, "owner": ownersList, "type": typesList}
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
        elif source == "currencyrates":
            payload = GetTransactionHistory("currencyrates")

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


@app.route("/api/get/plot/<string:source>", methods=["GET"])
def GetPlot(source):
    if source == "currencyrates":
        try:
            df = Read("retcurrr")
            plot1 = plot_to_img_tag(df, "Currency Rates Over Time", "Date", "Rate")
            payload = jsonify({"success": True, "plot": plot1})
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


@app.route("/api/add/currencyrates", methods=["POST"])
def AddCurrencyRate():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    # Parse JSON data into string line
    line = ",".join([str(content[key]) for key in content.keys()])

    try:
        Add(line, "currrate")
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


@app.route("/api/get/balance/<string:source>", methods=["POST"])
def Balance(source):
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    try:
        if source == "tables":
            if content.table == "allcurr":
                data_curr1 = ConvRead("norm", "allcurr", True)
                data_curr2 = Read("allcurr")

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

                payload = jsonify(
                    {
                        "success": True,
                        "table": data_curr,
                    }
                )
            elif content.table == "owner-table":
                owners = ConvReadPlus("norm", "allmowner")

                payload = jsonify(
                    {
                        "success": True,
                        "table": owners,
                    }
                )
            elif content.table == "type-table":
                types = ConvRead("norm", "allmtype", True)

                payload = jsonify(
                    {
                        "success": True,
                        "table": types,
                    }
                )
            elif content.table == "currType":
                currType = GenerateTable("currType+%")
                payload = jsonify(
                    {
                        "success": True,
                        "table": currType,
                    }
                )
                
        elif source == "balance":
            if content.owner is "None" and content.type is "None":
                data = MarkerRead("none") 
            elif content.owner is not "None" and content.type is "None":
                data = MarkerRead("byowner", content.owner)
            elif content.owner is "None" and content.type is not "None":
                data = MarkerRead("bytype", content.type)
            elif content.owner is not "None" and content.type is not "None":
                data = MarkerRead("byall", content.owner + "," + content.type)
                
            payload = jsonify({
                "success": True,
                "data": data,
            })
                
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        payload = (
            jsonify(
                {
                    "success": False,
                    "message": str(e),
                }
            ),
            400,
        )

    finally:
        return payload


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


def api_start():
    # app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1200
    app.run(debug=True, port=5050)
