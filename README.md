<div align="center">

<img src="https://capsule-render.vercel.app/api?type=cylinder&color=0:1D4ED8,50:2563EB,100:0891B2&height=180&section=header&text=Library%20Management%20System&fontSize=38&fontColor=ffffff&fontAlignY=45&animation=blinking" width="100%"/>

<br/>

<a href="#">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=2563EB&center=true&vCenter=true&width=650&lines=Flask+%2B+SQLite+%2B+Jinja2;Browse.+Search.+Check+Out.+Return.;One+file.+One+command.+Fully+working." alt="Typing SVG"/>
</a>

<br/><br/>

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
</p>

<p>
  <img src="https://img.shields.io/badge/Setup-60_seconds-22C55E?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Database-Auto--seeded-2563EB?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/Status-Complete-059669?style=flat-square"/>
  &nbsp;
  <img src="https://img.shields.io/badge/License-MIT-0891B2?style=flat-square"/>
</p>

</div>

---

<div align="center">

## `< The Idea />`

</div>

> Spreadsheet-based book tracking breaks down fast — no live counts, no search, no checkout history. This replaces it with a proper web app: one Python file, one SQLite database, run it anywhere. No cloud, no config, no fuss.

<br/>

---

## 📊 Live Dashboard

<div align="center">

| 📦 Total Books | ✅ Available | 📤 Checked Out | 👤 Active Borrowers |
|:---:|:---:|:---:|:---:|
| Every title in catalog | Copies ready now | Copies with borrowers | People with open loans |

*All four counters recalculate on every request — always accurate, zero caching.*

</div>

---

## ⚡ Feature Breakdown

<details>
<summary><strong>🔍 Search & Filter</strong></summary>

<br/>

- **Full-text search** across title and author (case-insensitive `LIKE`)
- **Category dropdown** — filter to a single subject group
- Both filters stack — search "Data" in "Technology" narrows precisely
- Clears with one click — no page reload

</details>

<details>
<summary><strong>📖 Check Out a Book</strong></summary>

<br/>

- Any book with available copies shows a borrower name field
- On submit: `available_copies` decremented, checkout record inserted with today's date
- Validation: borrower name required, copy must exist
- Flash message confirms success

</details>

<details>
<summary><strong>↩️ Mark Returned</strong></summary>

<br/>

- Fully checked-out books show **Mark Returned** instead
- Closes the oldest open checkout for that book
- Increments `available_copies` atomically
- No manual record hunting required

</details>

<details>
<summary><strong>🎨 Color-Coded Availability Badges</strong></summary>

<br/>

| Badge | Condition | Color |
|:---|:---|:---|
| `3 / 3 available` | Multiple copies free | 🟢 Green |
| `1 / 3 left` | Only one copy left | 🟡 Amber |
| `Out of stock` | Zero copies available | 🔴 Red |

</details>

---

## 🏗️ Architecture

```
library-management-system/
├── app.py                # Flask app — all routes, DB logic, seed data
├── requirements.txt      # flask>=3.0.0
├── library.db            # SQLite — auto-created & seeded on first run
├── templates/
│   └── index.html        # Jinja2 template — full UI, one page
└── static/
    └── css/
        └── style.css     # Design tokens, badges, responsive grid
```

---

## 🧩 Key Code

### Database Schema + Auto-Seed

```python
def init_db():
    with get_db() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS books (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                title            TEXT    NOT NULL,
                author           TEXT    NOT NULL,
                category         TEXT    NOT NULL,
                total_copies     INTEGER NOT NULL DEFAULT 1,
                available_copies INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS checkouts (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id       INTEGER NOT NULL,
                borrower_name TEXT    NOT NULL,
                checkout_date TEXT    NOT NULL,
                returned      INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (book_id) REFERENCES books(id)
            );
        ''')
        # Seeds 8 books on first launch — Clean Code, Atomic Habits,
        # Designing Data-Intensive Applications, Deep Work, and more
```

### Dynamic Search — Stacked SQL Filters

```python
@app.route('/')
def index():
    search   = request.args.get('search',   '').strip()
    category = request.args.get('category', '').strip()

    query  = 'SELECT * FROM books WHERE 1=1'
    params = []

    if search:
        query += ' AND (LOWER(title) LIKE ? OR LOWER(author) LIKE ?)'
        params += [f'%{search.lower()}%', f'%{search.lower()}%']

    if category:
        query += ' AND category = ?'
        params.append(category)

    books = db.execute(query, params).fetchall()
```

### Checkout — Atomic Update + Record Insert

```python
@app.route('/checkout/<int:book_id>', methods=['POST'])
def checkout(book_id):
    borrower = request.form.get('borrower_name', '').strip()
    if not borrower:
        flash('Borrower name is required.', 'error')
        return redirect(url_for('index'))

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
    flash(f'"{book_id}" checked out to {borrower}.', 'success')
    return redirect(url_for('index'))
```

### Return — Close Oldest Open Checkout

```python
@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    db = get_db()
    checkout = db.execute(
        '''SELECT id FROM checkouts
           WHERE book_id = ? AND returned = 0
           ORDER BY checkout_date ASC LIMIT 1''',
        (book_id,)
    ).fetchone()

    if checkout:
        db.execute('UPDATE checkouts SET returned = 1 WHERE id = ?',
                   (checkout['id'],))
        db.execute(
            'UPDATE books SET available_copies = available_copies + 1 WHERE id = ?',
            (book_id,)
        )
        db.commit()
    return redirect(url_for('index'))
```

---

## 🎨 Design Tokens

<div align="center">

| Token | Value | Role |
|:---|:---|:---|
| `--primary` | `#2563EB` | Actions, links, stats |
| `--success` | `#059669` | Available badge, flash success |
| `--warning` | `#D97706` | Low-stock badge |
| `--danger` | `#DC2626` | Out-of-stock badge, flash error |
| `--surface` | `#F8FAFC` | Page background |
| `--card` | `#FFFFFF` | Card & table background |

</div>

---

## 🚀 Run It

```bash
git clone https://github.com/layankhayyat04-ui/library-management-system-.git
cd library-management-system-

pip install -r requirements.txt
python app.py
```

Open **[http://localhost:5000](http://localhost:5000)** — database seeds itself on first launch.

---

## 🗺️ What's Next

| Feature | Description |
|:---|:---|
| Auth & Roles | Staff-only access with Flask-Login |
| Due Dates | Track return deadlines, flag overdue |
| Email Reminders | Auto-notify borrowers before due date |
| REST API | JSON endpoints for mobile/frontend integration |
| Export to Excel | One-click catalog + checkout history |

---

<div align="center">

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0891B2,100:2563EB&height=120&section=footer&text=Built%20by%20Layan%20Khayyat&fontSize=20&fontColor=ffffff&fontAlignY=65&animation=twinkling" width="100%"/>

<br/>

[![Portfolio](https://img.shields.io/badge/Portfolio-layankhayyat.com-2563EB?style=for-the-badge&logo=vercel&logoColor=white)](https://layankhayyat.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/layankhayyat)

</div>
