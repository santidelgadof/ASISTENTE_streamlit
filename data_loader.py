import pandas as pd
from sqlalchemy import text
from config import get_db_engine
import json
import os

def load_topics():
    if os.path.exists('topics.json'):
        with open('topics.json', 'r') as file:
            return json.load(file)
    return {}

def save_topic(topic_name, description, sql_query, user_name):
    topics = load_topics()
    topics[topic_name] = {"description": description, "sql_query": sql_query, "creator": user_name}
    with open('topics.json', 'w') as file:
        json.dump(topics, file)

def delete_topic(topic_name, user_name):
    topics = load_topics()
    if topic_name in topics and topics[topic_name]['creator'] == user_name:
        del topics[topic_name]
        with open('topics.json', 'w') as file:
            json.dump(topics, file)


