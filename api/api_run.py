from flask import Flask, request, render_template
from db_scripts.script import *


app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def home():
    if (request.method == "GET"):
        return render_template("index.html")
    else:
        date = request.form.get("Date", "")
        sum_ = request.form.get("Sum", "")
        category = request.form.get("Category", "")
        sub_category = request.form.get("Sub-category", "")
        comment = request.form.get("Comment", "")
        person_bank = request.form.get("Person-Bank", "")
        currency = request.form.get("Currency", "")

        final_str = f"{date},{sum_},{category},{sub_category},"
        if not comment:
            final_str += ", ,"
        else:
            final_str += f"{comment},{person_bank}"
        final_str += f",{currency}"

        Add(final_str)
        return render_template("index.html")
        
def api_start():
    app.run(debug=True)