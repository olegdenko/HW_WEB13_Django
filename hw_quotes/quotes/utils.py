from pymongo import MongoClient
import psycopg2



def get_mongodb():
    client = MongoClient("mongodb://localhost")

    db = client.hw
    return db


def get_postgresql(db):
    try:
        connection = psycopg2.connect(**db)
        return connection
    except psycopg2.Error as e:
        print(f"Помилка підключення до PostgreSQL: {e}")
        return None
