import mongoengine as me
from slugify import slugify

class Post(me.Document):
    title = me.StringField(max_length=255, required=True)
    slug = me.StringField(max_length=255, required=True)
    body = me.StringField(required=True)
    tags = me.ListField(me.StringField(), default=[])

    meta = {
        'allow_inheritance': True,
        'indexes': ['-id', 'slug'],
        'ordering': ['-id']
    }

    def __str__(self):
        return "{}".format(self.title)

    def __repr__(self):
        return u"<Post: {}>".format(str(self))

    def __unicode__(self):
        return unicode(self.id)

    @property
    def creation_date(self):
        """Return creation date from object id"""
        return self.id.generation_time

    @classmethod
    def create(cls, title, body, slug=None):
        """Create Blog Post object"""
        slug = slugify(title)
        post = Post(title=title, body=body, slug=slug)
        post.save()
        return post