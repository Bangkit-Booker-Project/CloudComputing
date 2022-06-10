# from copy import PyStringMap
# from email import charset
# from ast import Return
import os
from sqlite3 import connect
import sqlite3
import pymysql
import pandas as pd


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name =  os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
db_host = os.environ.get('CLOUD_SQL_HOST_NAME')

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
    cursor = conn.cursor()
    book = None
    dictBook=[]
    # with conn.cursor() as cursor:
    try:
        cursor.execute("SELECT * FROM books WHERE bookTitle=%s", (title,))
        rows = cursor.fetchall()
    except pymysql.MySQLError as e:
        return False

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
    try :
        cursor.execute("SELECT * FROM books WHERE bookGenre1=%s OR bookGenre2=%s OR bookGenre3=%s ORDER BY bookRating DESC LIMIT 50", (genre,genre,genre))
        rows = cursor.fetchall()
    except pymysql.MySQLError as e:
        return False
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


# Mencari buku dengan title random
def searchRandomTitle(title):
    # titles='%'+title+'%'
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    # querry ="SELECT * FROM books WHERE bookTitle OR bookAuthor OR Publisher LIKE CONCAT('%%', %s, '%%')"
    querry ="SELECT * FROM books WHERE bookTitle LIKE CONCAT('%%', %s, '%%') OR bookAuthor LIKE CONCAT('%%', %s, '%%') OR Publisher LIKE CONCAT('%%', %s, '%%')"

    try :
        cursor.execute(querry, (title,title,title))
        rows = cursor.fetchall()
    except pymysql.MySQLError as e:
        return False
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
    try:
        result = books_recommendations(title)
    except:
        return False
    sim=[]
    book = None
  
    result = result.reset_index()  # make sure indexes pair with number of rows
    for index, row in result.iterrows():
        book =  getOneBook(row[0])
        # if book is False:
        #     return book
        sim.append(book)
    return sim



#====================================================================================================================#



# sql_querry = """CREATE TABLE books (
#     bookTitle text NOT NULL, 
#     bookRating float NOT NULL,
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

# konek = sqlite3.connect('books.sqlite')


# def dbKonek():
#     con = None
#     try:
#         con = sqlite3.connect('books.sqlite')
#     except sqlite3.error as e:
#         print(e)
#     return con

def regsisterUser(email,password, username):
    # konek = dbKonek()
    # kursor = konek.cursor()
    conn = db_connection()
    cursor = conn.cursor()
    sql_Querry = ("INSERT INTO users (email,password,username) VALUES (%s, %s, %s)")

    # user = []
    try :
        cursor.execute(sql_Querry,(email,password,username))
        # kursor.execute(sql_Querry,(email,password,username))
        # rows = kursor.fetchall()
        conn.commit()
        # for r in rows:
        #     user = r
        return False
    except pymysql.MySQLError as e:
        print(e)
        return True


def loginUser(email):
    conn = db_connection()
    cursor = conn.cursor()
    # konek =dbKonek()
    # kursor = konek.cursor()
    sql_Querry = "SELECT * FROM users WHERE email=%s"
    user = False
    try :
        cursor.execute(sql_Querry,(email,))
        rows = cursor.fetchall()
        for r in rows:
            user = r
    except:
        return False
    return user

def resetPassword(uid,pwd):
    conn = db_connection()
    cursor = conn.cursor()
    # konek =dbKonek()
    # kursor = konek.cursor()
    sql_Querry = "UPDATE users SET password=%s WHERE id=%s"
    user = False
    try :
        cursor.execute(sql_Querry,(pwd,uid))
        conn.commit()
        # rows = konek.fetchall()
        # for r in rows:
        #     user = r
        return True
    except:
        return False


# sql_querry = ''
# cursor.execute(sql_querry)
# CREATE TABLE users (
#     id        INTEGER    PRIMARY KEY AUTO_INCREMENT
#                          UNIQUE
#                          NOT NULL,
#     email     CHAR (255) NOT NULL
#                          UNIQUE,
#     password  CHAR (255) NOT NULL,
#     username  CHAR (255) NOT NULL,
#     genres TEXT
# );


# INSERT INTO users (email,password,username) VALUES ('admin','admin','admin')
# UPDATE users SET ratedBook ='[classics]' WHERE id=1
# SELECT * FROM users WHERE email='admin'



# https://nitratine.net/blog/post/how-to-hash-passwords-in-python/





# rekomendasi 50 buku untuk user

# book_data = pd.read_csv('book_dataset.csv')

# # Mengubah book_ids menjadi list tanpa nilai yang sama
# books_ids = book_data['ISBN'].unique().tolist()
 
# # Melakukan proses encoding book_ids
# book_to_book_encoded = {x: i for i, x in enumerate(books_ids)}
 
# # Melakukan proses encoding angka ke book_ids
# book_encoded_to_book = {i: x for i, x in enumerate(books_ids)}

def bookRecomendation(uID):

    # ngambil user id
    user_id=uID
    books_have_been_read_by_user= "SELECT * FROM users WHERE id=%s"
    ISBN = "SELECT bookID FROM books"
    books_have_not_been_read_by_user = ISBN[~ISBN['bookID'].isin(books_have_been_read_by_user['bookID'].values)]
    
    # List data ISBN yang telah diencode pada buku yang dibelum dibaca user
    book_list = [[ISBN.get(x)] for x in books_have_not_been_read_by_user]
    return book_list
    
    




