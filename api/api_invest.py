from flask import (
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
)
from api_run import app
from db_scripts.script import read_csv, Read
from db_scripts.consts import SPVstockPath, SPVcurrPath
from db_scripts.investScript import *


@app.route("/invest", methods=["GET"])
def investMainPage():
    return redirect("investPages/investAdd.html")


@app.route("/invest/add/transaction", methods=["GET, POST"])
def investAddPage():
    if request.method == "POST":
        content = request.get_json()
        if content is None:
            return "Error: No JSON data received", 400

        # Parse JSON data into string line
        line = ",".join([str(content[key]) for key in content.keys()])

        try:
            result = AddInvestTransaction(line)
            if result == -1:
                return render_template_string(
                    "Error: Database has missing tables or does not exist"
                )
            elif result == 0:
                return url_for("investAddPage")
        except Exception as e:
            return render_template_string("Error: {{ error }}", error=str(e))

    if request.method == "GET":
        try:
            personBank = Read("retacc")
            investPB = ReadInvest("ipb")
            currency = read_csv(SPVcurrPath)
            stock = read_csv(SPVstockPath)
        except Exception as e:
            return render_template_string("Error: {{ error }}", error=str(e))

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

        render_template(
            "investPages/investAdd.html",
            options=options,
            history=history,
        )

    return render_template("investPages/investAdd.html")


@app.route("/invest/add/stockPrice", methods=["GET", "POST"])
def investAddStockPricePage():
    if request.method == "POST":
        content = request.get_json()
        if content is None:
            return "Error: No JSON data received", 400

        # Parse JSON data into string line
        line = ",".join([str(content[key]) for key in content.keys()])

        try:
            result = AddInvestStockPrice(line)
            if result == -1:
                return render_template_string(
                    "Error: Database has missing tables or does not exist"
                )
            elif result == 0:
                return url_for("investAddStockPricePage")
        except Exception as e:
            return render_template_string("Error: {{ error }}", error=str(e))

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


@app.route("/invest/balance", methods=["GET"])
def investBalanceSheet():
    if request.method == "GET":
        try:
            data = CalculateBalance()

            return render_template(
                "investPages/investBalance.html",
                data=data,
            )
        except Exception as e:
            return render_template_string("Error: {{ error }}", error=str(e))
