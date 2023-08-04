from app import app, socketio
from flask import render_template, session, request, redirect, url_for
from flask_socketio import send, join_room, leave_room
import random
from string import ascii_uppercase
from flask_login import current_user, login_required
from datetime import datetime
from app.util import moderator


rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length+1):
            if _ == 3:
                code += '-'
            else:
                code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/chats", methods=["POST", "GET"])
@login_required
def chats():
    if request.method == "POST":

        # if current_user.is_authenticated:
        #     name = current_user.username
        # else:
        #     name = 'Anonymous'

        name = current_user.username

        code = request.form.get("code")

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

    room = generate_unique_code(6)
    rooms[room] = {"members": 0, "messages": []}

    session["room"] = room
    session["name"] = current_user.username
    
    return redirect(url_for("room"))


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("chats"))

    return render_template("chat_room.html", code=room, messages=rooms[room]["messages"], user=current_user)

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    msg = moderator.moderate_msg(data['data'])
    
    content = {
        "name": session.get("name"),
        "message": msg,
        "timestamp": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room", "timestamp": timestamp, "sysgen": True}, to=room)
    rooms[room]["members"] += 1


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room", "timestamp": timestamp, "sysgen": True}, to=room)