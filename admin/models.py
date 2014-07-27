from django.db import models

# Create your models here.
class BlogArticle(models.Model):
    title = models.CharField()
    subtitle = models.CharField()
    text = models.TextField()
    date = models.DateField()

    def __unicode__(self):
        return self.title
