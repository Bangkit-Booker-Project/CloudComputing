from distutils.debug import DEBUG
from pickle import TRUE
from flask import Flask, request, jsonify
from importlib_metadata import method_cache
import json
import sqlite3
# import pymysql
# pakai %s daripada ?

app = Flask(__name__)
# Koneksi Database
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn



@app.route('/book/<title>', methods=['GET'])
def singleBook(title):
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