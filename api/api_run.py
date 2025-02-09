from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
)
import base64
import io
import matplotlib.pyplot as plt
from db_scripts.script import *
from db_scripts.consts import *


app = Flask(__name__)


def plot_to_img_tag(df):
    plt.figure(figsize=(10, 5))
    # Plot each currency's rate over time
    for currency in df.columns[1:]:  # Skip the 'date' column
        plt.plot(df["date"], df[currency], marker="o", label=currency)
    plt.title("Currency Rates Over Time")
    plt.xlabel("Date")
    plt.ylabel("Rate")
    plt.legend()
    plt.grid(True)
    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    # Encode image to base64 string
    img_tag = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return img_tag


@app.route("/", methods=["POST", "GET"])
def main():
    Re_Calculate_deposit()
    return redirect("/add/expense")


@app.route("/add/expense", methods=["POST", "GET"])
def Expense():
    if request.method == "GET":
        try:
            categories = read_csv(SPVcatExpPath)
            sub_categories = read_csv(SPVsubcatPath)
            currencies = read_csv(SPVcurrPath)
        except:
            return render_template_string(
                "<h1>Missing or inaccesible csv with special values!</h1><p>Please check csv files and try again</p>"
            )
        try:
            person_banks = Read("retacc")
        except:
            return render_template_string(
                "<h1>Missing or inaccesible database file!</h1><p>Please check or re-create database and try again</p>"
            )
        options = {
            "categories": categories,
            "sub_categories": sub_categories,
            "person_banks": person_banks,
            "currencies": currencies,
        }

        data = Read("m-")
        columns = [
            "ID",
            "Date",
            "Category",
            "Sub-category",
            "Person bank",
            "Sum",
            "Currency",
            "Comment",
        ]

        return render_template(
            "addexp.html", options=options, columns=columns, data=data
        )

    else:
        date = request.form.get("Date", "")
        category = request.form.get("Category", "")
        sub_category = request.form.get("Sub-category", "")
        person_bank = request.form.get("Person-Bank", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")

        # Check if comment is empty and assign a whitespace if it is
        if not comment:
            comment = " "

        # Insert minus to expense sum
        sum = "-" + sum

        final_str = (
            f"{date},{category},{sub_category},{person_bank},{sum},{currency},{comment}"
        )

        try:
            Add(final_str, "main")
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("Expense"))


@app.route("/edit/expense/<int:id>", methods=["GET", "POST"])
def EditExpense(id):
    if request.method == "GET":
        # Fetch the existing record by ID
        record = GrabRecordByID(id, "exp")
        if record:
            categories = read_csv(SPVcatExpPath)
            sub_categories = read_csv(SPVsubcatPath)
            person_banks = Read("retacc")
            currencies = read_csv(SPVcurrPath)
            options = {
                "categories": categories,
                "sub_categories": sub_categories,
                "person_banks": person_banks,
                "currencies": currencies,
            }
            columns = [
                "ID",
                "Date",
                "Category",
                "Sub-category",
                "Person bank",
                "Sum",
                "Currency",
                "Comment",
            ]
            data = record

            return render_template(
                "addexp.html",
                options=options,
                edit_record=record,
                columns=columns,
                data=data,
            )
        else:
            return "Record not found", 404

    else:
        # Update the existing record
        date = request.form.get("Date", "")
        category = request.form.get("Category", "")
        sub_category = request.form.get("Sub-category", "")
        person_bank = request.form.get("Person-Bank", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")

        # Check if comment is empty and assign a whitespace if it is
        if not comment:
            comment = " "

        if not sub_category:
            sub_category = " "

        # Insert minus to expense sum
        sum = "-" + sum

        final_str = f"{id},{date},{category},{sub_category},{person_bank},{sum},{currency},{comment}"

        try:
            UpdateRecord(final_str)
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to update record!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("Expense"))


@app.route("/add/income", methods=["POST", "GET"])
def Income():
    if request.method == "GET":
        categories = read_csv(SPVcatIncPath)
        currencies = read_csv(SPVcurrPath)
        person_banks = Read("retacc")

        options = {
            "categories": categories,
            "person_banks": person_banks,
            "currencies": currencies,
        }

        data = Read("m+")
        columns = [
            "ID",
            "Date",
            "Category",
            "Person bank",
            "Sum",
            "Currency",
            "Comment",
        ]

        return render_template(
            "addinc.html", options=options, columns=columns, data=data
        )
    else:
        date = request.form.get("Date", "")
        category = request.form.get("Category", "")
        sub_category = request.form.get("Sub-category", "")
        person_bank = request.form.get("Person-Bank", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")

        # Check if comment is empty and assign a whitespace if it is
        if not comment:
            comment = " "

        final_str = (
            f"{date},{category},{sub_category},{person_bank},{sum},{currency},{comment}"
        )

        try:
            Add(final_str, "main")
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("Income"))


