from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# --- Helper Function ---
def find_event_by_id(event_id):
    """Loop through the events list to find the event matching the ID."""
    for event in events:
        if event.id == event_id:
            return event
    return None


# Welcome Route 
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Events API!"}), 200


# Get All Events Route
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)
    
    # Strict validation for POST: title must be present
    if not data or "title" not in data:
        return jsonify({"error": "Bad Request: 'title' is a required field"}), 400

    next_id = max([event.id for event in events], default=0) + 1
    new_event = Event(id=next_id, title=data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # CRITICAL FIX 1: Check if the resource exists FIRST to return a 404 properly
    event = find_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
        
    data = request.get_json(silent=True) or {}
    
    # CRITICAL FIX 2: Allow partial updates without failing on missing keys
    if "title" in data:
        event.title = data["title"]

    return jsonify(event.to_dict()), 200


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Check if the resource exists first
    event = find_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
        
    events.remove(event)
    
    # Returns a valid confirmation JSON payload
    return jsonify({"message": "Event deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)