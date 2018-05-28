from flask import Flask, request, session, url_for, render_template
from .models import Topic, Event
from json import dumps, loads

def serialize_topic(topic):
    return {
        'name': topic['name'],
        'id': topic['id']
    }

def serialize_event(event):
    return {
        'name': event['name'],
        'id': event['id'],
        'location': event['location'],
        'organiser': event['organiser']
    }

def _serialize_topic(topic):
    return dumps([serialize_topic(record['topic']) for record in topic])

#def _serialize_topic(topic):
#    return [serialize_topic(record['topic']) for record in topic]

app = Flask(__name__)

@app.route("/topic/create", methods=['POST'])
def _make_topic():
    JSON_input = request.get_json()
    Topic.make_topic(JSON_input["Topic"])
    return '''Topic Created'''

@app.route("/event/create", methods=['POST'])
def _make_event():
    JSON_input = request.get_json()
    Event.make_event(JSON_input["Event"])
    return '''Event Created'''

@app.route("/event/relate", methods=['POST'])
def _make_relation():
    JSON_input = request.get_json()
    event_info = JSON_input["Event"]
    topic_info = JSON_input["Topic"]
    Event.make_relation(event_info["id"], topic_info["id"])
    return '''Relationship Created'''

@app.route("/event/find-topics", methods=['POST'])
def _find_related_topics():
    JSON_input = request.get_json()
    event_info = JSON_input["Event"]
    _related_topics = Event.find_related_topics(event_info["id"])
    temp4 = []
    #for record in _related_topics:             
    #    temp4.append(record["topic"])
    #return render_template('template_find_topics.html',output=temp4)
    temp3 = _serialize_topic(_related_topics)
    return render_template('template_find_topics.html', output = temp3)
