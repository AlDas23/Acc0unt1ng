from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    render_template_string,
)
from api_run import app

@app.route("/invest", methods=["GET"])
def investMainPage():
    return redirect("investPages/investAdd.html")

@app.route("/invest/add", methods=["GET, POST"])
def investAddPage():
    if request.method == "POST":
        pass
        # TODO: Add the logic to handle the form submission here
        
    if request.method == "GET":
        pass
        # TODO: Add the logic to handle the GET request here

    return render_template("investPages/investAdd.html")