from flask import Flask, request, jsonify, session, send_file , render_template
from flask_cors import CORS
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "findo_secret_key"
CORS(app, supports_credentials=True)

# Database setup
def init_db():
    with sqlite3.connect("findo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT, email TEXT UNIQUE, password TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS items (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER, name TEXT, location TEXT, status TEXT)""")
        conn.commit()

init_db()

@app.route("/", methods=["GET"])
def home_page():
    print("HEllo")
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name, email, password = data["name"], data["email"], data["password"]

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        with sqlite3.connect("findo.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                           (name, email, hashed_pw))
            conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists!"}), 400

# User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email, password = data["email"], data["password"]

    with sqlite3.connect("findo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user[2]):
            session["user_id"] = user[0]
            return jsonify({"message": "Login successful!", "user": {"id": user[0], "name": user[1]}})
        return jsonify({"error": "Invalid credentials!"}), 401

# Get all found items
@app.route("/items", methods=["GET"])
def get_items():
    with sqlite3.connect("findo.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, location FROM items WHERE status='found'")
        items = cursor.fetchall()
        return jsonify([{"name": i[0], "location": i[1]} for i in items])

# Add lost/found item
@app.route("/add", methods=["POST"])
def add_item():
    # if "user_id" not in session:
    #     return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    name, location, status = data["name"], data["location"], data["status"]
    
    with sqlite3.connect("findo.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO items (user_id, name, location, status) VALUES (?, ?, ?, ?)",
                       ( "user", name, location, status))
        conn.commit()
    
    return jsonify({"message": "Item added successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True)