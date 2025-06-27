from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Ensure database file exists
DB_PATH = os.path.join("data", "phishing.db")

def log_event(user_id, event_type, data=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO events (user_id, event_type, data, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, event_type, data, datetime.now()))
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit/<user_id>", methods=["GET", "POST"])
def submit(user_id):
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        log_event(user_id, "submitted", f"{email}:{password}")
        return redirect("/educate")
    log_event(user_id, "clicked")
    return render_template("submit.html")

@app.route("/educate")
def educate():
    return render_template("educate.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT event_type, COUNT(*) FROM events GROUP BY event_type")
    stats = c.fetchall()
    conn.close()
    return render_template("dashboard.html", stats=stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

