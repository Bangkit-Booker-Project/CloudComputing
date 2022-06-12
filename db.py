import os
import pymysql
import pandas as pd
import numpy as np
import main



db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name =  os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
db_host = os.environ.get('CLOUD_SQL_HOST_NAME')

# model = tf.keras.models.load_model('my_model')
book_data = pd.read_csv('book_dataset.csv')

def db_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    conn = None
    try:
        # if os.environ.get('GAE_ENV') == 'standard':
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
def cosineSim(bookTitle, similarity_data=cosine_sim_df, k=10):
    index = similarity_data.loc[:,bookTitle].to_numpy().argpartition(
        range(-1, -k, -1))
    
    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    
    # Drop nama_resto agar nama resto yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(bookTitle, errors='ignore')
 
    return pd.DataFrame(closest).head(k)

def similiarBooks(title):
    try:
        result = cosineSim(title)
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




def booksRecomendation(uID):
    conn = db_connection()
    cursor = conn.cursor()
    bukuRaw= "SELECT bookID FROM ratingDataset WHERE userID=%s"
    # print(bukuRaw)
    cursor.execute(bukuRaw,(uID,))
    bukuRaw = cursor.fetchall()
    books_have_been_read_by_user = []
    for r in bukuRaw:
        x = r['bookID']
        books_have_been_read_by_user.append(x)
    books_have_been_read_by_user = pd.DataFrame(books_have_been_read_by_user)
    books_have_not_been_read_by_user = book_data[~book_data['books'].isin(books_have_been_read_by_user[0].values)]['books']

    ISBN_encoder = book_data.books.iloc[0:]

    # List data ISBN yang telah diencode pada buku yang dibelum dibaca user
    book_list = [[ISBN_encoder.get(x)] for x in books_have_not_been_read_by_user ]

    user_book_array = np.hstack(([[uID]] * len(book_list), book_list))
    ratings = main.model.predict(user_book_array).flatten()
    # Menentukan top rating buku
    top_ratings_indices = ratings.argsort()[-50:][::-1]
    # Mengambil data ISBN 
    ISBN = book_data.ISBN.iloc[0:]
    # List data ISBN pada top rating buku
    recommended_book_ids  = [ISBN.get(book_list[x][0]) for x in top_ratings_indices]
    recommended_books = book_data[book_data['ISBN'].isin(recommended_book_ids)]['bookTitle']
    
    return recommended_books


def getRecomendationBooks(uId):
    try:
        result = booksRecomendation(uId)
    except:
        return False
    hasilRekomendasi=[]  
    buku = None
    for x in result:
        buku = getOneBook(x)
        hasilRekomendasi.append(buku)
    return hasilRekomendasi

def getbuk(ISBN):
    getBook = book_data[book_data.ISBN.isin([ISBN])]['books']
    getBook = getBook.iloc[0]
    return getBook

def getISBN(books):
    getISBN = book_data[book_data.books.isin([books])]['ISBN']
    getISBN = getISBN.iloc[0]
    return getISBN

def updateRatingsTable(userId,ISBN,bookRating):
    conn = db_connection()
    cursor = conn.cursor()
    sql_Querry = ("INSERT INTO ratingDataset (userID,bookID,bookRating) VALUES (%s, %s, %s)")

    # user = []
    try :
        ISBN = getbuk(ISBN)
        cursor.execute(sql_Querry,(userId,ISBN,bookRating))
        conn.commit()
        buku = getRatedBooks(userId)
        # buku = getRecomendationBooks(userId)
        # for r in rows:
        #     user = r
        return buku
    except:
        # print(e)
        return False

def getRatedBooks(uID):
    conn = db_connection()
    cursor = conn.cursor()
    bukuRaw= "SELECT * FROM ratingDataset WHERE userID=%s"
    # print(bukuRaw)
    
    bukus = []
    bukuIns = None
    try :
        cursor.execute(bukuRaw,(uID,))
        ratedData = cursor.fetchall()
    except:
         return False

    for r in ratedData:
        bukuIns = r
        bookID = bukuIns['bookID']
        userRating = bukuIns['bookRating']
        ISBN = getISBN(bookID)
        title = book_data[book_data.ISBN.isin([ISBN])]['bookTitle']
        # getDbuku = book_data[book_data.ISBN.isin([ISBNr])][['bookTitle'','ISBN','url','bookAuthor','yearOfPublication','bookImage','bookPages','Publisher','bookDesc','bookGenre1','bookGenre2','bookGenre3']]'
        title = title.iloc[0]
        # dictBook = {
        #     "bookTitle" : book[0],
        #     "userBookRating" : bukuIns['bookRating'],
        #     "ISBN" : book[1],
        #     "url" : book[2],
        #     "bookAuthor" : book[3],
        #     "yearOfPublication" : book[4],
        #     "bookImage" : book[5],
        #     "bookPages" : book[6],
        #     "Publisher" : book[7],
        #     "bookDesc" : book[8],
        #     "bookGenre1" : book[9],
        #     "bookGenre2" : book[10],
        #     "bookGenre3" : book[11]
        # }
        dictBook = getOneBook(title)
        dictBook['userRating']=userRating
        bukus.append(dictBook)
    return bukus

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
    sql_Querry = "SELECT * FROM users WHERE email= %s"
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

def rekomendasiDummy():
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    # with conn.cursor() as cursor:
    try:
        cursor.execute("select * from books ORDER BY RAND( ) limit 40")
        rows = cursor.fetchall()
    except pymysql.MySQLError as e:
        return False
    bookObj = []
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
        bookObj.append(dictBook)
    return bookObj
