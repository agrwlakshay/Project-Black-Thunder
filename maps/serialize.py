
class serialize:
    def serialize_topic(topic):
        return {
            'topic_name': topic['topic_name'],
            'topic_id': topic['topic_id']
        }

    def serialize_event(event):
        return {
            'event_name': event['event_name'],
            'event_id': event['event_id'],
            'image_url': event['image_url'],
            'latitude': event['latitude'],
            'longitude': event['longitude'],
            'start_date': event['start_date'],
            'end_date': event['end_date'],
            'min_ticket_price': event['min_ticket_price'] ,
            'topic_id': event['topic_id']
        }

    def _serialize_topic(topic):
        return ([serialize_topic(record['topic']) for record in topic])

class initialize:
    def initialize_event(event):
        event.setdefault('event_id', 0)
        event.setdefault('image_url', 0)
        event.setdefault('latitude', 0)
        event.setdefault('longitude', 0)
        event.setdefault('start_date', 0)
        event.setdefault('end_date', 0)
        event.setdefault('min_ticket_price', 0)
        event.setdefault('topic_id', 0)
        event.setdefault('event_name', 0)
        return event

    def initialize_topic(topic):
        topic.setdefault('topic_name', 0)
        topic.setdefault('topic_id', 0)
        return topic
