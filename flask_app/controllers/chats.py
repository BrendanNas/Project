from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.chat import Chat

@app.route("/create/chats", methods=["POST"])
def create_chats():
    if not Chat.validate_chats(request.form):
        return redirect("/")
    else:
        Chat.save(request.form)
        return redirect("/dashboard")
    
@app.route("/chats/<int:id>")
def chats(id):
    data  = {
        "id": id
    }
    chat = Chat.get_by_id(data)
    return render_template("chat.html", chat = chat)

@app.route("/delete/chats/<int:id>")
def delete_chats(id):
    data = {
        "id": id
    }
    Chat.delete_chat(data)
    return redirect("/dashboard") 

@app.route("/edit/chats/<int:id>")
def update(id):
    data = {
        "id": id
    }
    chat= Chat.get_by_id(data)
    return render_template("chat.html", chat = chat, id = id)

@app.route("/edit/chats/<int:id>", methods = ["POST"])
def edit_chats(id):
    Chat.update(request.form, id)
    return redirect (f"/chats/{id}")