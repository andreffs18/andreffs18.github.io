from mongoengine.fields import StringField, ListField, EmailField, DateTimeField, FloatField, IntField
from mongoengine import Document

from core.settings import logger
from core.utils import generate_slug

import time


class BlogArticle(Document):

    title = StringField(required=True)
    subtitle = StringField()
    content = StringField(required=True)
    slug = StringField()
    timestamp = IntField()
    read_time = FloatField()
    author = StringField()

    def __unicode__(self):
        return self.title

    @classmethod
    def create_article(self, **kwargs):
        logger.debug("Creating new Blog Post")

        timestamp = time.time()

        article = BlogArticle.objects.create(title = kwargs["title"],
                                            subtitle = kwargs["subtitle"],
                                            content = kwargs["content"],
                                            slug = generate_slug(kwargs["title"], timestamp),
                                            timestamp = timestamp,
                                            )
        article.save()
        logger.info("Article saved to db.")
        return article