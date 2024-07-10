from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database initialization
conn = sqlite3.connect('library.db')
conn.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              author TEXT NOT NULL)''')
conn.commit()
conn.close()


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = sqlite3.connect('library.db')
        conn.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        conn.commit()
        conn.close()

        return redirect(url_for('view_books'))

    return render_template('add_book.html')


@app.route('/view_books')
def view_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    return render_template('view_books.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
