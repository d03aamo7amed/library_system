# 📚 ReadSpace — Next-Generation Digital Library System

![Django](https://img.shields.io/badge/Backend-Django-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![JavaScript](https://img.shields.io/badge/Frontend-Vanilla%20JS-F7DF1E?style=for-the-badge&logo=javascript)
![Theme](https://img.shields.io/badge/UI%2FUX-Dark%20Glassmorphism-00F2FE?style=for-the-badge)

> **ReadSpace** is an advanced, full-stack library management and discovery platform built with Django. It features a modern Dark Glassmorphism UI, real-time zero-latency search, automated stock control, and robust admin audit trails.

## 🌟 Key Features

* **✨ Modern Dark Glassmorphism UI:** High-retention translucent interface built with custom CSS.
* **⚡ Zero-Latency Search:** Instant client-side JavaScript filtering across titles, authors, and categories without page reloads.
* **📦 Automated Stock Control:** Real-time inventory auto-deduction and restoration with mathematical guardrails preventing negative stock.
* **🛡️ Audit Trail & Security:** Full system logging for admin actions (Admin ID, Loan ID, Timestamp) with protected session routing.
* **⚙️ Smart Dashboard Utilities:** One-click overdue book tracking and bulk operations for batch updating loan statuses.
* **🌱 Developer Utilities:** Custom management command (`seed_books`) for populating test data instantly.

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Django, Python |
| **Frontend** | HTML5, Custom CSS3 (Glassmorphism), Vanilla JavaScript |
| **Database** | SQLite |
| **Authentication** | Django Auth & CSRF Security |


## 🚀 Quick Start & Installation

Follow these simple steps to get **ReadSpace** up and running locally:


### 1. Clone the Repository
```bash
git clone [https://github.com/d03aamo7amed/ReadSpace.git]
(https://github.com/d03aamo7amed/ReadSpace.git)
cd ReadSpace

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install django


python manage.py migrate

# Populate database with initial books data
python manage.py seed_books

# Create admin account for dashboard access
python manage.py createsuperuser

python manage.py runserver
# Open your browser and navigate to http://127.0.0.1:8000/.


## 👥 Team & Module Ownership

| Role | Name / Lead | Key Deliverables |
| :--- | :--- | :--- |
| **Project Lead & QA** | Doaa | Integration, Architecture, Glassmorphic Theme, SRS & README |
| **Backend & Auth** | zainab | Signup, Login, Protected Sessions & Redirects |
| **Models & Admin** | huda ashraf | Book Schemas, Audit Logs, Custom Management Commands (`seed_books`) |
| **Core Logic Engine** | huda & zainab | Borrow/Return Logic, Real-Time Stock Validation, Overdue Filter |
| **Frontend & UI/UX** | ragaa adel | Base Glassmorphic Layouts, "My Shelf" views, CSS Components |
| **Frontend & JS** | mariam mohamed | Client-side Live Search Engine, Form Validations, Dynamic Badges |

---

## 🔑 Demo Credentials

Use these accounts to explore the system during defense or testing:

* **Admin Portal (`/admin`):**
  * **Username:** `admin`
  * **Password:** `@123456#`
* **Demo Member Account:**
  * **Username:** `do3aa`
  * **Password:** `@123456#`

---

## 📄 License & Acknowledgments

Built for academic presentation and defense under Django MVT Architecture. Designed with ❤️ by the **ReadSpace** team.


