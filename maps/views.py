from flask import Flask, request, session, url_for, render_template, json
from .models import Topic, Event
from .serialize import serialize, initialize

app = Flask(__name__)

@app.route("/topic/create", methods=['POST'])
def _make_topic():
    JSON_input = request.get_json()
    initialize.initialize_topic(JSON_input["Topic"])
    Topic.make_topic(JSON_input["Topic"])
    return '''Topic Created'''

@app.route("/event/create", methods=['POST'])
def _make_event():
    JSON_input = request.get_json()
    initialize.initialize_event(JSON_input["Event"])
    Event.make_event(JSON_input["Event"])
    if JSON_input["Event"]["topic_id"] and JSON_input["Event"]["event_id"]:
        event_info = JSON_input["Event"]
        Event.make_relation(event_info["event_id"], event_info["topic_id"])
        return '''Event and Relationship Created'''
    return '''Event Created'''

@app.route("/event/relate", methods=['POST'])
def _make_relation():
    JSON_input = request.get_json()
    event_info = JSON_input["Event"]
    topic_info = JSON_input["Topic"]
    Event.make_relation(event_info["event_id"], topic_info["topic_id"])
    return '''Relationship Created'''

@app.route("/event/find-topics", methods=['POST'])
def _find_related_topics():
    JSON_input = request.get_json()
    event_info = JSON_input["Event"]
    _related_topics = Event.find_related_topics(event_info["id"])

    return json.dumps(serialize._serialize_topic(_related_topics))
