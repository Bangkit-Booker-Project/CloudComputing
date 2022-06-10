import sqlite3
import pandas as pd
import re
import numpy as np

# from keras.models import load_model
# import tensorflow as tf
# import tensorflow as tf
# from tensorflow import keras
import pickle

# text = '(0,)' 
# x = re.findall('[0-9]', text)
# # print(x[0])

def dbKonek():
    con = None
    try:
        con = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return con

book_data = pd.read_csv('book_dataset.csv')

model = pickle.load(open('model.pkl', 'rb'))


def bookRecomendation(uID):
    conn = dbKonek()
    cursor = conn.cursor()
    user_id=uID
    bukuRaw= "SELECT bookID FROM ratingDataset WHERE userID=?"
    cursor.execute(bukuRaw,(uID,))
    bukuRaw = cursor.fetchall()
    books_have_been_read_by_user = []

    for r in bukuRaw:
        r=str(r)
        x = re.findall('[0-9]+', r)
        x[0] = int(x[0])
        books_have_been_read_by_user.append(x[0])
    books_have_been_read_by_user = pd.DataFrame(books_have_been_read_by_user)
    books_have_not_been_read_by_user = book_data[~book_data['books'].isin(books_have_been_read_by_user[0].values)]['books'] 
    ISBN_encoder = book_data.books.iloc[0:]

    # List data ISBN yang telah diencode pada buku yang dibelum dibaca user
    book_list = [[ISBN_encoder.get(x)] for x in books_have_not_been_read_by_user ]

    user_book_array = np.hstack(([[uID]] * len(book_list), book_list))
    ratings = model.predict(user_book_array).flatten()
    # Menentukan top rating buku
    top_ratings_indices = ratings.argsort()[-50:][::-1]
    # Mengambil data ISBN 
    ISBN = book_data.ISBN.iloc[0:]
    # List data ISBN pada top rating buku
    recommended_book_ids  = [ISBN.get(book_list[x][0]) for x in top_ratings_indices]
    top_books_recommended = (
        books_have_been_read_by_user.sort_values(
            by = 'bookRating',
            ascending=False
        )
        .head(5)
        .ISBN.values
    )
    # Menentukan buku yang direkomendasikan untuk user
    recommended_books = book_data[book_data['ISBN'].isin(recommended_book_ids)]['bookTitle']
    return user_book_array

print(bookRecomendation(0))

# Menampilkan buku yang direkomendasikan untuk user
# recommended_books = bookRecomendation(0)
# for row in recommended_books.itertuples():
#     print(row)

# print(text)
# for r in text:
#     r=str(r)
#     x = re.findall('[0-9]', r)
#     print(x[0])






    # CREATE TABLE ratingDataset (
    # userId     INTEGER       NOT NULL,
    # bookID     VARCHAR (20)  NOT NULL,
    # bookRating DOUBLE        NOT NULL,
    # bookTitle  VARCHAR (255) NOT NULL);
