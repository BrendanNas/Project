from flask_app import app
from flask import render_template, redirect, session

@app.route("/")
def home():
    if session.get("user_id"):
        return redirect("/dashboard")
    return render_template("index.html")