@app.route("/edit/income/<int:id>", methods=["GET", "POST"])
def EditIncome(id):
    if request.method == "GET":
        # Fetch the existing record by ID
        record = GrabRecordByID(id, "inc")
        if record:
            categories = read_csv(SPVcatIncPath)
            person_banks = Read("retacc")
            currencies = read_csv(SPVcurrPath)
            options = {
                "categories": categories,
                "person_banks": person_banks,
                "currencies": currencies,
            }
            columns = [
                "ID",
                "Date",
                "Category",
                "Person bank",
                "Sum",
                "Currency",
                "Comment",
            ]
            data = record

            return render_template(
                "addinc.html",
                options=options,
                edit_record=record,
                columns=columns,
                data=data,
            )
        else:
            return "Record not found", 404

    else:
        # Update the existing record
        date = request.form.get("Date", "")
        category = request.form.get("Category", "")
        person_bank = request.form.get("Person-Bank", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")

        # Check if comment is empty and assign a whitespace if it is
        if not comment:
            comment = " "

        final_str = f"{id},{date},{category}, ,{person_bank},{sum},{currency},{comment}"

        try:
            UpdateRecord(final_str)
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to update record!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("Income"))


@app.route("/transfer", methods=["POST", "GET"])
def Transfer():
    if request.method == "GET":
        currencies = read_csv(SPVcurrPath)
        person_banks = Read("retacc")

        options = {"person_banks": person_banks, "currencies": currencies}

        data = Read("alltran")
        columns = ["ID", "Date", "Sender", "Receiver", "Sum", "Currency", "Comment"]
        dataA = Read("alladvtran")
        columnsA = [
            "ID",
            "Date",
            "Sender",
            "Sum",
            "Currency",
            "Receiver",
            "Sum",
            "Currency",
            "Currency rate",
            "Comment",
        ]

        return render_template(
            "transfer.html",
            options=options,
            columns=columns,
            data=data,
            dataA=dataA,
            columnsA=columnsA,
        )
    else:
        form_id = request.form.get("form_type")
        if form_id == "transfer":
            date = request.form.get("Date", "")
            sender = request.form.get("Sender", "")
            receiver = request.form.get("Receiver", "")
            comment = request.form.get("Comment", "")
            sum = request.form.get("Sum", "")
            currency = request.form.get("Currency", "")

            # Check if comment is empty and assign a whitespace if it is
            if not comment:
                comment = " "

            final_str = f"{date},{sender},{receiver},{sum},{currency},{comment}"

            try:
                Add(final_str, "transfer")
            except Exception as e:
                # Capture the exception message
                error_message = str(e)
                # Return the error message in the response
                return render_template_string(
                    "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                    error_message=error_message,
                )

            return redirect(url_for("Transfer"))

        elif form_id == "advtransfer":
            date = request.form.get("Date", "")
            sender = request.form.get("Sender", "")
            ssum = request.form.get("SSum", "")
            scurr = request.form.get("SCurrency", "")
            receiver = request.form.get("Receiver", "")
            rsum = request.form.get("RSum", "")
            rcurr = request.form.get("RCurrency", "")
            curr_rate = request.form.get("Currency rate", "")
            comment = request.form.get("Comment", "")

            # Check if comment is empty and assign a whitespace if it is
            if not comment:
                comment = " "

            final_str = f"{date},{sender},{ssum},{scurr},{receiver},{rsum},{rcurr},{curr_rate},{comment}"

            try:
                Add(final_str, "advtransfer")
            except Exception as e:
                # Capture the exception message
                error_message = str(e)
                # Return the error message in the response
                return render_template_string(
                    "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                    error_message=error_message,
                )

            return redirect(url_for("Transfer"))


