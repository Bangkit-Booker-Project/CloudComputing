html { scroll-behavior: smooth; }  BOOKER API Documentation     

*   [Bangkit BOOKER](#booker "Dicoding Story")

*   [Endpoint](#endpoint "Endpoint")

*   [Register](#register "Register")
*   [Login](#login "Login")
*   [Reset Password](#reset-password "Reset password")
*   [Search Books by random input](#search-books-by-random-input "Search Books")
*   [Find Book by Title](#find-books-by-title "Find Book")
*   [Top Rating Book by Genre](#top-rating-book-by-genre "Top Rating Book by Genre")
*   [Similiar Book by Title](#similiar-book-by-title "Similiar Book by Title")

Bangkit Booker
==============

> API untuk Book rekomendation based on user preferences

[Endpoint](#endpoint)
---------------------

[https://bangkit-booker-352402.et.r.appspot.com](https://bangkit-booker-352402.et.r.appspot.com/)

### Register

*   URL
    *   `/register`
*   Method
    *   POST
*   Request Body
    *   `username` as `string`
    *   `email` as `string`, must be unique
    *   `password` as `string`, must be at least 6 characters
*   Response
    
        {
          "error": false,
          "message": "User Created Successfully"
        }
    

### Login

*   URL
    *   `/login`
*   Method
    *   POST
*   Request Body
    *   `email` as `string`
    *   `password` as `string`
*   Response
    
        {
          "error": false,
          "message": "User login successfully",
          "result": {
              "email": "admin",
              "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoyLCJleHAiOjE2NTU0NTY2MTB9.nfsZEjaXxPt4g0eeRHtA3zyR8XQzxamROgcUySP9S3I",
              "uid": 2,
              "username": "admin"
        }
    

### Reset Password

*   URL
    *   `/resetPassword`
*   Method
    *   POST
*   Request Body
    *   `password` as `string`
*   Parameter
    
    *   `token` as `string`
    
    *   Example
    
        https://bangkit-booker-352402.et.r.appspot.com/resetPassword?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoyLCJleHAiOjE2NTU0MzMyNjN9.N1ENZiHGss-W9gnyAIx-Fv6NvuYM-lUtSwNLgapk97U
    
*   Response
    
        {
          "error": false,
          "message": "Password Changed"
        }
    

### Search Books by random input

*   URL
    *   `/search/[randomString]`
*   Method
    *   GET
*   Response
    
        {
          "error": false,
          "message": "Books fetched successfully",
          "result":[
              {
                  "ISBN": "345379632",
                  "Publisher": "Ballantine Books",
                  "bookAuthor": "Terry Brooks",
                  "bookDesc": "Eight centuries ago the first Knight of the Word was commissioned to combat the demonic evil of the Void. Now that daunting legacy has passed to John Ross - along with powerful magic and the knowledge that his actions are all that stand between a living hell and humanity's future.Then, after decades of service to the Word, an unspeakable act of violence shatters John Ross's weary faith. Haunted by guilt, he turns his back on his dread gift, settling down to build a normal life, untroubled by demons and nightmares.But a fallen Knight makes a tempting prize for the Void, which could bend the Knight's magic to its own evil ends. And once the demons on Ross's trail track him to Seattle, neither he nor anyone close to him will be safe. His only hope is Nest Freemark, a college student who wields an extraordinary magic all her own. Five years earlier, Ross had aided Nest when the future of humanity rested upon her choice between Word and Void. Now Nest must return the favor. She must restore Ross's faith, or his life - and hers - will be forfeit...",
                  "bookGenre1": "Fantasy",
                  "bookGenre2": "Fantasy-UrbanFantasy",
                  "bookGenre3": "Fiction",
                  "bookGenres": "['Fantasy', 'Fantasy-UrbanFantasy', 'Fiction', 'ScienceFictionFantasy', 'ScienceFiction', 'Fantasy-Magic', 'Fantasy-EpicFantasy', 'Paranormal-Demons', 'Horror', 'Epic']",
                  "bookImage": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1403811542l/420496.jpg",
                  "bookPages": "386 pages",
                  "bookRating": 4.05,
                  "bookTitle": "A Knight of the Word",
                  "ratingCount": 14502,
                  "url": "https://www.goodreads.com/book/show/420496.A_Knight_of_the_Word",
                  "yearOfPublication": "1998"
              },
              {
                "ISBN": "380789019",
                "Publisher": "Avon",
                "bookAuthor": "Neil Gaiman",
                "bookDesc": "Under the streets of London there's a place most people could never even dream of. A city of monsters and saints, murderers and angels, knights in armour and pale girls in black velvet. This is the city of the people who have fallen between the cracks.Richard Mayhew, a young businessman, is going to find out more than enough about this other London. A single act of kindness catapults him out of his workday existence and into a world that is at once eerily familiar and utterly bizarre. And a strange destiny awaits him down here, beneath his native city: Neverwhere.",
                "bookGenre1": "Fantasy",
                "bookGenre2": "Fiction",
                "bookGenre3": "Fantasy-UrbanFantasy",
                "bookGenres": "['Fantasy', 'Fiction', 'Fantasy-UrbanFantasy', 'Audiobook', 'ScienceFictionFantasy', 'ScienceFiction', 'Adventure', 'Horror', 'YoungAdult', 'Adult']",
                "bookImage": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1348747943l/14497.jpg",
                "bookPages": "370 pages",
                "bookRating": 4.16,
                "bookTitle": "Neverwhere",
                "ratingCount": 450266,
                "url": "https://www.goodreads.com/book/show/14497.Neverwhere",
                "yearOfPublication": "1998"
            }
          ]
        }
    

### Find Books by Title

*   URL
    *   `/book/[Title]`
*   Method
    *   GET
*   Response
    
        {
          "error": false,
          "message": "Books fetched successfully",
          "result":
              {
                  "ISBN": "345379632",
                  "Publisher": "Ballantine Books",
                  "bookAuthor": "Terry Brooks",
                  "bookDesc": "Eight centuries ago the first Knight of the Word was commissioned to combat the demonic evil of the Void. Now that daunting legacy has passed to John Ross - along with powerful magic and the knowledge that his actions are all that stand between a living hell and humanity's future.Then, after decades of service to the Word, an unspeakable act of violence shatters John Ross's weary faith. Haunted by guilt, he turns his back on his dread gift, settling down to build a normal life, untroubled by demons and nightmares.But a fallen Knight makes a tempting prize for the Void, which could bend the Knight's magic to its own evil ends. And once the demons on Ross's trail track him to Seattle, neither he nor anyone close to him will be safe. His only hope is Nest Freemark, a college student who wields an extraordinary magic all her own. Five years earlier, Ross had aided Nest when the future of humanity rested upon her choice between Word and Void. Now Nest must return the favor. She must restore Ross's faith, or his life - and hers - will be forfeit...",
                  "bookGenre1": "Fantasy",
                  "bookGenre2": "Fantasy-UrbanFantasy",
                  "bookGenre3": "Fiction",
                  "bookGenres": "['Fantasy', 'Fantasy-UrbanFantasy', 'Fiction', 'ScienceFictionFantasy', 'ScienceFiction', 'Fantasy-Magic', 'Fantasy-EpicFantasy', 'Paranormal-Demons', 'Horror', 'Epic']",
                  "bookImage": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1403811542l/420496.jpg",
                  "bookPages": "386 pages",
                  "bookRating": 4.05,
                  "bookTitle": "A Knight of the Word",
                  "ratingCount": 14502,
                  "url": "https://www.goodreads.com/book/show/420496.A_Knight_of_the_Word",
                  "yearOfPublication": "1998"
              }
        }
    

### Top Rating Book by Genre

*   URL
    *   `/topRatings/[Genre]`
*   Method
    *   GET
*   Response
    
        {
          "error": false,
          "message": "Books fetched successfully",
          "result":
              {
                  "ISBN": "345379632",
                  "Publisher": "Ballantine Books",
                  "bookAuthor": "Terry Brooks",
                  "bookDesc": "Eight centuries ago the first Knight of the Word was commissioned to combat the demonic evil of the Void. Now that daunting legacy has passed to John Ross - along with powerful magic and the knowledge that his actions are all that stand between a living hell and humanity's future.Then, after decades of service to the Word, an unspeakable act of violence shatters John Ross's weary faith. Haunted by guilt, he turns his back on his dread gift, settling down to build a normal life, untroubled by demons and nightmares.But a fallen Knight makes a tempting prize for the Void, which could bend the Knight's magic to its own evil ends. And once the demons on Ross's trail track him to Seattle, neither he nor anyone close to him will be safe. His only hope is Nest Freemark, a college student who wields an extraordinary magic all her own. Five years earlier, Ross had aided Nest when the future of humanity rested upon her choice between Word and Void. Now Nest must return the favor. She must restore Ross's faith, or his life - and hers - will be forfeit...",
                  "bookGenre1": "Fantasy",
                  "bookGenre2": "Fantasy-UrbanFantasy",
                  "bookGenre3": "Fiction",
                  "bookGenres": "['Fantasy', 'Fantasy-UrbanFantasy', 'Fiction', 'ScienceFictionFantasy', 'ScienceFiction', 'Fantasy-Magic', 'Fantasy-EpicFantasy', 'Paranormal-Demons', 'Horror', 'Epic']",
                  "bookImage": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1403811542l/420496.jpg",
                  "bookPages": "386 pages",
                  "bookRating": 4.05,
                  "bookTitle": "A Knight of the Word",
                  "ratingCount": 14502,
                  "url": "https://www.goodreads.com/book/show/420496.A_Knight_of_the_Word",
                  "yearOfPublication": "1998"
              }
        }


### Similiar Book by Title

*   URL
    *   `/similiarBooks/[Title]`
*   Method
    *   GET
*   Response
    
        {
          "error": false,
          "message": "Books fetched successfully",
          "result":
              {
                  "ISBN": "345379632",
                  "Publisher": "Ballantine Books",
                  "bookAuthor": "Terry Brooks",
                  "bookDesc": "Eight centuries ago the first Knight of the Word was commissioned to combat the demonic evil of the Void. Now that daunting legacy has passed to John Ross - along with powerful magic and the knowledge that his actions are all that stand between a living hell and humanity's future.Then, after decades of service to the Word, an unspeakable act of violence shatters John Ross's weary faith. Haunted by guilt, he turns his back on his dread gift, settling down to build a normal life, untroubled by demons and nightmares.But a fallen Knight makes a tempting prize for the Void, which could bend the Knight's magic to its own evil ends. And once the demons on Ross's trail track him to Seattle, neither he nor anyone close to him will be safe. His only hope is Nest Freemark, a college student who wields an extraordinary magic all her own. Five years earlier, Ross had aided Nest when the future of humanity rested upon her choice between Word and Void. Now Nest must return the favor. She must restore Ross's faith, or his life - and hers - will be forfeit...",
                  "bookGenre1": "Fantasy",
                  "bookGenre2": "Fantasy-UrbanFantasy",
                  "bookGenre3": "Fiction",
                  "bookGenres": "['Fantasy', 'Fantasy-UrbanFantasy', 'Fiction', 'ScienceFictionFantasy', 'ScienceFiction', 'Fantasy-Magic', 'Fantasy-EpicFantasy', 'Paranormal-Demons', 'Horror', 'Epic']",
                  "bookImage": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1403811542l/420496.jpg",
                  "bookPages": "386 pages",
                  "bookRating": 4.05,
                  "bookTitle": "A Knight of the Word",
                  "ratingCount": 14502,
                  "url": "https://www.goodreads.com/book/show/420496.A_Knight_of_the_Word",
                  "yearOfPublication": "1998"
              }
              ...
        }
    
### Top Rating Book by Genre

*   URL
    *   `/topRatings/[Genre]`
*   Method
    *   GET
*   Response
    
        {
          "error": false,
          "message": "Books fetched successfully",
          "result":
              {
                  "ISBN": "345379632",
                  "Publisher": "Ballantine Books",
                  "bookAuthor": "Terry Brooks",
                  "bookDesc": "Eight centuries ago the first Knight of the Word was commissioned to combat the demonic evil of the Void. Now that daunting legacy has passed to John Ross - along with powerful magic and the knowledge that his actions are all that stand between a living hell and humanity's future.Then, after decades of service to the Word, an unspeakable act of violence shatters John Ross's weary faith. Haunted by guilt, he turns his back on his dread gift, settling down to build a normal life, untroubled by demons and nightmares.But a fallen Knight makes a tempting prize for the Void, which could bend the Knight's magic to its own evil ends. And once the demons on Ross's trail track him to Seattle, neither he nor anyone close to him will be safe. His only hope is Nest Freemark, a college student who wields an extraordinary magic all her own. Five years earlier, Ross had aided Nest when the future of humanity rested upon her choice between Word and Void. Now Nest must return the favor. She must restore Ross's faith, or his life - and hers - will be forfeit...",
                  "bookGenre1": "Fantasy",
                  "bookGenre2": "Fantasy-UrbanFantasy",
                  "bookGenre3": "Fiction",
                  "bookGenres": "['Fantasy', 'Fantasy-UrbanFantasy', 'Fiction', 'ScienceFictionFantasy', 'ScienceFiction', 'Fantasy-Magic', 'Fantasy-EpicFantasy', 'Paranormal-Demons', 'Horror', 'Epic']",
                  "bookImage": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1403811542l/420496.jpg",
                  "bookPages": "386 pages",
                  "bookRating": 4.05,
                  "bookTitle": "A Knight of the Word",
                  "ratingCount": 14502,
                  "url": "https://www.goodreads.com/book/show/420496.A_Knight_of_the_Word",
                  "yearOfPublication": "1998"
              }
        }

### Get Book Recomendation For User

*   URL
    *   `/recomendation`
*   Method
    *   GET

*   Parameter
    
    *   `token` as `string`
    
    *   Example
    
        https://bangkit-booker-352402.et.r.appspot.com/recomendation?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoyLCJleHAiOjE2NTU0MzMyNjN9.N1ENZiHGss-W9gnyAIx-Fv6NvuYM-lUtSwNLgapk97U
    
*   Response

        {
          "error": false,
          "message": "Books fetched successfully",
          "result":[
              {
                  "ISBN": "345379632",
                  "Publisher": "Ballantine Books",
                  "bookAuthor": "Terry Brooks",
                  "bookDesc": "Eight centuries ago the first Knight of the Word was commissioned to combat the demonic evil of the Void. Now that daunting legacy has passed to John Ross - along with powerful magic and the knowledge that his actions are all that stand between a living hell and humanity's future.Then, after decades of service to the Word, an unspeakable act of violence shatters John Ross's weary faith. Haunted by guilt, he turns his back on his dread gift, settling down to build a normal life, untroubled by demons and nightmares.But a fallen Knight makes a tempting prize for the Void, which could bend the Knight's magic to its own evil ends. And once the demons on Ross's trail track him to Seattle, neither he nor anyone close to him will be safe. His only hope is Nest Freemark, a college student who wields an extraordinary magic all her own. Five years earlier, Ross had aided Nest when the future of humanity rested upon her choice between Word and Void. Now Nest must return the favor. She must restore Ross's faith, or his life - and hers - will be forfeit...",
                  "bookGenre1": "Fantasy",
                  "bookGenre2": "Fantasy-UrbanFantasy",
                  "bookGenre3": "Fiction",
                  "bookGenres": "['Fantasy', 'Fantasy-UrbanFantasy', 'Fiction', 'ScienceFictionFantasy', 'ScienceFiction', 'Fantasy-Magic', 'Fantasy-EpicFantasy', 'Paranormal-Demons', 'Horror', 'Epic']",
                  "bookImage": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1403811542l/420496.jpg",
                  "bookPages": "386 pages",
                  "bookRating": 4.05,
                  "bookTitle": "A Knight of the Word",
                  "ratingCount": 14502,
                  "url": "https://www.goodreads.com/book/show/420496.A_Knight_of_the_Word",
                  "yearOfPublication": "1998"
              }
            .... up to 50 book....
            ]
        }
    

### update buku yang dirating user

*   URL
    *   `/updateReadBook`
*   Method
    *   POST
*   Request Body
    *   `ISBN` as `string`
    *   `bookRating` as `double`
*   Parameter
    
    *   `token` as `string`
    
    *   Example
    
        https://bangkit-booker-352402.et.r.appspot.com/recomendation?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoyLCJleHAiOjE2NTU0MzMyNjN9.N1ENZiHGss-W9gnyAIx-Fv6NvuYM-lUtSwNLgapk97U
    
*   Response

        {
          "error": false,
          "message": "Data Updated successfully",
          "book recomendation":[
              {
                  "ISBN": "345379632",
                  "Publisher": "Ballantine Books",
                  "bookAuthor": "Terry Brooks",
                  "bookDesc": "Eight centuries ago the first Knight of the Word was commissioned to combat the demonic evil of the Void. Now that daunting legacy has passed to John Ross - along with powerful magic and the knowledge that his actions are all that stand between a living hell and humanity's future.Then, after decades of service to the Word, an unspeakable act of violence shatters John Ross's weary faith. Haunted by guilt, he turns his back on his dread gift, settling down to build a normal life, untroubled by demons and nightmares.But a fallen Knight makes a tempting prize for the Void, which could bend the Knight's magic to its own evil ends. And once the demons on Ross's trail track him to Seattle, neither he nor anyone close to him will be safe. His only hope is Nest Freemark, a college student who wields an extraordinary magic all her own. Five years earlier, Ross had aided Nest when the future of humanity rested upon her choice between Word and Void. Now Nest must return the favor. She must restore Ross's faith, or his life - and hers - will be forfeit...",
                  "bookGenre1": "Fantasy",
                  "bookGenre2": "Fantasy-UrbanFantasy",
                  "bookGenre3": "Fiction",
                  "bookGenres": "['Fantasy', 'Fantasy-UrbanFantasy', 'Fiction', 'ScienceFictionFantasy', 'ScienceFiction', 'Fantasy-Magic', 'Fantasy-EpicFantasy', 'Paranormal-Demons', 'Horror', 'Epic']",
                  "bookImage": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1403811542l/420496.jpg",
                  "bookPages": "386 pages",
                  "bookRating": 4.05,
                  "bookTitle": "A Knight of the Word",
                  "ratingCount": 14502,
                  "url": "https://www.goodreads.com/book/show/420496.A_Knight_of_the_Word",
                  "yearOfPublication": "1998"
              }
            .... up to 50 book....
            ]
        }
        
window.$docsify = { name: '', repo: '' }