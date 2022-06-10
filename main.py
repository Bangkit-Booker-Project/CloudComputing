from functools import wraps
from flask import Flask, make_response, request, jsonify,render_template
import jwt
import datetime
import db
import os
import hashlib
import string    
import random # define the random module 

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# app = Flask(__name__, static_folder="your path to static")

# validasi token untuk user login
app.config['SECRET_KEY'] = "thisisthesecretkey"
dataJWT = None
def tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #https://www.dasjdoenifes.com/route?token=dfjnewifnifnmemfllsenfioesnfesf
        data = None
        if not token:
            return jsonify({'message' : 'Token is missing'}), 403
        try:
            global dataJWT 
            dataJWT = jwt.decode(token, 'thisisthesecretkey', algorithms=['HS256'])
        except:
            return jsonify({'message' : 'Token {} is invalid!'.format(token)}), 403
        return f(*args, **kwargs)

    return decorated

respon={
  "error" : True,
  "message" : "",
}
# Api testing saja bukan real api 
@app.route('/')
def dokumentasi():
    return render_template('index.html')

@app.route('/protected', methods=['GET','POST'])
@tokenRequired
def protected():
    return jsonify(dataJWT)
    
@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone Can See This'})


# API untuk melakukan querry satu buku berdasarkan nama buku
@app.route('/book/<title>', methods=['GET'])
def getSingleBook(title):
    book = db.getOneBook(title)
    res=respon
    if book:
        res["error"] = False
        res["message"] = "Book fetched successfully"
        res['result'] = book
        return jsonify(res), 200
    else:
        res["error"] = True
        res["message"] = "Book Named {} Not Existing".format(title)
        return jsonify(res), 400

# Untuk search buku random name
@app.route('/search/<random>', methods=['GET'])
def searchBook(random):
    book = db.searchRandomTitle(random)
    res=respon
    if book:
        res["error"] = False
        res["message"] = "Books fetched successfully"
        res['result'] = book
        return jsonify(res), 200
    else:
        res["error"] = True
        res["message"] = "Books With {} Not Existing".format(random)
        return jsonify(res), 400


# Querry 20 rating buku tertinggi berdasarkan genre
@app.route('/topRatings/<genre>', methods=['GET'])
def topRatingByGenre(genre):
    books = db.topRatingByGenre(genre)
    res=respon
    if books:
        res["error"] = False
        res["message"] = "Book fetched successfully"
        res['result'] = books
        return jsonify(res), 200
    else:
        res["error"] = True
        res["message"] = "Book with Genre {} Not Existing".format(genre)
        return jsonify(res), 400

# COSINE SIMILARITY
@app.route('/similiarBooks/<title>', methods=['GET'])
# @tokenRequired
def similiarBooks(title):
    sim=db.similiarBooks(title)
    res=respon
    if sim is not False:
        res["error"] = False
        res["message"] = "Similiar book fetched successfully"
        res['result'] = sim
        return jsonify(res), 200
    else:
        res["error"] = True
        res["message"] = "Book Named {} Not Existing".format(title)
        return jsonify(res), 400
        

# User activities
# belum dideploy

def encodePW(pw):
    salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12)) 
    key = pw.encode()
    key = hashlib.sha256(key)
    key = key.hexdigest()
    encPW = salt+key
    return encPW
    
def verifPw(dbPW,inputPW):
    salt = dbPW[:12]
    key = dbPW[12:]
    inputPW = inputPW.encode()
    inputPW = hashlib.sha256(inputPW)
    encodedPW = inputPW.hexdigest()
    
    if key == encodedPW:
        return True
    else:
        return False

# def encodePW(pw):
#     salt = os.urandom(12)
#     key = hashlib.pbkdf2_hmac('sha256', pw.encode('utf-8'), salt, 100000)
#     encPW = salt+key
#     return encPW

# def verifPw(dbPW,inputPW):
#     salt = dbPW[:12]
#     key = dbPW[12:]
#     encodedPW = hashlib.pbkdf2_hmac('sha256',inputPW.encode('utf-8'),salt, 100000)
#     if key == encodedPW:
#         return True
#     else:
#         return False

# for register new user
@app.route('/register', methods=['POST'])
def register():
    auth = request
    uEmail = auth.form['email']
    uPass = auth.form['password']
    uName = auth.form['username']
    res = respon
    uPass = encodePW(uPass)
    userD = db.regsisterUser(uEmail,uPass,uName)
    if userD is False:
        res["error"] = False
        res["message"] = "User Created Successfully"
        # res['result'] = userD
        return jsonify(res), 200
    else:
        res["error"] = True
        res["message"] = "User with Email {} Already Existing".format(uEmail)
        return jsonify(res), 400

# API untuk Login User
@app.route('/login', methods=['POST'])
def login():
    auth = request
    uEmail = auth.form['email']
    res=respon
    userD = db.loginUser(uEmail)
    if userD is False:
        res["error"] = True
        res["message"] = 'Wrong Email'
        return jsonify(res), 400
    passwordD = userD['password']
    # print(passwordD)
    inPassword = auth.form['password']
    pswd = verifPw(passwordD, inPassword)
    # print(pswd)
    if pswd:
    # if auth and auth.password == 'password':
        token = jwt.encode({'user' : userD['id'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7)}, app.config['SECRET_KEY'])
        res['error'] = False
        res['message'] = "User login successfully"
        res['result']= {
            'uid' : userD['id'],
            'email' : userD['email'],
            'username' : userD['username'],
            'token' : token
        }
        return jsonify(res), 200
    else:
        res["error"] = True
        res["message"] = 'Wrong Password'
        return jsonify(res), 400

# API untuk reset password
@app.route('/resetPassword', methods=['POST'])
@tokenRequired
def resetPassword():
    auth = request
    # uEmail = auth.form['email']
    uPass = auth.form['password']
    # uName = auth.form['username']
    uId = dataJWT["user"]
    
    res = respon
    uPass = encodePW(uPass)
    userD = db.resetPassword(uId,uPass)
    if userD is not False:  
        res["error"] = False
        res["message"] = "Password Changed"
        # res['result'] = userD
        return jsonify(res), 200
    else:
        res["error"] = True
        res["message"] = "Password Failed to Changed"
        return jsonify(res), 400
    # return jsonify('berhasil')




if __name__ == '__main__':
    app.run(debug=True)