<div align="center">

<a href="./showcase.html">
<img src="https://img.shields.io/badge/%E2%9C%A8%20Live%20Showcase-2563EB?style=for-the-badge&logoColor=white" height="36"/>
</a>

</div>

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=slice&color=0:1D4ED8,40:2563EB,80:0891B2,100:06B6D4&height=250&section=header&text=Library%20System&fontSize=72&fontColor=fff&fontAlignY=50&desc=Python%20%E2%80%A2%20Flask%20%E2%80%A2%20SQLite%20%E2%80%A2%20Jinja2&descSize=20&descAlignY=72&descFontColor=BAE6FD&animation=blinking&reversal=true" width="100%"/>

</div>

<br/>

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=22&pause=1000&color=2563EB&center=true&vCenter=true&width=620&lines=A+full+book+catalog+in+60+seconds+flat.;Search.+Check+out.+Return.+No+spreadsheet.;One+Python+file.+One+command.+Done." alt="typing"/>
</div>

<br/>

<div align="center">

<img src="https://skillicons.dev/icons?i=python,flask,sqlite&theme=dark" height="50"/>

&nbsp;&nbsp;&nbsp;

<img src="https://img.shields.io/badge/Jinja2-B41717?style=flat-square&logo=jinja&logoColor=white"/>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white"/>

<br/><br/>

<img src="https://img.shields.io/badge/Setup-60%20seconds-22C55E?style=for-the-badge"/>
&nbsp;
<img src="https://img.shields.io/badge/Database-Auto--seeded-2563EB?style=for-the-badge"/>
&nbsp;
<img src="https://img.shields.io/badge/Status-Complete-059669?style=for-the-badge"/>

</div>

---

<br/>

<table>
<tr>
<td width="55%">

### 💡 What & Why

Spreadsheet-based book tracking breaks down fast — no live counts, no search, no checkout history.

This replaces it with a proper web app that runs anywhere with one command. No cloud, no config.

**`python app.py` → open browser → done.**

</td>
<td width="45%">

### 📊 Live Dashboard Stats

```
📦  Total Books     ─── every title in catalog
✅  Available       ─── copies ready now  
📤  Checked Out     ─── copies with borrowers
👤  Active Borrowers ── people with open loans
```
*Recalculates on every request. Always accurate.*

</td>
</tr>
</table>

<br/>

---

## 🏗️ Project Structure

```
library-management-system/
├── app.py               # Flask app — all routes, DB logic, seed data
├── requirements.txt     # flask>=3.0.0
├── library.db           # SQLite — auto-created & seeded on first run
├── templates/
│   └── index.html       # Jinja2 — full UI, single page
└── static/
    └── css/style.css    # Design tokens · badges · responsive grid
```

<br/>

---

## ⚡ Feature Breakdown

<details>
<summary><b>🔍 Search & Filter — stacked SQL filters</b></summary>

<br/>

Full-text search across title and author (case-insensitive `LIKE`), plus category dropdown filter. Both stack — search `"Data"` in `"Technology"` narrows precisely. Clears with one click, no reload.

```python
query  = 'SELECT * FROM books WHERE 1=1'
params = []

if search:
    query  += ' AND (LOWER(title) LIKE ? OR LOWER(author) LIKE ?)'
    params += [f'%{search.lower()}%', f'%{search.lower()}%']

if category:
    query  += ' AND category = ?'
    params.append(category)
```

</details>

<details>
<summary><b>📖 Checkout — atomic update + record insert</b></summary>

<br/>

On submit: `available_copies` decremented, checkout record inserted with today's date. Borrower name required. Validation on both. Flash message on success.

```python
@app.route('/checkout/<int:book_id>', methods=['POST'])
def checkout(book_id):
    borrower = request.form.get('borrower_name', '').strip()
    if not borrower:
        flash('Borrower name is required.', 'error')
        return redirect(url_for('index'))

    db = get_db()
    db.execute('UPDATE books SET available_copies = available_copies - 1 WHERE id = ?', (book_id,))
    db.execute('INSERT INTO checkouts (book_id, borrower_name, checkout_date) VALUES (?, ?, ?)',
               (book_id, borrower, date.today().isoformat()))
    db.commit()
```

</details>

<details>
<summary><b>↩️ Return — closes oldest open checkout</b></summary>

<br/>

No manual record hunting. Finds the oldest unreturned checkout for that book and closes it atomically.

```python
@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    db  = get_db()
    row = db.execute(
        'SELECT id FROM checkouts WHERE book_id = ? AND returned = 0 ORDER BY checkout_date ASC LIMIT 1',
        (book_id,)
    ).fetchone()
    if row:
        db.execute('UPDATE checkouts SET returned = 1 WHERE id = ?', (row['id'],))
        db.execute('UPDATE books SET available_copies = available_copies + 1 WHERE id = ?', (book_id,))
        db.commit()
```

</details>

<details>
<summary><b>🎨 Color-coded availability badges</b></summary>

<br/>

| Badge | Condition | Color |
|:------|:----------|:------|
| `3 / 3 available` | Full stock | 🟢 Green |
| `1 / 3 left` | Low stock | 🟡 Amber |
| `Out of stock` | Zero copies | 🔴 Red |

</details>

<br/>

---

## 🗄️ Database Schema

```sql
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
```

*Auto-created and seeded with 8 books (Clean Code, Atomic Habits, Designing Data-Intensive Applications…) on first launch.*

<br/>

---

## 🎨 Design Tokens

<div align="center">

| Token | Hex | Role |
|:------|:----|:-----|
| `primary` | ![#2563EB](https://placehold.co/14x14/2563EB/2563EB.png) `#2563EB` | Actions · links · stat tiles |
| `success` | ![#059669](https://placehold.co/14x14/059669/059669.png) `#059669` | Available badge · flash success |
| `warning` | ![#D97706](https://placehold.co/14x14/D97706/D97706.png) `#D97706` | Low-stock badge |
| `danger` | ![#DC2626](https://placehold.co/14x14/DC2626/DC2626.png) `#DC2626` | Out-of-stock badge · flash error |

</div>

<br/>

---

## 🚀 Run It

```bash
git clone https://github.com/layankhayyat04-ui/library-management-system-.git
cd library-management-system-
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** — database seeds itself on first launch.

<br/>

---

## 🗺️ Roadmap

| Feature | Description |
|:--------|:------------|
| Auth & Roles | Staff-only access with Flask-Login |
| Due Dates | Track return deadlines, flag overdue |
| Email Reminders | Auto-notify borrowers before due date |
| REST API | JSON endpoints for frontend/mobile integration |
| Export to Excel | One-click catalog + checkout history |

<br/>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:06B6D4,50:0891B2,100:2563EB&height=120&section=footer&text=Built%20by%20Layan%20Khayyat&fontSize=22&fontColor=fff&fontAlignY=70&animation=twinkling" width="100%"/>

<br/>

[![Portfolio](https://img.shields.io/badge/%F0%9F%8C%90%20layankhayyat.com-2563EB?style=for-the-badge)](https://layankhayyat.com)
&nbsp;
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/layankhayyat)

</div>
