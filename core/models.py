from mongoengine.fields import StringField, ListField, EmailField, DateTimeField, FloatField, IntField
from mongoengine import Document
from django.http import HttpResponseRedirect

from core.settings import logger

import time

class ContactMessage(Document):

    name = StringField(required=True)
    email = EmailField(required=True)
    message = StringField()
    timestamp = IntField()

    def __unicode__(self):
        return "%s - %s" % (self.email, self.message[:36])

    @classmethod
    def create_contact_message(self, **kwargs):
        logger.debug("Creating Contact message")

        timestamp = time.time()

        message = ContactMessage.objects.create(name = kwargs["name"],
                                                email = kwargs["email"],
                                                message = kwargs["message"],
                                                timestamp = timestamp,
                                                )
        message.save()
        logger.info("Message saved to db.")
        return message

    @classmethod
    def delete_contact_message(self, **kwargs):
        logger.debug("Deleting Contact Message")
        try:
            message = ContactMessage.objects.get(id=kwargs['id'])
            message.delete()
        except:
            return False

        return True


def delete_blog_article(request):
    message_id = request.GET['article']
    response = ContactMessage.delete_contact_message(id=message_id)
    if response:
        status = "success"
    else:
        status = "error"

    return HttpResponseRedirect('/lol')
