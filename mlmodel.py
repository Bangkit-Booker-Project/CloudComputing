import onnxruntime
import pathlib
import sqlite3
import pandas as pd
# import re
import numpy as np
import db

ONNX_SESSION = None

def get_session():
    global ONNX_SESSION
    if ONNX_SESSION == None:
        model_path = str(pathlib.Path("model.onnx"))
        sess = onnxruntime.InferenceSession(model_path)
        ONNX_SESSION = sess
    return ONNX_SESSION
    

book_data = pd.read_csv('book_dataset.csv')

def predict(uId):
    onnx_sess = get_session()
    sess_inputs = onnx_sess.get_inputs()[0]
    conn = db.db_connection()
    cursor = conn.cursor()
    user_id=uId
    bukuRaw= "SELECT bookID FROM ratingDataset WHERE userID=%s"
    cursor.execute(bukuRaw,(user_id,))
    bukuRaw = cursor.fetchall()
    books_have_been_read_by_user = []

    for r in bukuRaw:
        x = r['bookID']
        books_have_been_read_by_user.append(x)
        # books_have_been_read_by_user.append(x[0])
    books_have_been_read_by_user = pd.DataFrame(books_have_been_read_by_user)
    books_have_not_been_read_by_user = book_data[~book_data['books'].isin(books_have_been_read_by_user[0].values)]['books']

    ISBN_encoder = book_data.books.iloc[0:]

    # List data ISBN yang telah diencode pada buku yang dibelum dibaca user
    book_list = [[ISBN_encoder.get(x)] for x in books_have_not_been_read_by_user ]

    user_book_array = np.hstack(([[uId]] * len(book_list), book_list))
    ratings = onnx_sess.run(None, {sess_inputs.name:user_book_array})
    # list(itertools.chain.from_iterable(ratings))
    # Menentukan top rating buku
    ratings = np.array(ratings).flatten()

    top_ratings_indices = ratings.argsort()[-50:][::-1]
    # Mengambil data ISBN 
    ISBN = book_data.ISBN.iloc[0:]
    # List data ISBN pada top rating buku
    recommended_book_ids  = [ISBN.get(book_list[x][0]) for x in top_ratings_indices]

    book_sort = book_data[book_data.books.isin(books_have_been_read_by_user[0])][['bookTitle', 'bookRating', 'bookGenres', 'ISBN']]
    top_books_recommended = (
        book_sort.sort_values(
            by = 'bookRating',
            ascending=False
        )
        .head(5)
        .ISBN.values
    )
    # Menentukan buku yang direkomendasikan untuk user
    recommended_books = book_data[book_data['ISBN'].isin(recommended_book_ids)]['bookTitle']
    return recommended_books
