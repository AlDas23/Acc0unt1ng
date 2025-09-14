from flask import (
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
    Blueprint,
    jsonify,
)
from db_scripts.script import read_csv, Read
from db_scripts.consts import SPVstockPath, SPVcurrPath
from db_scripts.investScript import *

investPage = Blueprint("investPage", __name__)


@investPage.route("/invest", methods=["GET"])
def investMainPage():
    return redirect("/invest/add/transaction")


@investPage.route("/invest/add/transaction", methods=["GET", "POST"])
def investAddPage():
    if request.method == "POST":
        content = request.get_json()
        if content is None:
            return "Error: No JSON data received", 400

        # Parse JSON data into string line
        line = ",".join([str(content[key]) for key in content.keys()])

        try:
            if AddInvestTransaction(line) == -1:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Database has missing tables or does not exist",
                        }
                    ),
                    400,
                )
            return jsonify(
                {"success": True, "redirect_url": url_for("investPage.investAddPage")}
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

    if request.method == "GET":
        try:
            personBank = Read("retacc")
            investPB = ReadInvest("retipb")
            currency = read_csv(SPVcurrPath)
            stock = read_csv(SPVstockPath)
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

        options = {
            "personBank": personBank,
            "investPB": investPB,
            "currency": currency,
            "stock": stock,
        }

        data = GetTransactionHistory()

        # convert the data to a list of dictionaries
        history = []
        for row in data:
            history.append(
                {
                    "id": row[0],
                    "date": row[1],
                    "pb": row[2],
                    "amount": row[3],
                    "currency": row[4],
                    "ipbName": row[5],
                    "iAmount": row[6],
                    "stock": row[7],
                    "fee": row[8],
                    "stockPrice": row[9],
                }
            )

        return render_template(
            "investPages/investAdd.html",
            options=options,
            history=history,
        )


@investPage.route("/invest/add/stockPrice", methods=["GET", "POST"])
def investAddStockPricePage():
    if request.method == "POST":
        content = request.get_json()
        if content is None:
            return "Error: No JSON data received", 400

        # Parse JSON data into string line
        line = ",".join([str(content[key]) for key in content.keys()])

        try:
            if AddInvestStockPrice(line) == -1:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Database has missing tables or does not exist",
                        }
                    ),
                    400,
                )
            return jsonify(
                {
                    "success": True,
                    "redirect_url": url_for("investPage.investAddStockPricePage"),
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

    if request.method == "GET":
        try:
            stock = read_csv(SPVstockPath)
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

        options = {
            "stock": stock,
        }

        plot = GraphStockPrice()

        data = ReadInvest("stock")

        history = []
        for row in data:
            history.append(
                {
                    "id": row[0],
                    "date": row[1],
                    "stock": row[2],
                    "price": row[3],
                }
            )
        return render_template(
            "investPages/investStockPrice.html",
            options=options,
            history=history,
            graph=plot,
        )


@investPage.route("/invest/balance", methods=["GET"])
def investBalanceSheet():
    if request.method == "GET":
        try:
            data = CalculateBalance()

            return render_template(
                "investPages/investBalance.html",
                data=data,
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
