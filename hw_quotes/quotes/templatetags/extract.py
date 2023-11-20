from ..models import Author
from bson import ObjectId
from django import template

from ..utils import get_mongodb

register = template.Library()


def get_authormongo(id_):
    db = get_mongodb()
    author = db.authors.find_one({'_id': ObjectId(id_)})
    return author['fullname']


def get_author(author_id):
    try:
        author = Author.objects.get(id=author_id)
        return author.fullname
    except Author.DoesNotExist:
        return "Author not found"


register.filter('author', get_author)
