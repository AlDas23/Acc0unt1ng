from flask import Flask, request, render_template
from db_scripts.script import *


app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def home():
    if (request.method == "GET"):
        return render_template("index.html")
    else:
        final_str = request.form["Date"]
        final_str = final_str + "," + request.form["Sum"]
        final_str = final_str + "," + request.form["Category"]
        final_str = final_str + "," + request.form["Sub-category"]
        if (request.form["Comment"] == None):
            final_str = final_str + ", ,"
        else:
            final_str = final_str + "," + request.form["Person-Bank"]
        final_str = final_str + "," + request.form["Currency"]
        Add(final_str)
        
def api_start():
    app.run(debug=True)