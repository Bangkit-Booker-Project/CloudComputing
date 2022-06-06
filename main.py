from functools import wraps
from pickle import TRUE
from flask import Flask, make_response, request, jsonify,render_template
import json
# import sqlite3
import jwt
import datetime
# import pandas as pd
# import numpy as np
import db
# import firebase_admin
# import pyrebase
# import pymysql
# pakai %s daripada ?

app = Flask(__name__)

# validasi token untuk user login
app.config['SECRET_KEY'] = "thisisthesecretkey"

def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #https://www.dasjdoenifes.com/route?token=dfjnewifnifnmemfllsenfioesnfesf
        data = None
        if not token:
            return jsonify({'message' : 'Token is missing'}), 403
        try:
            data = jwt.decode(token, 'thisisthesecretkey', algorithms=['HS256'])
        except:
            return jsonify({'message' : 'Token {} is invalid!'.format(token)}), 403
        return f(*args, **kwargs)

    return decorated

# Koneksi Database
# def db_connection():
#     conn = None
#     try:
#         conn = pymysql.connect("books.sqlite")
#     except sqlite3.error as e:
#         print(e)
#     return conn

## COSINE
# conn_cosine = db_connection()
# cursor_cosine = conn_cosine.cursor()
# cursor_cosine.execute("SELECT * FROM books")
# book_data_SQL = cursor_cosine.fetchall()
# book_data = pd.DataFrame(book_data_SQL, columns=['bookTitle', 'bookRating', 'ISBN','bookAuthor','yearOfPublication','Publisher','url','bookImage','bookDesc','ratingCount','bookPages','bookGenres','bookGenre1','bookGenre2','bookGenre3'])
# book_data_filtered = book_data[['ISBN', 'bookTitle', 'bookAuthor', 'bookGenre1', 'bookGenre2', 'bookGenre3', 'bookGenres']]


# cosine_sim_df = pd.read_csv('cosine.csv')
# cosine_sim_df = cosine_sim_df.drop(cosine_sim_df.columns[0], axis=1)

# def books_recommendations(bookTitle, similarity_data=cosine_sim_df, k=10):
#     index = similarity_data.loc[:,bookTitle].to_numpy().argpartition(
#         range(-1, -k, -1))
    
#     # Mengambil data dengan similarity terbesar dari index yang ada
#     closest = similarity_data.columns[index[-1:-(k+2):-1]]
    
#     # Drop nama_resto agar nama resto yang dicari tidak muncul dalam daftar rekomendasi
#     closest = closest.drop(bookTitle, errors='ignore')
 
#     return pd.DataFrame(closest).head(k)

# # Get One Book
# def getOneBook(title):
#     conn = db.db_connection()
#     cursor = conn.cursor()
#     book = None
#     cursor.execute("SELECT * FROM books WHERE bookTitle=?", (title,))
#     rows = cursor.fetchall()
#     for r in rows:
#         book = r
#     if book is not None:
#         dictBook = {
#             "bookTitle" : book[0],
#             "bookRating" : book[1],
#             "ISBN" : book[2],
#             "bookAuthor" : book[3],
#             "yearOfPublication" : book[4],
#             "Publisher" : book[5],
#             "url" : book[6],
#             "bookImage" : book[7],
#             "bookDesc" : book[8],
#             "ratingCount" : book[9],
#             "bookPages" : book[10],
#             "bookGenres" : book[11],
#             "bookGenre1" : book[12],
#             "bookGenre2" : book[13],
#             "bookGenre3" : book[14]
#         }
#     return dictBook

# Api testing saja bukan real api 
@app.route('/')
def dokumentasi():
    return render_template('index.html')

@app.route('/protected')
# @tokenRequired
def protected():
    return jsonify({'message' : 'Only Available For people that have token'})
    
@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone Can See This'})


# API untuk Login User
@app.route('/login', methods=['POST'])
def login():
    auth = request
    if auth.form['password'] == 'password':
    # if auth and auth.password == 'password':
        token = jwt.encode({'user' : auth.form['username'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token})
        # return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Tidak dapat diverivikasi', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


# API untuk melakukan querry satu buku berdasarkan nama buku
@app.route('/book/<title>', methods=['GET'])
# @tokenRequired
def getSingleBook(title):
    # print(title)
    book = db.getOneBook(title)
    if book:
        # json_object = json.loads(book)
        # json_formatted_str = json.dumps(book, indent=4)
        return jsonify(book), 200
        # return jsonify(book, indent=2), 200
        # return jsonify(book), 200
    else:
        return jsonify("Book Named {} Not Existing".format(title)), 404


# Querry 20 rating buku tertinggi berdasarkan genre
@app.route('/topRatings/<genre>', methods=['GET'])
# @tokenRequired
def topRatingByGenre(genre):
    listObj = db.topRatingByGenre(genre)
    if listObj:
        # json_object = json.loads(listObj)
        # json_formatted_str = json.dumps(listObj, indent=4)
        return jsonify(listObj), 200
        # return jsonify(listObj,indent=2), 200
    else:
        return jsonify("Book with genre {} Not Existing".format(genre)), 404

# COSINE SIMILARITY
@app.route('/similiarBooks/<title>', methods=['GET'])
# @tokenRequired
def similiarBooks(title):
    try:
        sim=db.similiarBooks(title)
        return jsonify(sim), 200
    except:
        return jsonify("Book Named {} Not Existing".format(title)), 404

# User activities




if __name__ == '__main__':
    app.run(debug=False)