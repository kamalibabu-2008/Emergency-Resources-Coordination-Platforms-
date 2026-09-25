"""
ResQLink backend
Run:
    pip install flask flask-cors
    python app.py

Then open:
    http://127.0.0.1:5000/

This is a simple SQLite-backed hackathon backend.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3, os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "resqlink.db")

app = Flask(__name__, static_folder=BASE)
CORS(app)

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS incidents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        location TEXT NOT NULL,
        priority TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'New',
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource TEXT NOT NULL,
        location TEXT NOT NULL,
        priority TEXT NOT NULL,
        people INTEGER NOT NULL,
        status TEXT DEFAULT 'Pending',
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS volunteers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        skill TEXT NOT NULL,
        availability TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS sos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        message TEXT,
        created_at TEXT NOT NULL
    );
    """)
    con.commit()
    con.close()

def now():
    return datetime.now().isoformat(timespec="seconds")

@app.get("/")
def home():
    return send_from_directory(BASE, "index.html")

@app.get("/api/health")
def health():
    return jsonify(ok=True, service="ResQLink API")

@app.get("/api/incidents")
def incidents():
    con=db()
    rows=con.execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])

@app.post("/api/incidents")
def create_incident():
    data=request.get_json(force=True)
    required=["type","location","priority"]
    if any(not data.get(x) for x in required):
        return jsonify(error="type, location and priority are required"),400
    con=db()
    cur=con.execute("""INSERT INTO incidents(type,location,priority,description,created_at)
                       VALUES(?,?,?,?,?)""",
                    (data["type"],data["location"],data["priority"],
                     data.get("description",""),now()))
    con.commit()
    row=con.execute("SELECT * FROM incidents WHERE id=?",(cur.lastrowid,)).fetchone()
    con.close()
    return jsonify(dict(row)),201

@app.patch("/api/incidents/<int:item_id>")
def update_incident(item_id):
    data=request.get_json(force=True)
    status=data.get("status")
    if not status: return jsonify(error="status required"),400
    con=db()
    con.execute("UPDATE incidents SET status=? WHERE id=?",(status,item_id))
    con.commit()
    row=con.execute("SELECT * FROM incidents WHERE id=?",(item_id,)).fetchone()
    con.close()
    return jsonify(dict(row)) if row else (jsonify(error="not found"),404)

@app.get("/api/requests")
def requests_list():
    con=db()
    rows=con.execute("SELECT * FROM requests ORDER BY id DESC").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])

@app.post("/api/requests")
def create_request():
    data=request.get_json(force=True)
    required=["resource","location","priority","people"]
    if any(data.get(x) in (None,"") for x in required):
        return jsonify(error="resource, location, priority and people are required"),400
    con=db()
    cur=con.execute("""INSERT INTO requests(resource,location,priority,people,created_at)
                       VALUES(?,?,?,?,?)""",
                    (data["resource"],data["location"],data["priority"],
                     int(data["people"]),now()))
    con.commit()
    row=con.execute("SELECT * FROM requests WHERE id=?",(cur.lastrowid,)).fetchone()
    con.close()
    return jsonify(dict(row)),201

@app.patch("/api/requests/<int:item_id>")
def update_request(item_id):
    data=request.get_json(force=True)
    status=data.get("status")
    if not status: return jsonify(error="status required"),400
    con=db()
    con.execute("UPDATE requests SET status=? WHERE id=?",(status,item_id))
    con.commit()
    row=con.execute("SELECT * FROM requests WHERE id=?",(item_id,)).fetchone()
    con.close()
    return jsonify(dict(row)) if row else (jsonify(error="not found"),404)

@app.get("/api/volunteers")
def volunteers():
    con=db()
    rows=con.execute("SELECT * FROM volunteers ORDER BY id DESC").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])

@app.post("/api/volunteers")
def create_volunteer():
    data=request.get_json(force=True)
    required=["name","phone","skill","availability"]
    if any(not data.get(x) for x in required):
        return jsonify(error="all volunteer fields are required"),400
    con=db()
    cur=con.execute("""INSERT INTO volunteers(name,phone,skill,availability,created_at)
                       VALUES(?,?,?,?,?)""",
                    (data["name"],data["phone"],data["skill"],data["availability"],now()))
    con.commit()
    row=con.execute("SELECT * FROM volunteers WHERE id=?",(cur.lastrowid,)).fetchone()
    con.close()
    return jsonify(dict(row)),201

@app.post("/api/sos")
def create_sos():
    data=request.get_json(force=True)
    con=db()
    cur=con.execute("INSERT INTO sos(location,message,created_at) VALUES(?,?,?)",
                    (data.get("location","Unknown"),data.get("message","Immediate assistance required"),now()))
    con.commit()
    row=con.execute("SELECT * FROM sos WHERE id=?",(cur.lastrowid,)).fetchone()
    con.close()
    return jsonify(dict(row)),201

@app.get("/api/dashboard")
def dashboard():
    con=db()
    incidents=con.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
    open_incidents=con.execute("SELECT COUNT(*) FROM incidents WHERE status NOT IN ('Contained','Resolved')").fetchone()[0]
    requests=con.execute("SELECT COUNT(*) FROM requests WHERE status NOT IN ('Delivered','Resolved')").fetchone()[0]
    volunteers=con.execute("SELECT COUNT(*) FROM volunteers").fetchone()[0]
    sos=con.execute("SELECT COUNT(*) FROM sos").fetchone()[0]
    con.close()
    return jsonify(total_incidents=incidents,active_incidents=open_incidents,
                   open_requests=requests,volunteers=volunteers,sos_alerts=sos)

if __name__ == "__main__":
    init_db()
    print("ResQLink running at http://127.0.0.1:5000/")
    app.run(host="127.0.0.1",port=5000,debug=True)
