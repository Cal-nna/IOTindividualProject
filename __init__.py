from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.pubnub_client import pubnub, CHANNEL
from pubnub.exceptions import PubNubException


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////var/www/calweb/app/instance/calweb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "change-this-in-production"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SceneLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(80))
    old_scene = db.Column(db.String(10))
    new_scene = db.Column(db.String(10))



# GLOBAL STATE (shared by all users)
current_mode = {"scene": "day"}  # day or night

@app.route("/")
def index():
    return render_template(
        "index.html",
        scene=current_mode["scene"]
    )

@app.route("/toggle", methods=["POST"])
@login_required
def toggle():
    old_scene = current_mode["scene"]
    new_scene = "night" if old_scene == "day" else "day"

    current_mode["scene"] = new_scene

    try:
        pubnub.publish() \
            .channel(CHANNEL) \
            .message({"mode": new_scene}) \
            .sync()
    except PubNubException as e:
        return str(e), 500

    log = SceneLog(
        username=current_user.username,
        old_scene=old_scene,
        new_scene=new_scene
    )

    db.session.add(log)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/outdex")
def outdex():
    return render_template("outdex.html")

if __name__ == "__main__":
    app.run(debug=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return "Username already exists", 400

        # Create new user
        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Log user in immediately after registration
        login_user(user)

        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/logs")
@login_required
def logs():
    logs = SceneLog.query.order_by(SceneLog.timestamp.desc()).all()
    return render_template("logs.html", logs=logs)


@app.route("/api/visual", methods=["POST"])
@login_required
def set_visual_mode():
    data = request.get_json()
    mode = data.get("mode")

    if mode not in ("day", "night"):
        return jsonify({"error": "Invalid mode"}), 400

    old_scene = current_mode["scene"]
    current_mode["scene"] = mode

    try:
        pubnub.publish() \
            .channel(CHANNEL) \
            .message({"mode": mode}) \
            .sync()
    except PubNubException as e:
        return jsonify({"error": str(e)}), 500

    log = SceneLog(
        username=current_user.username,
        old_scene=old_scene,
        new_scene=mode
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({"status": "ok", "mode": mode})

@app.context_processor
def inject_scene():
    return {
        "scene": current_mode["scene"]
    }

