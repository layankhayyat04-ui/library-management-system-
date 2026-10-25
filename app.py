from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'change-this-in-production'

DATABASE = 'library.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                total_copies INTEGER NOT NULL DEFAULT 1,
                available_copies INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS checkouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                borrower_name TEXT NOT NULL,
                checkout_date TEXT NOT NULL,
                returned INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (book_id) REFERENCES books(id)
            );
        ''')

        # Seed data if empty
        count = db.execute('SELECT COUNT(*) FROM books').fetchone()[0]
        if count == 0:
            db.executemany(
                'INSERT INTO books (title, author, category, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)',
                [
                    ('Clean Code', 'Robert C. Martin', 'Software Engineering', 3, 2),
                    ('The Pragmatic Programmer', 'David Thomas', 'Software Engineering', 2, 2),
                    ('Thinking, Fast and Slow', 'Daniel Kahneman', 'Psychology', 2, 1),
                    ('Atomic Habits', 'James Clear', 'Self-Development', 4, 4),
                    ('Designing Data-Intensive Applications', 'Martin Kleppmann', 'Data Engineering', 2, 2),
                    ('Deep Work', 'Cal Newport', 'Self-Development', 3, 3),
                    ('The Lean Startup', 'Eric Ries', 'Business', 2, 0),
                    ('Zero to One', 'Peter Thiel', 'Business', 3, 2),
                ]
            )


@app.route('/')
def index():
    db = get_db()
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    query = 'SELECT * FROM books WHERE 1=1'
    params = []

    if search:
        query += ' AND (LOWER(title) LIKE ? OR LOWER(author) LIKE ?)'
        params += [f'%{search.lower()}%', f'%{search.lower()}%']

    if category:
        query += ' AND category = ?'
        params.append(category)

    books = db.execute(query, params).fetchall()
    categories = [r['category'] for r in db.execute('SELECT DISTINCT category FROM books ORDER BY category').fetchall()]

    total = db.execute('SELECT COUNT(*) FROM books').fetchone()[0]
    available = db.execute('SELECT SUM(available_copies) FROM books').fetchone()[0] or 0
    checked_out = db.execute('SELECT SUM(total_copies - available_copies) FROM books').fetchone()[0] or 0
    borrowers = db.execute('SELECT COUNT(DISTINCT borrower_name) FROM checkouts WHERE returned = 0').fetchone()[0]

    return render_template('index.html',
                           books=books, categories=categories,
                           search=search, category=category,
                           stats={'total': total, 'available': available,
                                  'checked_out': checked_out, 'borrowers': borrowers})


@app.route('/checkout/<int:book_id>', methods=['POST'])
def checkout(book_id):
    borrower = request.form.get('borrower_name', '').strip()
    if not borrower:
        flash('Please enter a borrower name.', 'error')
        return redirect(url_for('index'))

    db = get_db()
    book = db.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()

    if not book or book['available_copies'] < 1:
        flash('No copies available.', 'error')
        return redirect(url_for('index'))

    db.execute('UPDATE books SET available_copies = available_copies - 1 WHERE id = ?', (book_id,))
    db.execute('INSERT INTO checkouts (book_id, borrower_name, checkout_date) VALUES (?, ?, ?)',
               (book_id, borrower, date.today().isoformat()))
    db.commit()
    flash(f'✅ "{book["title"]}" checked out to {borrower}.', 'success')
    return redirect(url_for('index'))


@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    db = get_db()
    checkout = db.execute(
        'SELECT * FROM checkouts WHERE book_id = ? AND returned = 0 ORDER BY id ASC LIMIT 1',
        (book_id,)
    ).fetchone()

    if not checkout:
        flash('No active checkout found.', 'error')
        return redirect(url_for('index'))

    db.execute('UPDATE checkouts SET returned = 1 WHERE id = ?', (checkout['id'],))
    db.execute('UPDATE books SET available_copies = available_copies + 1 WHERE id = ?', (book_id,))
    db.commit()

    book = db.execute('SELECT title FROM books WHERE id = ?', (book_id,)).fetchone()
    flash(f'↩️ "{book["title"]}" marked as returned.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
