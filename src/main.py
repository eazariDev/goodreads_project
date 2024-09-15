from models import *
from importer import *
from fixtures.reports import *
from peewee import fn
 
def load_data():
    importer_classes = [
        UserImporter, BookImporter, AuthorImporter,
        BookAuthorImporter, ShelfImporter, BookShelfImporter
    ]
    for _class in importer_classes:
        print(_class.load())
        

def create_tables():
    database.create_tables(
        [User, Book, Author, Shelf, BookShelf,
         BookAuthor, BookTranslator, UserAuthorRelation,
         UserRelation]
    )
    
def show_data():
    show_users()
    print("*" * 80)
    show_books()
    
def show_user_data(username, password):
    user = User.authenticate(username, password)
    if user is None:
        print('user does not exit')
    else:
        print(f'welcome {user.username}')
        for shelf in user.shelves:
            books = list()
            print(f'{shelf.name}({shelf.book_shelves.count()})')
            for book_shelf in user.book_shelves:
                if book_shelf.shelf.name == shelf.name:
                    books.append(book_shelf.book.name)
            if books:
                print(f'Books in shelf: {books}')
    
    print("#" * 80)

def show_book_rates():
    query = BookShelf.select(
        BookShelf.book, fn.AVG(BookShelf.rate).alias('rates_avg'),
        fn.SUM(BookShelf.rate).alias('rates_sum'),
        fn.COUNT(BookShelf.rate).alias('rates_count')
        ).group_by(BookShelf.book)
    for q in query:
        print(f'book id: {q.book_id}    average rate: {q.rates_avg}     sum of rates: {q.rates_sum}     number of rates: {q.rates_count}')

def show_users_shelves():
    query = BookShelf.select(
        BookShelf.user,
        BookShelf.shelf,
        fn.COUNT(BookShelf.book).alias('books_count')
    ).group_by(BookShelf.shelf)
    for q in query:
        print(f'username: {q.user.username}     shelf: {q.shelf.name}       number of books in shelf: {q.books_count}')

def show_all_book_shelves():
    query = BookShelf.select().join(User)\
        .switch(BookShelf).join(Book)\
            .switch(BookShelf).join(Shelf)
    
    for q in query:
        print(f'username: {q.user.username}     book name: {q.book.name}     shelf: {q.shelf.name}')
    
if __name__ == '__main__':
    
    #run this command to create tables (once in the begining)
    # create_tables()
    
    #run this command to add data to tables
    # load_data()
    
    #run this command to get data from tables
    # show_data()
    
    # show_user_data('hosein', '654321')
    # show_user_data('erfan', '23434')
    # show_user_data('iman', '654321')
    # bs = BookShelf.get_by_id(2)
    # print(f'state before change: {bs.shelf.name}')
    # bs.change_to_read()
    # print(f'state after change: {bs.shelf.name}')
    # print(f'state before change: {bs.shelf.name}')
    # bs.change_to_want_to_read()
    # print(f'state after change: {bs.shelf.name}')
    
    show_book_rates()
    show_users_shelves()
    show_all_book_shelves()