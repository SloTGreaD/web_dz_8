from mongoengine import Document, StringField, ListField, ReferenceField, connect
import json


connect('', host="")

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

with open('authors.json', encoding='utf-8') as file:
    authors_data = json.load(file)
    for author_data in authors_data:
        author = Author(**author_data)
        author.save()


with open('quotes.json', encoding='utf-8') as file:
    quotes_data = json.load(file)
    for quote_data in quotes_data:
        
        author = Author.objects(fullname=quote_data['author']).first()
        quote_data.pop('author', None)  
        quote = Quote(author=author, **quote_data)
        quote.save()



def search_quotes():
    while True:
        command = input("Enter your command: ")
        if command == 'exit':
            break
        key, value = command.split(':', 1)
        value = value.strip()
        
        if key == 'name':
            author = Author.objects(fullname=value).first()
            if author:
                quotes = Quote.objects(author=author)
            else:
                quotes = []
        elif key == 'tag':
            quotes = Quote.objects(tags=value)
        elif key == 'tags':
            tags = value.split(',')
            quotes = Quote.objects(tags__in=tags)
        else:
            quotes = []

        for quote in quotes:
            print(f'"{quote.quote}" - {quote.author.fullname}')


if __name__ == '__main__':
    search_quotes()