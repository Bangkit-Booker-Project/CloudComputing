**Dokumentasi Backend Booker Project**
--------------------------------------

### Untuk mendapatkan satu buku bedasarkan Nama Buku

*   **API :** bangkit-booker-352402.et.r.appspot.com/book/<NamaBuku>
*   **Method :** GET
*   **Keterangan :** Ganti <NamaBuku> Sesuai Buku yang ingin dicari, nama buku case sensitive (jika tidak sesuai huruf besar dan kecil akan) mengembalikan error.
*   **Contoh :**[https://bangkit-booker-352402.et.r.appspot.com/book/The%20Sight](https://bangkit-booker-352402.et.r.appspot.com/book/The%20Sight "https://bangkit-booker-352402.et.r.appspot.com/book/The%20Sight")

### Untuk mendapatkan 10 similiar book (Cosine Similarity) bedasarkan Nama Buku

*   **API :** https://bangkit-booker-352402.et.r.appspot.com/similiarBooks/<NamaBuku>
*   **Method :** GET
*   **Keterangan :** Ganti <NamaBuku> Sesuai Buku yang ingin dicari, nama buku case sensitive (jika tidak sesuai huruf besar dan kecil akan mengembalikan error.)
*   **Contoh :** [https://bangkit-booker-352402.et.r.appspot.com/similiarBooks/The%20Sight](https://bangkit-booker-352402.et.r.appspot.com/similiarBooks/The%20Sight "https://bangkit-booker-352402.et.r.appspot.com/similiarBooks/The%20Sight")

### Untuk mendapatkan 20 top Ratings Book bedasarkan Genre Buku

*   **API :** https://bangkit-booker-352402.et.r.appspot.com/topRatings/<Genre>
*   **Method :** GET
*   **Keterangan :** Ganti <Genre> Sesuai Buku yang ingin dicari, nama Genre case sensitive (jika tidak sesuai huruf besar dan kecil akan mengembalikan error.)
*   **Contoh :** [https://bangkit-booker-352402.et.r.appspot.com/topRatings/Classics](https://bangkit-booker-352402.et.r.appspot.com/topRatings/Classics "https://bangkit-booker-352402.et.r.appspot.com/topRatings/Classics")

\*Untuk melihat hasil APInya Disarankan untuk menggunakan mozilla firefox untuk tampilan yang lebih rapih