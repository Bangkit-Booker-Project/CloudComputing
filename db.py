# from copy import PyStringMap
# from email import charset
import os
# from sqlite3 import connect
# import sqlite3
import pymysql
import pandas as pd

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name =  os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
db_host = os.environ.get('CLOUD_SQL_HOST_NAME')
# conn = sqlite3.connect('books.sqlite')
def db_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    conn = None
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect( #host=db_host,
                                    user=db_user,
                                    password=db_password,
                                    unix_socket=unix_socket,
                                    db=db_name,
                                    charset='utf8',
                                    cursorclass=pymysql.cursors.DictCursor
                                    )
    except pymysql.MySQLError as e:
        return e
    return conn



# untuk konek ke cloud mysql
# conn = pymysql.connect(
#     host='omfofineofne.sdaeojeaf.com',
#     database='bookpred',
#     user='wdioioawmd',
#     password='cscnsneo',
#     charset='utfmb8',
#     cursorclass=pymysql.cursors.DictCursos
# )
# conn = db_connection()
# cursor = conn.cursor()

# Get One Book
def getOneBook(title):
    conn = db_connection()
    # cursor = conn.cursor()
    book = None
    dictBook=[]
    # with conn.cursor() as cursor:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM books WHERE bookTitle=%s", (title,))
        rows = cursor.fetchall()
    for r in rows:
        book = r
    if book is not None:
        dictBook = {
            "bookTitle" : book['bookTitle'],
            "bookRating" : book['bookRating'],
            "ISBN" : book['ISBN'],
            "bookAuthor" : book['bookAuthor'],
            "yearOfPublication" : book['yearOfPublication'],
            "Publisher" : book['Publisher'],
            "url" : book['url'],
            "bookImage" : book['bookImage'],
            "bookDesc" : book['bookDesc'],
            "ratingCount" : book['ratingCount'],
            "bookPages" : book['bookPages'],
            "bookGenres" : book['bookGenres'],
            "bookGenre1" : book['bookGenre1'],
            "bookGenre2" : book['bookGenre2'],
            "bookGenre3" : book['bookGenre3']
        }
    return dictBook

# Get 20 top book By Genre
def topRatingByGenre(genre):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    cursor.execute("SELECT * FROM books WHERE bookGenre1=%s OR bookGenre2=%s OR bookGenre3=%s ORDER BY bookRating DESC LIMIT 20", (genre,genre,genre))
    rows = cursor.fetchall()
    listObj = []
    for r in rows:
        book = r
        dictBook = {
            "bookTitle" : book['bookTitle'],
            "bookRating" : book['bookRating'],
            "ISBN" : book['ISBN'],
            "bookAuthor" : book['bookAuthor'],
            "yearOfPublication" : book['yearOfPublication'],
            "Publisher" : book['Publisher'],
            "url" : book['url'],
            "bookImage" : book['bookImage'],
            "bookDesc" : book['bookDesc'],
            "ratingCount" : book['ratingCount'],
            "bookPages" : book['bookPages'],
            "bookGenres" : book['bookGenres'],
            "bookGenre1" : book['bookGenre1'],
            "bookGenre2" : book['bookGenre2'],
            "bookGenre3" : book['bookGenre3']
        }
        listObj.append(dictBook)
    return listObj

# Rekomendasi Buku
cosine_sim_df = pd.read_csv('cosine.csv')
cosine_sim_df = cosine_sim_df.drop(cosine_sim_df.columns[0], axis=1)
def books_recommendations(bookTitle, similarity_data=cosine_sim_df, k=10):
    index = similarity_data.loc[:,bookTitle].to_numpy().argpartition(
        range(-1, -k, -1))
    
    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    
    # Drop nama_resto agar nama resto yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(bookTitle, errors='ignore')
 
    return pd.DataFrame(closest).head(k)

def similiarBooks(title):
    result = books_recommendations(title)
    sim=[]
    book = None     
    result = result.reset_index()  # make sure indexes pair with number of rows
    for index, row in result.iterrows():
        book =  getOneBook(row[0])
        sim.append(book)
    return sim







# sql_querry = """CREATE TABLE books (
#     bookTitle text NOT NULL, 
#     bookRating integer NOT NULL,
#     ISBN varchar(20) PRIMARY KEY,
#     bookAuthor text NOT NULL,
#     yearOfPublication text NOT NULL,
#     Publisher text NOT NULL,
#     url text NOT NULL,
#     bookImage text NOT NULL,
#     bookDesc text NOT NULL,
#     ratingCount integer,
#     bookPages text NOT NULL,
#     bookGenres text NOT NULL,
#     bookGenre1 text NOT NULL,
#     bookGenre2 text NOT NULL,
#     bookGenre3 text NOT NULL

# )"""
# cursor.execute(sql_querry)
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

