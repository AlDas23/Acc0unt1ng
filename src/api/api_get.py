from flask import (
    Blueprint,
    jsonify,
)
from db_scripts import consts
from db_scripts.SPVScripts import read_spv
from db_scripts.baseScripts import Re_Calculate_deposit, Read, ReadLegacy
from db_scripts.investScript import ReadInvest
from db_scripts.script import GetTransactionHistory
from helpers.configScripts import ReadBackupYears
from helpers.extras import ParseCurrRatesNames
from helpers.genPlot import CurrencyRatePlot, GraphStockPrice, plot_to_img_tag_legacy
from helpers.decorators import db_required

getEndpoints = Blueprint("getEndpoints", __name__)


@getEndpoints.route("/get/list/<string:source>", methods=["GET"])
@db_required
def GetList(source):
    try:
        if source == "categories_exp":
            expCategories = read_spv(consts.SPVcatExpPath)
            payload = jsonify(
                {
                    "success": True,
                    "categories": expCategories,
                }
            )
        elif source == "categories_inc":
            incCategories = read_spv(consts.SPVcatIncPath)
            payload = jsonify(
                {
                    "success": True,
                    "categories": incCategories,
                }
            )
        elif source == "subcategories":
            subCategories = read_spv(consts.SPVsubcatPath)
            payload = jsonify(
                {
                    "success": True,
                    "subcategories": subCategories,
                }
            )
        elif source == "currency":
            currencies = read_spv(consts.SPVcurrPath)
            payload = jsonify(
                {
                    "success": True,
                    "currencies": currencies,
                }
            )
        elif source == "stocks":
            stock = read_spv(consts.SPVstockPath)
            payload = jsonify(
                {
                    "success": True,
                    "stocks": stock,
                }
            )
        elif source == "currrateplotnames":
            originalCurrencies = [
                currency
                for currency in read_spv(consts.SPVcurrPath)
                if currency != consts.mainCurrency
            ]
            currRatePlotNames = Read("currratenamesinv")
            originalCurrencies.extend(
                f"{item}->{consts.mainCurrency}" for item in currRatePlotNames
            )
            payload = jsonify(
                {
                    "success": True,
                    "cuurrateplotnames": originalCurrencies,
                }
            )
        elif source == "pb":
            pb = Read("initpbnames")
            payload = jsonify(
                {
                    "success": True,
                    "data": pb,
                }
            )
        elif source == "markers":
            owners = Read("exowner")
            types = Read("extype")
            payload = jsonify(
                {"success": True, "data": {"owners": owners, "types": types}}
            )
        elif source == "exYears":
            years = ReadBackupYears()
            years.append(consts.currentYear)
            years = sorted(set(years), reverse=True)
            payload = jsonify({"success": True, "data": {"years": years}})
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


@getEndpoints.route("/get/options/<string:source>", methods=["GET"])
@db_required
def GetOptions(source):
    try:
        if source == "expense":
            categories = read_spv(consts.SPVcatExpPath)
            sub_categories = read_spv(consts.SPVsubcatPath)
            currencies = read_spv(consts.SPVcurrPath)
            person_banks = Read("retacc")
            options = {
                "categories": categories,
                "subcategories": sub_categories,
                "currency": currencies,
                "pb": person_banks,
            }

        elif source == "income":
            categories = read_spv(consts.SPVcatIncPath)
            currencies = read_spv(consts.SPVcurrPath)
            person_banks = Read("retacc")
            options = {
                "categories": categories,
                "currency": currencies,
                "pb": person_banks,
            }

        elif source == "transfer":
            currencies = read_spv(consts.SPVcurrPath)
            person_banks = Read("retacc")
            options = {
                "currency": currencies,
                "pb": person_banks,
            }

        elif source == "deposit":
            currencies = read_spv(consts.SPVcurrPath)
            person_banks = Read("retacc")
            options = {
                "currencies": currencies,
                "pb": person_banks,
            }

        elif source == "currencyrates":
            currencies = read_spv(consts.SPVcurrPath)
            options = {
                "currency": currencies,
            }

        elif source == "balance":
            ownersList = Read("retmowner")
            typesList = Read("retmtype")
            options = {"owner": ownersList, "type": typesList}

        elif source == "invest-transaction":
            stocks = read_spv(consts.SPVstockPath)
            currencies = read_spv(consts.SPVcurrPath)
            pb = Read("initpbnames")
            ipb = ReadInvest("ipb")
            options = {
                "stocks": stocks,
                "currency": currencies,
                "pb": pb,
                "ipb": ipb,
            }
        elif source == "invest-stockprice":
            stocks = read_spv(consts.SPVstockPath)
            currencies = read_spv(consts.SPVcurrPath)
            options = {
                "stocks": stocks,
                "currency": currencies,
            }

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

    return payload


@getEndpoints.route("/get/history/<string:source>/<string:year>", methods=["GET"])
@getEndpoints.route("/get/history/<string:source>", methods=["GET"])
@db_required
def GetHistory(source, year=consts.currentYear):
    try:
        if source == "expense":
            history = GetTransactionHistory("expense", year)
        elif source == "income":
            history = GetTransactionHistory("income", year)
        elif source == "transfer":
            history = GetTransactionHistory("transfer", year)
        elif source == "transferADV":
            history = GetTransactionHistory("advtransfer", year)
        elif source == "depositO":
            Re_Calculate_deposit()
            history = GetTransactionHistory("depositO", year)
        elif source == "depositC":
            history = GetTransactionHistory("depositC", year)
        elif source == "currencyrates":
            history = GetTransactionHistory("currencyrates", year)

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


@getEndpoints.route("/get/plot/<string:source>", methods=["GET"])
@getEndpoints.route("/get/plot/<string:source>/<string:filters>", methods=["GET"])
@db_required
def GetPlot(source, filters=None):
    try:
        if source == "currencyrates":
            if consts.isLegacyCurrencyRates:
                data = ReadLegacy("currrate")
                plot = plot_to_img_tag_legacy(
                    data, "Currency Rates Over Time", "Date", "Rate"
                )
            else:
                data = Read("currrateplot")
                data.extend(
                    ParseCurrRatesNames(Read("currrateplotinv"), consts.mainCurrency)
                )
                filterArr = filters.split("|")
                if filterArr == ["None"]:
                    filterArr = None
                plot = CurrencyRatePlot(data, filterArr)
            payload = jsonify({"success": True, "plot": plot})
        if source == "investstockprice":
            data = ReadInvest("graphstock")
            plot = GraphStockPrice(data)
            payload = jsonify({"success": True, "plot": plot})

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
