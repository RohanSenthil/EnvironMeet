from app import app, socketio
from flask import render_template, session, request, redirect, url_for
from flask_socketio import send, join_room, leave_room
import random
from string import ascii_uppercase
from flask_login import current_user, login_required
import uuid


rooms = {}

def generate_unique_code():
    return uuid.uuid4().hex
    # while True:
    #     code = ""
    #     for _ in range(length):
    #         code += random.choice(ascii_uppercase)
        
    #     if code not in rooms:
    #         break
    
    # return code

@app.route("/chats", methods=["POST", "GET"])
def chats():
    if request.method == "POST":

        if current_user.is_authenticated:
            name = current_user.username
        else:
            name = 'Anonymous'

        code = request.form.get("code")

        if not name:
            return render_template("chats.html", error="Please enter a name.", code=code, name=name)

        if not code:
            return render_template("chats.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        
        if code not in rooms:
            return render_template("chats.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name

        return redirect(url_for("room"))

    return render_template("chats.html")


@app.route("/chats/create", methods=['POST'])
@login_required
def create_chat():

    room = generate_unique_code()
    rooms[room] = {"members": 0, "messages": []}

    session["room"] = room
    session["name"] = current_user.username
    
    return redirect(url_for("room"))


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("chats"))

    return render_template("chat_room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")