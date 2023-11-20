import os
import django
from pymongo import MongoClient


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_quotes.settings")
django.setup()
from quotes.models import Quote, Tag, Author

DB_NAME = 'app_inst'
DB_USER = 'postgres'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '5432'

client = MongoClient("mongodb://localhost")
db = client.hw

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, created = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = Quote.objects.filter(quote=quote['quote']).exists()

    if not exist_quote:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(quote=quote['quote'], author=a)
        q.tags.set(tags)
