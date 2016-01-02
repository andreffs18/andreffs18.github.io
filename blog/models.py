from django.db import models
import os
from andreffs.settings import db as DB
from django.utils import timezone
from bson.objectid import ObjectId
import blog.services as blogservices
from slugify import slugify
# Create your models here.
#
#
# class MongoCollection(object):
#
#     @classmethod
#



class Articles(object):
    collection = DB.articles

    @classmethod
    def create(cls, title, body):
        article = cls.collection.insert({
            'title': title,
            'body': body,
            'slug': slugify(title),
        })
        cls.update(article, **{'creation_date': article.generation_time})
        return article

    @classmethod
    def update(cls, obj, **params):
        """updates article <obj> with params values
        :param obj: article json object returned from collection query
        :return: nothing
        """
        if isinstance(obj, ObjectId):
            _id = obj
        else:
            _id = obj['_id']

        return cls.collection.update({'_id': _id}, {"$set": params})


    @classmethod
    def all(cls):
        return cls.collection.find()

    def objects(self):
        return self.collection.find()

    @classmethod
    def filter(cls, **filter):
        return cls.collection.find_one(filter)

    @classmethod
    def _drop_collection(cls):
        return cls.collection.remove()


#
# titles = [" ".join(map(lambda x: x.capitalize(), f.split("-")))
#           for f in blogservices.get_articles_titles()]
# paths = [u"{}/{}".format(blogservices.articles_folder, f)
#          for f in blogservices.get_articles_titles()]
#
# for title, filepath in zip(titles, paths):
#     with open(filepath, 'r') as body:
#         Articles.create(title, body.read())

# from django.db import models
# #http://www.djangorocks.com/tutorials/how-to-create-a-basic-blog-in-django/configuring-the-automatic-admin.html

# from django.db.models import permalink
#
# # Create your models here.
#
# admin.site.register(Blog)
# admin.site.register(Category)
#
# class Blog(models.Model):
#     title = models.CharField(max_length=100, unique=True)
#     slug = models.SlugField(max_length=100, unique=True)
#     body = models.TextField()
#     posted = models.DateTimeField(db_index=True, auto_now_add=True)
#     category = models.ForeignKey('blog.Category')
#
#     def __unicode__(self):
#         return '%s' % self.title
#
#     @permalink
#     def get_absolute_url(self):
#         return ('view_blog_post', None, { 'slug': self.slug })
#
# class Category(models.Model):
#     title = models.CharField(max_length=100, db_index=True)
#     slug = models.SlugField(max_length=100, db_index=True)
#
#     def __unicode__(self):
#         return '%s' % self.title
#
#     @permalink
#     def get_absolute_url(self):
#         return ('view_blog_category', None, { 'slug': self.slug })