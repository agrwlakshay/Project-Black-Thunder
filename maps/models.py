from neo4j.v1 import GraphDatabase, basic_auth
import os

url="bolt://localhost:7687"
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

driver = GraphDatabase.driver(url, auth=basic_auth("neo4j", "2545"))

class Unique:
    def topic_uniqueness_constraint():
        def create_uniqueness_constraint(tx):
            tx.run("CREATE CONSTRAINT ON (n:Topic) ASSERT n.topic_id IS UNIQUE")

        with driver.session() as session:
            session.write_transaction(create_uniqueness_constraint)

    def event_uniqueness_constraint():
        def create_uniqueness_constraint(tx):
            tx.run("CREATE CONSTRAINT ON (n:Event) ASSERT n.event_id IS UNIQUE")

        with driver.session() as session:
            session.write_transaction(create_uniqueness_constraint)


class Topic:
    def make_topic(topic):
        def create_topic(tx, topic_name, topic_id):
            tx.run("CREATE (a:Topic{topic_name:$topic_name, topic_id:$topic_id})",
                  topic_name=topic_name, topic_id=topic_id)
        with driver.session() as session:
            session.write_transaction(create_topic,  topic['topic_name'], topic['topic_id'])


class Event:
    def make_event(event):
        def create_event(tx, event_name, event_id, image_url, latitude, longitude, start_date, end_date,
                         min_ticket_price, topic_id ):
            tx.run("CREATE (a:Event{event_name:$event_name, event_id:$event_id, image_url:$image_url, latitude:$latitude, longitude:$longitude, start_date:$start_date, end_date:$end_date, min_ticket_price:$min_ticket_price, topic_id:$topic_id} )",
                   event_name=event_name, event_id=event_id, image_url=image_url, latitude=latitude,
                   longitude=longitude, start_date=start_date, end_date=end_date,
                   min_ticket_price=min_ticket_price, topic_id=topic_id)
        with driver.session() as session:
            session.write_transaction(create_event, event['event_name'], event['event_id'],
                                      event['image_url'], event['latitude'], event['longitude'],
                                      event['start_date'], event['end_date'], event['min_ticket_price'],
                                      event['topic_id'] )

    def make_relation(event_id, topic_id):
        def create_relation(tx, event_id, topic_id):
            tx.run("MATCH (a:Event{event_id:$event_id}),(c:Topic{topic_id:$topic_id}) CREATE (a)-[b:BASED_ON]->(c)",
                   event_id=event_id, topic_id=topic_id)
        with driver.session() as session:
            session.write_transaction(create_relation, event_id, topic_id)

    def find_related_topics(event_id):
        def find_relations(tx, event_id):
            related_topics = tx.run("MATCH (a:Event{event_id:$event_id})-[b:BASED_ON]->(c:Topic) RETURN c AS topic",
                                    event_id=event_id)
            return related_topics

        with driver.session() as session:
            results = session.read_transaction(find_relations, event_id)
        return results
