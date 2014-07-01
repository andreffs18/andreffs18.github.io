from mongoengine.fields import StringField, ListField, EmailField, DateTimeField
from mongoengine import Document

from blog.utils import generate_slug


import datetime

import logging
logger = logging.getLogger('andreffs.' + __name__)

class BlogPost(Document):

    title = StringField(required=True)
    subtitle = StringField()
    content = StringField(required=True)
    slug = StringField()
    date =DateTimeField()
    comments = StringField()

    @classmethod
    def create_article(self, **kwargs):
        logger.debug("Creating Article Post.")
        article = BlogPost.objects.create(title = kwargs["title"],
                                          subtitle = kwargs["subtitle"],
                                          content = kwargs["content"],
                                          slug = generate_slug(kwargs["title"]),
                                          data = datetime.datetime.now,
                                          comments = "0")
        article.save()
        logger.debug("Article \"%s\" saved to db." % article["id"])
        return article



