from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# GLOBAL STATE (shared by all users)
current_mode = {"scene": "day"}  # day or night

@app.route("/")
def index():
    return render_template(
        "index.html",
        scene=current_mode["scene"]
    )

@app.route("/toggle", methods=["POST"])
def toggle():
    if current_mode["scene"] == "day":
        current_mode["scene"] = "night"
    else:
        current_mode["scene"] = "day"

    return redirect(url_for("index"))


@app.route("/outdex")
def outdex():
    return render_template("outdex.html")

if __name__ == "__main__":
    app.run(debug=True)
