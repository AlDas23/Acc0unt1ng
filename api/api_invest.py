from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
)
from api_run import app
from db_scripts.script import read_csv, Read
from db_scripts.consts import SPVstockPath, SPVcurrPath
from db_scripts.investScript import ReadInvest


@app.route("/invest", methods=["GET"])
def investMainPage():
    return redirect("investPages/investAdd.html")


@app.route("/invest/add", methods=["GET, POST"])
def investAddPage():
    if request.method == "POST":
        pass
        # TODO: Add the logic to handle the form submission here

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
            history.append({
                "id": row[0],
                "date": row[1],
                "pb": row[2],
                "amount": row[3],
                "currency": row[4],
                "ipbName": row[5],
                "iAmount": row[6],
                "stock": row[7],
            })

        render_template(
            "investPages/investAdd.html",
            options=options,
            history=history,
        )

    return render_template("investPages/investAdd.html")
