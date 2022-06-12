from webbrowser import get
import pandas as pd
book_data = pd.read_csv('book_dataset.csv')
def getISBN(books):
    getISBN = book_data[book_data.books.isin([books])][['bookTitle','ISBN','url','bookAuthor','yearOfPublication','bookImage','bookPages','Publisher','bookDesc','bookGenre1','bookGenre2','bookGenre3']]
    getISBN = getISBN.iloc[0][0]
    return getISBN
book = getISBN(4)
# dictBook = {
#         "bookTitle" : book[0],
#         "ISBN" : book[1],
#         "url" : book[2],
#         "bookAuthor" : book[3],
#         "yearOfPublication" : book[4],
#         "bookImage" : book[5],
#         "bookPages" : book[6],
#         "Publisher" : book[7],
#         "bookDesc" : book[8],
#         "bookGenre1" : book[9],
#         "bookGenre2" : book[10],
#         "bookGenre3" : book[11]
#     }
print(book)
