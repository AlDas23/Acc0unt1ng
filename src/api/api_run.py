from flask import Flask, jsonify, request
from flask_cors import CORS
from db_scripts.script import *
from db_scripts.baseScripts import (
    Add,
    MarkerRead,
    Re_Calculate_deposit,
    Read,
    CheckDB,
    NewDBase,
)
from db_scripts.csvScripts import read_csv, SPVconf
from db_scripts.consts import *
from helpers.decorators import db_required
from helpers.genPlot import plot_to_img_tag
from api.api_invest import investPage

app = Flask(__name__)
app.register_blueprint(investPage, url_prefix="/")
CORS(app, resources=r"/*")


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/get/list/<string:source>", methods=["GET"])
def GetList(source):
    try:
        if source == "categories_exp":
            expCategories = read_csv(SPVcatExpPath)
            payload = jsonify(
                {
                    "success": True,
                    "categories": expCategories,
                }
            )
        elif source == "categories_inc":
            incCategories = read_csv(SPVcatIncPath)
            payload = jsonify(
                {
                    "success": True,
                    "categories": incCategories,
                }
            )
        elif source == "subcategories":
            subCategories = read_csv(SPVsubcatPath)
            payload = jsonify(
                {
                    "success": True,
                    "subcategories": subCategories,
                }
            )
        elif source == "currency":
            currencies = read_csv(SPVcurrPath)
            payload = jsonify(
                {
                    "success": True,
                    "currencies": currencies,
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


@app.route("/get/options/<string:source>", methods=["GET"])
@db_required
def GetOptions(source):
    try:
        if source == "expense":
            categories = read_csv(SPVcatExpPath)
            sub_categories = read_csv(SPVsubcatPath)
            currencies = read_csv(SPVcurrPath)
            person_banks = Read("retacc")
            options = {
                "categories": categories,
                "subcategories": sub_categories,
                "currency": currencies,
                "pb": person_banks,
            }

        elif source == "income":
            categories = read_csv(SPVcatIncPath)
            currencies = read_csv(SPVcurrPath)
            person_banks = Read("retacc")
            options = {
                "categories": categories,
                "currency": currencies,
                "pb": person_banks,
            }

        elif source == "transfer":
            currencies = read_csv(SPVcurrPath)
            person_banks = Read("retacc")
            options = {
                "currency": currencies,
                "pb": person_banks,
            }

        elif source == "deposit":
            currencies = read_csv(SPVcurrPath)
            person_banks = Read("retacc")
            options = {
                "currencies": currencies,
                "pb": person_banks,
            }

        elif source == "currencyrates":
            currencies = read_csv(SPVcurrPath)
            options = {
                "currency": currencies,
            }

        elif source == "balance":
            ownersList = Read("retmowner")
            typesList = Read("retmtype")
            options = {"owner": ownersList, "type": typesList}

        payload = jsonify({"success": True, "options": options})

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


@app.route("/get/history/<string:source>", methods=["GET"])
@db_required
def GetHistory(source):
    try:
        if source == "expense":
            history = GetTransactionHistory("expense")
        elif source == "income":
            history = GetTransactionHistory("income")
        elif source == "transfer":
            history = GetTransactionHistory("transfer")
        elif source == "transferADV":
            history = GetTransactionHistory("advtransfer")
        elif source == "depositO":
            Re_Calculate_deposit()
            history = GetTransactionHistory("depositO")
        elif source == "depositC":
            history = GetTransactionHistory("depositC")
        elif source == "currencyrates":
            history = GetTransactionHistory("currencyrates")

        payload = jsonify(
            {
                "success": True,
                "history": history,
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


@app.route("/get/plot/<string:source>", methods=["GET"])
@db_required
def GetPlot(source):
    if source == "currencyrates":
        try:
            data = Read("currrate")
            plot1 = plot_to_img_tag(data, "Currency Rates Over Time", "Date", "Rate")
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


@app.route("/add/expense", methods=["POST"])
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


@app.route("/edit/expense/<int:id>", methods=["POST"])
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


@app.route("/add/income", methods=["POST"])
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


@app.route("/edit/income/<int:id>", methods=["POST"])
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


@app.route("/add/transfer", methods=["POST"])
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


@app.route("/edit/transfer/<int:id>", methods=["POST"])
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


@app.route("/add/deposit", methods=["POST"])
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


@app.route("/add/currencyrates", methods=["POST"])
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


@app.route("/get/balance/<string:source>", methods=["POST"])
@db_required
def Balance(source):
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    Re_Calculate_deposit()
    try:
        if source == "tables":
            table_name = content.get("table") if isinstance(content, dict) else content

            if table_name == "curr-table":
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
            elif table_name == "owner-table":
                owners = ConvReadPlus("norm", "allmowner")

                payload = jsonify(
                    {
                        "success": True,
                        "table": owners,
                    }
                )
            elif table_name == "type-table":
                types = ConvRead("norm", "allmtype", True)

                payload = jsonify(
                    {
                        "success": True,
                        "table": types,
                    }
                )
            elif table_name == "curr-type-table":
                currType = GenerateTable("currType+%")
                payload = jsonify(
                    {
                        "success": True,
                        "table": currType,
                    }
                )
            else:
                payload = jsonify(
                    {
                        "success": False,
                        "message": "Invalid table name",
                    }
                )

        elif source == "balance":
            # For balance source, content should be an object with owner and type
            if isinstance(content, dict):
                owner = content.get("owner", "None")
                type_val = content.get("type", "None")
            else:
                # Handle case where content might be sent as a string
                owner = "None"
                type_val = "None"

            if owner == "None" and type_val == "None":
                data = MarkerRead("none")
            elif owner != "None" and type_val == "None":
                data = MarkerRead("byowner", owner)
            elif owner == "None" and type_val != "None":
                data = MarkerRead("bytype", type_val)
            elif owner != "None" and type_val != "None":
                data = MarkerRead("byall", owner + "," + type_val)

            payload = jsonify(
                {
                    "success": True,
                    "data": data,
                }
            )

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


@app.route("/get/report", methods=["POST"])
@db_required
def Report():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    rType = content.get("report_type", "")
    rFormat = content.get("report_format", "")
    categoryFilter = content.get("category", None)

    try:
        table_data = GenerateReport(rType, rFormat, categoryFilter)
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


@app.route("/get/report/year/<string:type>", methods=["GET"])
@db_required
def YearReport(type):
    if type == "total":
        data = GetYearlyData("yeartotalrep")
    elif type == "expense":
        data = GetYearlyData("yearexprep")
    elif type == "income":
        data = GetYearlyData("yearincrep")
    return jsonify({"success": True, "data": data})


@app.route("/database/status", methods=["GET"])
def DBStatus():
    status = CheckDB()
    if status == 0:
        return jsonify({"success": True})
    elif status == 1:
        return jsonify({"success": False, "corrupt": False})
    else:
        return jsonify({"success": False, "corrupt": True})


@app.route("/database/create", methods=["POST"])
def DBCreate():
    try:
        NewDBase()
        print("Database created.")
        return (jsonify({"success": True}), 200)
    except Exception as e:
        print("Error: " + str(e))
        return (jsonify({"success": False, "message": f"{str(e)}"}))


@app.route("/spv", methods=["GET", "POST"])
def SPVControl():
    if request.method == "GET":
        try:
            expCat = read_csv(SPVcatExpPath)
            incCat = read_csv(SPVcatIncPath)
            subCat = read_csv(SPVsubcatPath)
            curr = read_csv(SPVcurrPath)
            data = {
                "currency": curr,
                "incomeCategories": incCat,
                "expenseCategories": expCat,
                "subCategories": subCat,
            }
            return jsonify(
                {
                    "success": True,
                    "data": data,
                }
            )
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

    elif request.method == "POST":
        content = request.get_json()
        if content is None:
            return "Error: No JSON data received", 400

        try:
            SPVconf("curr", content.get("curr", []))
            SPVconf("inccat", content.get("incCat", []))
            SPVconf("expcat", content.get("expCat", []))
            SPVconf("subcat", content.get("subCat", []))
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
