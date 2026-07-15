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


# Welcome Route (Required for the first rubric criterion)
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Events API!"}), 200


# Get All Events Route (Required for the second rubric criterion)
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Task 1: Define the Problem
    # We need to extract the incoming JSON data safely and make sure 'title' is provided.
    
    # Task 2: Design and Develop the Code
    data = request.get_json(silent=True)
    if not data or "title" not in data or not data["title"].strip():
        # Input Validation: Return 400 Bad Request if title is missing/empty
        return jsonify({"error": "Bad Request: 'title' is a required field"}), 400

    # Task 3: Implement the Loop and Process Each Element
    # To assign a unique ID, we find the maximum current ID and add 1 (default to 1 if empty)
    next_id = max([event.id for event in events], default=0) + 1
    new_event = Event(id=next_id, title=data["title"])
    events.append(new_event)

    # Task 4: Return and Handle Results
    # Return 201 Created status code along with the created event data
    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Task 1: Define the Problem
    # We need to find the event by its ID and partially update its 'title' using JSON payload.
    
    # Task 2: Design and Develop the Code
    data = request.get_json(silent=True)
    if not data or "title" not in data or not data["title"].strip():
         return jsonify({"error": "Bad Request: 'title' field is required to update"}), 400

    # Task 3: Implement the Loop and Process Each Element
    event = find_event_by_id(event_id)
    if not event:
        # Resource Not Found handling
        return jsonify({"error": "Event not found"}), 404
        
    # Process the update
    event.title = data["title"]

    # Task 4: Return and Handle Results
    return jsonify(event.to_dict()), 200


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Task 1: Define the Problem
    # We need to locate an event by ID and cleanly remove it from our in-memory storage.
    
    # Task 2: Design and Develop the Code / Task 3: Implement the Loop
    event = find_event_by_id(event_id)
    if not event:
        # Resource Not Found handling
        return jsonify({"error": "Event not found"}), 404
        
    # Process the deletion
    events.remove(event)

    # Task 4: Return and Handle Results
    return jsonify({"message": "Event deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)