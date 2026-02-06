from flask import (
    request,
    Blueprint,
    jsonify,
)
from db_scripts.SPVScripts import SPVconf, read_spv
import db_scripts.consts as consts
from db_scripts.investScript import (
    AddInvestStockPrice,
    CalculateBalance,
    GetInvestTransactionHistory,
    AddInvestTransaction,
    InitInvestPB,
    ReadInvest,
)
from helpers.decorators import db_required

investEndpoints = Blueprint("investEndpoints", __name__)


@investEndpoints.route(
    "/get/invest/history/<string:source>/<string:year>", methods=["GET"]
)
@investEndpoints.route("/get/invest/history/<string:source>", methods=["GET"])
@db_required
def InvestGetHistory(source, year=consts.currentYear):
    try:
        if source != "transactions":
            history = GetInvestTransactionHistory("main", year)
        elif source == "stockprice":
            history = GetInvestTransactionHistory("stock", year)

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
    return payload


@investEndpoints.route("/get/ilist/<string:source>", methods=["GET"])
@db_required
def InvestGetList(source):
    try:
        if source == "ipb":
            ilist = ReadInvest("ipb")

        payload = jsonify(
            {
                "success": True,
                "ilist": ilist,
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

    return payload


@investEndpoints.route("/add/invest/transaction", methods=["POST"])
def InvestAddTransaction():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    try:
        AddInvestTransaction(content)
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


@investEndpoints.route("/add/invest/stockprice", methods=["POST"])
def InvestAddStockPrice():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    try:
        AddInvestStockPrice(content)
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


@investEndpoints.route("/get/invest/balance", methods=["GET"])
@db_required
def InvestBalanceSheet():
    try:
        data = CalculateBalance()
        return jsonify(
            {
                "success": True,
                "balance": data,
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


@investEndpoints.route("spv/invest", methods=["GET", "POST"])
def InvestSPVControl():
    if request.method == "GET":
        try:
            stocks = read_spv(consts.SPVstockPath)
            data = {
                "stocks": stocks,
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
            SPVconf("stocks", content.get["stocks", []])
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


@investEndpoints.route("/spv/ipb/add", methods=["POST"])
def AddIPB():
    content = request.get_json()
    if content is None:
        return "Error: No JSON data received", 400

    try:
        InitInvestPB(content["InvestPB"], content["Stock"])
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
