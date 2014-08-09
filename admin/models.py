from mongoengine.fields import StringField, ListField, EmailField, DateTimeField, FloatField, IntField
from mongoengine import Document
from django.http import HttpResponseRedirect

from core.settings import logger
from core.utils import generate_slug, calc_avg_read_time

import time


class BlogArticle(Document):

    title = StringField(required=True)
    content = StringField(required=True)
    slug = StringField()
    timestamp = IntField()
    read_time = StringField(default="1min")
    author = StringField()

    def __unicode__(self):
        return self.title

    @classmethod
    def create_article(self, **kwargs):
        logger.debug("Creating Blog article")

        timestamp = time.time()

        article = BlogArticle.objects.create(title = kwargs["title"],
                                            content = kwargs["content"],
                                            slug = generate_slug(kwargs["title"], timestamp),
                                            timestamp = timestamp,
                                            read_time = calc_avg_read_time(kwargs["content"]),
                                            )
        article.save()
        logger.info("Article saved to db.")
        return article

    @classmethod
    def delete_article(self, **kwargs):
        logger.debug("Deleting Blog Article")
        try:
            article = BlogArticle.objects.get(id=kwargs['id'])
            article.delete()
        except:
            return False

        return True


def delete_blog_article(request):
    article_id = request.GET['article']
    response = BlogArticle.delete_article(id=article_id)
    if response:
        status = "success"
    else:
        status = "error"

    return HttpResponseRedirect("/admin/blog?status=%s" % (status))