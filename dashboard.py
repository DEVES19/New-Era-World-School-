from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

# ---------- READ DATA ----------
def get_admissions():
    if not os.path.exists("admissions.json"):
        return []
    with open("admissions.json", "r") as f:
        return [json.loads(line) for line in f]

# ---------- HOME PAGE ----------
@app.route("/")
def home():
    admissions = get_admissions()
    return render_template("index.html", admissions=admissions)

# ---------- ADD DATA ----------
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

# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
    