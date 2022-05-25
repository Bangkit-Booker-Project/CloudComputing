from functools import wraps
from flask import Flask, make_response, request, jsonify
import json
import sqlite3
import jwt
import datetime
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
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

# Api testing saja bukan real api 
@app.route('/protected')
@tokenRequired
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


# API untuk melakukan querry buku berdasarkan nama buku
@app.route('/book/<title>', methods=['GET'])
def getSingleBook(title):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    cursor.execute("SELECT * FROM books WHERE bookTitle=?", (title,))
    rows = cursor.fetchall()
    for r in rows:
        book = r
    if book is not None:
        dictBook = {
            "bookTitle" : book[0],
            "bookRating" : book[1],
            "ISBN" : book[2],
            "bookAuthor" : book[3],
            "yearOfPublication" : book[4],
            "Publisher" : book[5],
            "url" : book[6],
            "bookImage" : book[7],
            "bookDesc" : book[8],
            "ratingCount" : book[9],
            "bookPages" : book[10],
            "bookGenres" : book[11]
        }
        return jsonify(dictBook), 200
    else:
        return "Book Named {} Not Existing".format(title), 404



if __name__ == '__main__':
    app.run(debug=True)