from flask import Flask, jsonify, request
from flask_cors import CORS
from db_scripts.script import (
    DeleteRecord,
    UpdateRecord,
    GenerateReport,
    GetYearlyData,
    GenerateTable,
    ConvRead,
    ConvReadPlus,
)
from db_scripts.baseScripts import (
    Add,
    InitPB,
    Mark,
    MarkerRead,
    Re_Calculate_deposit,
    Read,
)
from db_scripts.dbScripts import CheckDB, NewDBase, UpdateDB as UDB, UpdateDBYear
from db_scripts.SPVScripts import SPVconf, read_spv
import db_scripts.consts as consts
from helpers.configScripts import ModifyConfigSettings, ReadCurrentYear
from helpers.decorators import db_required
from helpers.extras import GetCurrentYear
from api.api_invest import investEndpoints
from api.api_get import getEndpoints

app = Flask(__name__)
app.register_blueprint(investEndpoints, url_prefix="/")
app.register_blueprint(getEndpoints, url_prefix="/")
CORS(app, resources=r"/*")


@app.route("/health", methods=["GET"])
def health_check():
    consts.currentYear = GetCurrentYear()
    if not ReadCurrentYear(consts.currentYear):
        UpdateDBYear()

    return jsonify({"status": "ok"}), 200


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

    if content.get("toDelete"):
        try:
            DeleteRecord(str(id), "main")
            return jsonify({"success": True})
        except Exception as e:
            print(f"Error occurred while deleting: {str(e)}")
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
                data_curr2 = Read("allcurr", str(consts.currentYear))

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
    yearFilter = content.get("report_year", consts.currentYear)

    try:
        table_data = GenerateReport(rType, rFormat, categoryFilter, yearFilter)
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


@app.route("/get/report/year/<string:type>/<string:year>", methods=["GET"])
@db_required
def YearReport(type, year):
    if type == "total":
        data = GetYearlyData("yeartotalrep", year)
    elif type == "expense":
        data = GetYearlyData("yearexprep", year)
    elif type == "income":
        data = GetYearlyData("yearincrep", year)
    return jsonify({"success": True, "data": data})


@app.route("/database/status", methods=["GET"])
def DBStatus():
    status = CheckDB()
    if status == 0:
        return jsonify({"success": True})
    elif status == 1:
        return jsonify({"success": False, "corrupt": False})
    elif status == 2 or status == 3:
        return jsonify({"success": False, "corrupt": True})
    elif status < 0:
        return jsonify({"success": True, "legacy": True})


@app.route("/database/create", methods=["POST"])
def DBCreate():
    try:
        NewDBase()
        print("Database created.")
        return (jsonify({"success": True}), 200)
    except Exception as e:
        print("Error: " + str(e))
        return jsonify({"success": False, "message": f"{str(e)}"})


@app.route("/spv", methods=["GET", "POST"])
def SPVControl():
    if request.method == "GET":
        try:
            expCat = read_spv(consts.SPVcatExpPath)
            incCat = read_spv(consts.SPVcatIncPath)
            subCat = read_spv(consts.SPVsubcatPath)
            curr = read_spv(consts.SPVcurrPath)
            data = {
                "currency": curr,
                "incomeCategories": incCat,
                "expenseCategories": expCat,
                "subCategories": subCat,
                "mainCurrency": consts.mainCurrency,
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
            SPVconf("currencies", content.get("curr", []))
            SPVconf("inc-categories", content.get("incCat", []))
            SPVconf("exp-categories", content.get("expCat", []))
            SPVconf("sub-categories", content.get("subCat", []))
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


@app.route("/spv/maincurrency", methods=["POST"])
def SPVMainCurrency():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    try:
        ModifyConfigSettings("main_currency", content["mainCurrency"])
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


@app.route("/spv/pb/add", methods=["POST"])
def AddPB():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    try:
        InitPB(content["PersonBank"], content["Sum"], content["Currency"])
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


@app.route("/spv/mark", methods=["POST"])
def MarkPB():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    try:
        Mark(content["PersonBank"], content["Owner"], content["Type"])
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


@app.route("/database/update", methods=["POST"])
def UpdateDB():
    try:
        UDB("exc_rate")
        print("Database updated.")
        return (jsonify({"success": True}), 200)
    except Exception as e:
        print("Error: " + str(e))
        return jsonify({"success": False, "message": f"{str(e)}"})
