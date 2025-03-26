from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample lost & found data (Simulated Database)
items = [
    {"id": 1, "name": "Laptop", "location": "Library", "status": "lost"},
    {"id": 2, "name": "Backpack", "location": "Cafeteria", "status": "found"},
]

# Route to get all lost/found items
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items)

# Route to add a new lost/found item
@app.route("/add", methods=["POST"])
def add_item():
    data = request.json
    new_item = {
        "id": len(items) + 1,
        "name": data["name"],
        "location": data["location"],
        "status": data["status"],
    }
    items.append(new_item)
    return jsonify({"message": "Item added successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
