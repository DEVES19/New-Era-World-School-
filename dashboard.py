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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    from flask import request, redirect

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    student_class = request.form["class"]
    phone = request.form["phone"]

    with open("admissions.json", "a") as f:
        f.write(json.dumps({
            "name": name,
            "class": student_class,
            "phone": phone
        }) + "\n")

    return redirect("/")
    return "New Era World School Dashboard is LIVE 🚀"