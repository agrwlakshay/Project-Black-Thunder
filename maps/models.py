from neo4j.v1 import GraphDatabase, basic_auth
import os

url="bolt://localhost:7687"
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

driver = GraphDatabase.driver(url, auth=basic_auth("neo4j", "2545"))

class Unique:
    def topic_uniqueness_constraint():
        def create_uniqueness_constraint(tx):
            tx.run("CREATE CONSTRAINT ON (n:Topic) ASSERT n.id IS UNIQUE")

        with driver.session() as session:
            session.write_transaction(create_uniqueness_constraint)

    def event_uniqueness_constraint():
        def create_uniqueness_constraint(tx):
            tx.run("CREATE CONSTRAINT ON (n:Event) ASSERT n.id IS UNIQUE")

        with driver.session() as session:
            session.write_transaction(create_uniqueness_constraint)


class Topic:
    def make_topic(node):
        def create_topic(tx, name, id):
            tx.run("CREATE (a:Topic{name:$name, id:$id})",
                   name=name, id=id)
        with driver.session() as session:
            session.write_transaction(create_topic, node['name'], node['id'])


class Event:
    def make_event(node):
        def create_event(tx, name, id, location, organiser):
            tx.run("CREATE (a:Event{name:$name, id:$id, location:$location, organiser:$organiser})",
                   name=name, id=id, location=location, organiser=organiser)
        with driver.session() as session:
            session.write_transaction(create_event, node['name'], node['id'],
                                      node['location'], node['organiser'])

    def make_relation(event_id, topic_id):
        def create_relation(tx, event_id, topic_id):
            tx.run("MATCH (a:Event{id:$event}),(c:Topic{id:$topic}) CREATE (a)-[b:BASED_ON]->(c)",
                   event=event_id, topic=topic_id)
        with driver.session() as session:
            session.write_transaction(create_relation, event_id, topic_id)

    def find_related_topics(event_id):
        def find_relations(tx, event_id):
            related_topics = tx.run("MATCH (a:Event{id:$id})-[b:BASED_ON]->(c:Topic) RETURN c AS topic", id=event_id)
            return related_topics

        with driver.session() as session:
            results = session.read_transaction(find_relations, event_id)
        return results
