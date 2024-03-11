import pika
import json
from models import Contact  # Припускаємо, що ваші моделі зберігаються в файлі models.py
from faker import Faker

fake = Faker()

connection = pika.BlockingConnection(pika.ConnectionParameters(''))
channel = connection.channel()


channel.queue_declare(queue='emails')


for _ in range(10):  
    fullname = fake.name()
    email = fake.email()
    contact = Contact(fullname=fullname, email=email)
    contact.save()

    
    channel.basic_publish(exchange='',
                          routing_key='emails',
                          body=json.dumps(str(contact.id)))

print(" [x] Sent 10 fake contacts to queue")
connection.close()
