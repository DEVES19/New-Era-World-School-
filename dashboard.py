from flask import Flask, render_template
import json
import os

app = Flask(__name__)

def get_admissions():
    if not os.path.exists("admissions.json"):
        return []
    data = []
    with open("admissions.json", "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_users():
    if not os.path.exists("users.json"):
        return []
    with open("users.json", "r") as f:
        return json.load(f)

@app.route("/")
def home():
    admissions = get_admissions()
    users = get_users()
    return render_template("index.html", admissions=admissions, users=len(users))

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
