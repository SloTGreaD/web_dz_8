import pika
import json
from models import Contact  

def callback(ch, method, properties, body):
    contact_id = json.loads(body)
    contact = Contact.objects(id=contact_id).first()
    
    if contact:
        print(f"Imitating sending email to {contact.fullname} <{contact.email}>")
        contact.message_sent = True
        contact.save()


connection = pika.BlockingConnection(pika.ConnectionParameters(''))
channel = connection.channel()


channel.queue_declare(queue='emails')


channel.basic_consume(queue='emails', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
