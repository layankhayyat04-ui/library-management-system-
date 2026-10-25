<div align="center">

<br/>

# Library Management System

**A full-stack web app for book tracking — browse, search, check out, return**

Replaces spreadsheet-based library tracking with a single, always-up-to-date digital record. Built end-to-end with Python: Flask handles the web server, SQLite stores the data permanently.

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

<br/>

</div>

---

## Overview

The Library Management System is a working web application that replaces manual, spreadsheet-based tracking of a book collection with a single, always-up-to-date digital record.

It keeps track of every book's total and available copies, records who has borrowed what, and lets staff search and filter the collection instantly — instead of scrolling through a spreadsheet.

Nothing is lost when the server restarts: SQLite stores the entire database in one file with no separate server needed.

---

## Features

### 📊 At-a-Glance Dashboard

The home screen opens with four live counters:

- **Total copies** across the whole collection
- **Available now** — how many can be checked out right now
- **Checked out** — currently borrowed
- **Active borrowers** — how many people currently have something

### 🔍 Instant Search

Typing into the search bar filters the book list in real time by **title or author**. Searching "Data" narrows 8 books down to the 2 matching titles — live, as you type.

### 🏷️ Category Filtering

Books are grouped by category. The dropdown filters the whole list to just that group — useful for browsing by subject rather than searching a specific title.

### ✅ Check Out a Book

Every book with at least one available copy shows a "Check Out" action with a borrower name field. Submitting it:

- Immediately reduces that book's available count by one
- Records the checkout with today's date in the database

### ↩️ Return a Book

When a book has zero available copies, its action column swaps to a **"Mark Returned"** button. Clicking it:

- Closes out that book's oldest active checkout record
- Adds one copy back to the available count

### 🎨 Live Status Badges

The catalog uses color-coded availability badges:

| Badge | Meaning |
|---|---|
| 🟢 Green | Well-stocked — several copies available |
| 🟡 Amber | Low copies — only one left |
| 🔴 Red/Teal | Fully checked out — shows Mark Returned |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · Flask |
| Database | SQLite |
| Templating | Jinja2 |
| Frontend | HTML · CSS |

**Why Flask & SQLite?** Flask lets the whole system run as a single small Python app with no external services required. SQLite needs no separate database server — the entire database lives in one file, making setup simple.

---

## What's Next

| Feature | Description |
|---|---|
| Accounts & Login | So only authorized staff can check books in and out |
| Due Dates & Overdue Alerts | Track when a book is due back; flag it visually when late |
| Email Reminders | Automatic notices before a book is due, and when overdue |
| Export to Excel | One-click export of the full catalog or checkout history |

---

## Project Status

This is a **real, working application** — every screenshot in the walkthrough shows the live running system, not a mockup. The core loop (browse, search, check out, return) is fully functional.

---

## About

Built by **Layan Khayyat**
B.Sc. Business Information Technology · Princess Sumaya University for Technology (PSUT)

[Portfolio](https://layankhayyat.com) · [LinkedIn](https://linkedin.com/in/layankhayyat)
