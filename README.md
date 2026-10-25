<div align="center">

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=2563EB&height=200&section=header&text=Library%20Management%20System&fontSize=36&fontColor=ffffff&fontAlignY=38&desc=Flask%20%2B%20SQLite%20Web%20Application&descAlignY=58&descSize=18&animation=fadeIn" width="100%"/>

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Complete-059669?style=for-the-badge"/>
</p>

<p align="center">
  <strong>Browse · Search · Check Out · Return</strong><br/>
  Replaces spreadsheet-based library tracking with one always-up-to-date web app.
</p>

<br/>

</div>

---

## ✨ Overview

A working full-stack web application that replaces manual, spreadsheet-based book tracking with a single digital record — browsable in any browser, with no extra services or databases to set up.

```
One Python file. One SQLite file. Run and go.
```

Everything persists across restarts. No setup beyond `pip install flask && python app.py`.

---

## 🖥️ Features

### 📊 Live Dashboard — 4 counters, always current

| Counter | What it shows |
|---|---|
| Total Books | Every book in the catalog |
| Available | Copies that can be checked out right now |
| Checked Out | Copies currently with borrowers |
| Active Borrowers | People who have at least one book |

### 🔍 Instant Search

Filters the catalog in real time by **title or author** as you type. Searching `"Data"` narrows 8 books to the 2 matching titles — no page reload.

### 🏷️ Category Dropdown

Filter the full catalog by subject group — useful when browsing a collection rather than searching for a specific title.

### ✅ Check Out a Book

Any book with available copies shows a borrower name field + **Check Out** button. On submit:
- Available count decreases by 1
- Checkout is recorded in the database with today's date

### ↩️ Mark Returned

When a book has 0 available copies, its action column shows **Mark Returned**. On click:
- The oldest open checkout record is closed
- Available count increases by 1

### 🎨 Color-Coded Status Badges

| Badge | Meaning |
|---|---|
| 🟢 Green | Several copies available |
| 🟡 Amber | Only 1 copy left |
| 🔴 Red | Fully checked out |

---

## 🚀 Getting Started

```bash
# Clone
git clone https://github.com/layankhayyat04-ui/library-management-system-.git
cd library-management-system-

# Install
pip install -r requirements.txt

# Run
python app.py
```

Open [http://localhost:5000](http://localhost:5000) — the database seeds itself on first launch with 8 sample books.

---

## 🧩 Key Code

### Database Initialization with Seed Data

```python
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
```

### Live Search with Dynamic SQL

```python
@app.route('/')
def index():
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
```

### Check Out a Book (atomic update)

```python
@app.route('/checkout/<int:book_id>', methods=['POST'])
def checkout(book_id):
    db = get_db()
    db.execute(
        'UPDATE books SET available_copies = available_copies - 1 WHERE id = ?',
        (book_id,)
    )
    db.execute(
        'INSERT INTO checkouts (book_id, borrower_name, checkout_date) VALUES (?, ?, ?)',
        (book_id, borrower, date.today().isoformat())
    )
    db.commit()
```

---

## 🗂️ Project Structure

```
library-management-system/
├── app.py                # Flask app — routes, DB logic, seed data
├── requirements.txt      # flask>=3.0.0
├── library.db            # SQLite — auto-created on first run
├── templates/
│   └── index.html        # Jinja2 template — full UI
└── static/
    └── css/
        └── style.css     # Responsive styles, badge system
```

---

## 🗺️ What's Next

| Feature | Description |
|---|---|
| Accounts & Login | Staff-only access with Flask-Login |
| Due Dates & Overdue Alerts | Track return deadlines, flag late books |
| Email Reminders | Auto-notify borrowers before due date |
| Export to Excel | One-click catalog + checkout history |
| REST API | JSON endpoints for mobile/frontend integration |

---

<div align="center">

<br/>

**Built by [Layan Khayyat](https://layankhayyat.com)**<br/>
B.Sc. Business Information Technology · Princess Sumaya University for Technology (PSUT)

<br/>

[![Portfolio](https://img.shields.io/badge/Portfolio-layankhayyat.com-2563EB?style=for-the-badge&logo=vercel&logoColor=white)](https://layankhayyat.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/layankhayyat)

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0891B2&height=100&section=footer" width="100%"/>

</div>
