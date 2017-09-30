from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now

from slugify import slugify

import logging
logger = logging.getLogger()


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True)
    body = models.CharField(max_length=10000)
    tags = ArrayField(models.CharField(max_length=255), blank=True, null=True)

    creation_date = models.DateTimeField(blank=True)
    last_update_at = models.DateTimeField(blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return u"{}".format(self.title)

    @classmethod
    def create(cls, title, body, **kwargs):
        """Create Blog Post object"""
        post = Post(title=title, body=body, **kwargs)
        post.save()
        return post

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.creation_date = now()

        if not self.slug:
            self.slug = slugify(self.title)

        self.last_update_at = now()
        return super(Post, self).save(*args, **kwargs)