@app.route("/add/deposit", methods=["POST", "GET"])
def AddDeposit():
    if request.method == "GET":
        

        currencies = read_csv(SPVcurrPath)
        person_banks = Read("retacc")

        options = {"person_banks": person_banks, "currencies": currencies}

        # data = Read("alldepacc")
        # columns = ["Name", "Owner", "Sum", "Currency"]

        dataA = Read("opendep")
        columnsH = [
            "Deposit Date",
            "Name",
            "Person-bank",
            "Sum",
            "Currency",
            "Months",
            "Closing Date",
            "%",
            "Currency rate",
            "Expected amount",
            "Comment",
        ]
        dataC = Read("closeddep")

        return render_template(
            "adddeposit.html",
            options=options,
            columnsA=columnsH,
            dataA=dataA,
            columnsC=columnsH,
            dataC=dataC,
        )
    else:
        dateIn = request.form.get("DateIn", "")
        name = request.form.get("Name", "")
        owner = request.form.get("Owner", "")
        comment = request.form.get("Comment", "")
        sum = request.form.get("Sum", "")
        currency = request.form.get("Currency", "")
        months = request.form.get("Months", "")
        dateOut = request.form.get("DateOut", "")
        percent = request.form.get("Percent", "")
        currRate = request.form.get("Currency rate", "")

        # Check fields if empty and assign a whitespace if they are
        if not comment:
            comment = " "
        if not months:
            months = " "
        if not dateOut:
            dateOut = " "
        if not currRate:
            currRate = " "

        final_str = f"{dateIn},{name},{owner},{sum},{currency},{months},{dateOut},{percent},{currRate},{comment}"

        try:
            Add(final_str, "deposit")
        except Exception as e:
            # Capture the exception message
            error_message = str(e)
            # Return the error message in the response
            return render_template_string(
                "<h1>Failed to add record!</h1><p>{{ error_message }}</p>",
                error_message=error_message,
            )

        return redirect(url_for("AddDeposit"))


@app.route("/view/rep", methods=["GET"])
def ViewReports():
    currencies = read_csv(SPVcurrPath)

    Ldata = Read("yeartotalrep")
    Lcolumns = ["Month", "Expenses", "Incomes", "Balance"]
    Cdata = Read("yearexprep")
    Ccolumns = ["Month"] + currencies + ["Total in RON"]
    Rdata = Read("yearincrep")
    Rcolumns = ["Month"] + currencies + ["Total in RON"]

    return render_template(
        "viewrep.html",
        Lcolumns=Lcolumns,
        Ldata=Ldata,
        Ccolumns=Ccolumns,
        Cdata=Cdata,
        Rcolumns=Rcolumns,
        Rdata=Rdata,
    )


