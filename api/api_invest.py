from flask import (
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
    Blueprint,
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
                return render_template_string(
                    "Error: Database has missing tables or does not exist"
                )
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return (
                render_template("error.html", error=f"Transaction failed: {str(e)}"),
                500,
            )
        return redirect(url_for("investPage.investAddPage"))

    if request.method == "GET":
        try:
            personBank = Read("retacc")
            investPB = ReadInvest("retipb")
            currency = read_csv(SPVcurrPath)
            stock = read_csv(SPVstockPath)
        except Exception as e:
            return render_template_string("Error: {{ error }}", error=str(e)), 500

        options = {
            "personBank": personBank,
            "investPB": investPB,
            "currency": currency,
            "stock": stock,
        }

        data = ReadInvest("alli")

        # convert the data to a list of dictionaries for easier rendering in HTML
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
                return render_template_string(
                    "Error: Database has missing tables or does not exist"
                )

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return (
                render_template("error.html", error=f"Transaction failed: {str(e)}"),
                500,
            )

        return redirect(url_for("investPage.investAddStockPricePage"))

    if request.method == "GET":
        try:
            stock = read_csv(SPVstockPath)
        except Exception as e:
            return render_template_string("Error: {{ error }}", error=str(e))

        options = {
            "stock": stock,
        }

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
        )


@investPage.route("/invest/balance", methods=["GET"])
def investBalanceSheet():
    # TODO: Bug where balance is not calculated and table is empty
    if request.method == "GET":
        try:
            data = CalculateBalance()

            return render_template(
                "investPages/investBalance.html",
                data=data,
            )
        except Exception as e:
            return render_template_string("Error: {{ error }}", error=str(e))
