from copy import PyStringMap
from email import charset
import sqlite3
# import pymysql

conn = sqlite3.connect('books.sqlite')

# untuk konek ke cloud mysql
# conn = pymysql.connect(
#     host='omfofineofne.sdaeojeaf.com',
#     database='bookpred',
#     user='wdioioawmd',
#     password='cscnsneo',
#     charset='utfmb8',
#     cursorclass=pymysql.cursors.DictCursos
# )
cursor = conn.cursor()

sql_querry = """CREATE TABLE books (
    bookTitle text NOT NULL, 
    bookRating integer NOT NULL,
    ISBN text PRIMARY KEY,
    bookAuthor text NOT NULL,
    yearOfPublication text NOT NULL,
    Publisher text NOT NULL,
    url text NOT NULL,
    bookImage text NOT NULL,
    bookDesc text NOT NULL,
    ratingCount text,
    bookPages text NOT NULL,
    bookGenres text NOT NULL
)"""
cursor.execute(sql_querry)
# conn.close()



# bookTitle
# bookRating
# ISBN
# bookAuthor
# yearOfPublication
# Publisher
# url
# bookImage
# bookDesc
# ratingCount
# bookPages
# bookGenres