@app.route("/view/advrep", methods=["POST", "GET"])
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
    data_curr = ConvRead("norm", "allcurr", True)
    columns_curr = ["Currency", "Sum", "%"]
    data_owner = ConvReadPlus("norm", "allmowner")
    columns_owner = ["Owner", "Currency", "Sum", "Sum RON"]
    data_type = ConvRead("norm", "allmtype", True)
    columns_type = ["Type", "Sum RON", "%"]
    owners = Read("retmowner")
    types = Read("retmtype")
    options = {"owners": owners, "types": types}

    if request.method == "GET":
        return render_template(
            "viewacc.html",
            data_curr=data_curr,
            columns_curr=columns_curr,
            data_owner=data_owner,
            columns_owner=columns_owner,
            data_type=data_type,
            columns_type=columns_type,
            options=options,
        )
    else:
        owner = request.form["Acc owner"]
        type = request.form["Acc type"]

        if type == " " and owner != " ":
            data = MarkerRead(owner, "byowner")

        elif owner == " " and type != " ":
            data = MarkerRead(type, "bytype")

        elif owner != " " and type != " ":
            all = owner + "," + type
            data = MarkerRead(all, "byall")
        else:
            return redirect(url_for("ViewAcc"))

        return render_template(
            "viewacc.html",
            data_curr=data_curr,
            columns_curr=columns_curr,
            data_owner=data_owner,
            columns_owner=columns_owner,
            data_type=data_type,
            columns_type=columns_type,
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
        columns = ["Date", "RON", "UAH", "EUR", "USD", "GBP", "CHF", "HUF", "AUR"]
        df = Read("retcurrr")
        plot1 = plot_to_img_tag(df)
        df = Read("retcurraur")
        plot2 = plot_to_img_tag(df)

        return render_template(
            "currencies.html", columns=columns, data=data, plot1=plot1, plot2=plot2
        )

    else:
        date = request.form["Date"]
        ron = request.form["RON"]
        eur = request.form["EUR"]
        usd = request.form["USD"]
        gbp = request.form["GBP"]
        chf = request.form["CHF"]
        huf = request.form["HUF"]
        aur = request.form["AUR"]

        final_str = f"{date},{ron},{eur},{usd},{gbp},{chf},{huf},{aur}"

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
    
@app.route("/reports", methods=["GET", "POST"])
def ReportsPage():
    if request.method == "GET":
        return render_template("reportsPage.html")
        
    else:
        ## TODO: Finish reports page backend logic
        pass


@app.route("/api", methods=["GET"])
def APIHome():
    return redirect("/api/help")


@app.route("/api/help", methods=["GET"])
def APIHelp():
    return """
API - Help message:

Go to /api/read for Read functions.
Go to /api/conf/mark to configure Markers.
Go to /api/conf/spv to configure SPVs and account initialization function.
Go to /api/conf/spv/read to read existing SPVs.
    """


@app.route("/api/read", methods=["GET", "POST"])
def APIRead():
    if request.method == "GET":
        return """
API - Read message:

Make a POST request on this adress with in next format:

       Key  |          Value
    -----------------------------------
    Command | *Command from list below*

Possible commands are:
    allm        - show all records from main table
    m+          - show positive records from main table
    m-          - show negative records from main table
    allacc      - show all accounts
    initpb      - show all initial accounts
    alldepacc   - show all deposit accounts
    alldep      - show all deposit records
    opendep     - show deposit records that considered open
    closeddep   - show deposit records that considered closed
    alltran     - show all standard transfer records
    alladvtran  - show all advanced transfer records  
    allcurrrate - show all currency rates records 
    mtype       - show all type markers
    mowner      - show all owner markers
    allmtype    - show all accounts grouped by type Marker
    allmowner   - show all accounts grouped by owner Marker
    exowner     - show existing owner Markers
    extype      - show existing type Markers
        """
    elif request.method == "POST":
        command = request.form.get("Command")
        if not command:
            return "Command not provided!", 400
        response = Read(command)
        if response is None:
            return "Unknown command!"
        else:
            return response


@app.route("/api/conf", methods=["GET"])
def APIConf():
    if request.method == "GET":
        return "You are not suppsed to be here pal."


@app.route("/api/conf/mark", methods=["GET", "POST"])
def APIConfMark():
    if request.method == "GET":
        return """
API - Configuration - Mark message:

Make a POST request on this adress with in next format:
    
      Key  |                      Value
    ----------------------------------------------------------
    Type   | [owner, type]
    BR     | *person_bank of account or deposit account name*
    Marker | *Marker value*
        """
    else:
        mode = request.form.get("Type")
        br = request.form.get("BR")
        marker = request.form.get("Marker")

        # Check if any of the required form data is missing
        if not mode or not br or not marker:
            return "Missing one or more required fields: 'Type', 'BR', 'Marker'", 400

        to_send = br + "," + marker
        try:
            Mark(to_send, mode)
        except:
            return "Wrong POST format!"
        finally:
            return "Mark success!"


@app.route("/api/conf/spv", methods=["GET", "POST"])
def APIConfSPV():
    if request.method == "GET":
        return """
API - Configuration - SPV message:

Commands available for POST are:
    catinc  - income categories
    catexp  - expense categories
    subcat  - sub-categories (expense)
    curr    - currencies 
    initpb  - Initialize account
    delpb   - Delete account. !WARNING!, dangerous function

Make a POST request on this adress with in next format:
    
        Key   |                     Value
    ----------------------------------------------------------
    Command   | *From commands above*
    SPVLine   | *For SPV values in format: str1,str2,...*  
    Mode      | *For SPV values, [A]ppend or [R]eplace list* 
    PB        | *Person_bank value*
    Sum       | *Only applicable with initpb*
    Currency  | *Currency value*
        """
    else:
        command = request.form.get("Command")
        SPVLine = request.form.get("SPVLine")
        mode = request.form.get("Mode")
        pb = request.form.get("PB")
        sum = request.form.get("Sum")
        currency = request.form.get("Currency")

        if sum != None:
            to_send = pb + "," + sum + "," + currency
        else:
            to_send = pb + "," + currency # TODO CBug: When using delpb command TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'

        try:
            if (
                command == "catinc"
                or command == "catexp"
                or command == "subcat"
                or command == "curr"
            ):
                SPVconf(command, SPVLine)
            elif command == "initpb":
                InitPB(to_send)
            elif command == "delpb":
                DelPB(to_send)
            else:
                raise Exception("Wrong POST format!")
        except:
            return "Wrong POST format!"
        finally:
            return "Success!"


@app.route("/api/conf/spv/read", methods=["GET", "POST"])
def APIConfSPVRead():
    if request.method == "GET":
        return """
API - Configuration - SPV - Read message:

Make a POST request on this adress with in next format:
    
        Key   |         Value
    -----------------------------------
    Read      | *From values below*
    
    
Possible values:
    catinc - income categories
    catexp - expense categories
    subcat - sub-categories (expense)
    curr   - currencies 
    
        """
    else:
        mode = request.form.get("Read")

        try:
            return ShowExistingSPVAPI(mode)
        except:
            return "Wrong POST format!"


def api_start():
    app.run(debug=True)
