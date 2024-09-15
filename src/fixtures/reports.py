from models import *

def show_users():
    users = User.select()
    for user in users:        
        #these two lines are the same, the second one use backref for selecting user shelves
        #shelves = Shelf.select().where(Shelf.user == user)
        number_of_shelves = user.shelves.count()
        shelves = ', '.join([shelf.name for shelf in user.shelves])
        print(user.username, '\t', shelves)

def show_books():
    books = Book.select()
    for book in books:
        authors = ', '.join([book_author.author.name for book_author in book.authors])
        print(book.name, '\t', book.isbn, '\t', authors)