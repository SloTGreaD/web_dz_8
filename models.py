from mongoengine import Document, StringField, BooleanField, connect

connect('', host="")

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
    
