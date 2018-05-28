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
