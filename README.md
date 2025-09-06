# RouteMate

**Tagline:** Never Miss a Seat Again!

Routemate is a modern web-based Bus Reservation Management System built with Flask and MySQL. It allows users to book, view, and cancel bus tickets, while admins can manage routes and bookings. The system features user authentication, an About Us section, Feedback and Contact forms (with email support), and a clean, responsive interface.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Use of Data Structures and Algorithms (DSA)](#use-of-data-structures-and-algorithms-dsa)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [About Us](#about-us)
- [Contact](#contact)
- [Feedback](#feedback)

---

## Features

- User registration and login
- Book, view, and cancel tickets
- Admin dashboard: manage buses, view all bookings, add/delete routes
- About Us, Feedback, and Contact Us pages
- Feedback and contact forms send messages via email
- **Modern, responsive UI with dark mode and travel-themed backgrounds**
- **Persistent dark mode toggle (remembers your choice)**
- **Improved dashboard with only functional quick/admin actions**
- **Beautiful hero section with visible travel scenery**
- **Session management and user-friendly navigation**

---

## Tech Stack

- **Frontend:**  
  - HTML5, CSS3 (custom, responsive, dark mode)
  - Jinja2 templating (Flask)
  - JavaScript (for dark mode toggle and UI effects)

- **Backend:**  
  - Python 3.x
  - Flask (web framework)
  - Flask-Mail (email support)
  - Flask-MySQLdb / mysql-connector-python (MySQL integration)

- **Database:**  
  - MySQL

- **Other:**  
  - Bootstrap (optional, for some UI elements)
  - Deployed locally (can be hosted on any server supporting Python/Flask)

---

## Use of Data Structures and Algorithms (DSA)

Routemate applies DSA concepts in several practical ways to ensure efficient and fair bus booking:

- **Queue Data Structure for Fair Booking:**  
  The booking logic uses a queue (`collections.deque`) to simulate real-world ticket queues, ensuring first-come, first-served seat allocation and preventing double-booking.

- **Relational Database as Structured Data Storage:**  
  MySQL tables (users, buses, bookings, stats) are used as persistent data structures, supporting efficient search, filtering, and relational operations.

- **Hash Tables for Session Management:**  
  Flask’s session object (a dictionary/hash table) is used for fast, secure access to user authentication and preferences.

- **Efficient Search and Filtering:**  
  Bus and booking searches are performed using SQL queries, which leverage indexing (similar to binary search) for fast lookups. Filtering by route, date, or user is handled efficiently in both SQL and Python.

- **Sorting and Reporting:**  
  Bookings and routes are displayed in sorted order (by date, time, etc.) using SQL’s `ORDER BY` and Python’s built-in sorting.

- **Algorithmic Logic:**  
  - Calculating journey durations and converting hours to days/hours for user-friendly display.
  - Managing seat availability and updates atomically to prevent race conditions.

- **Form Validation and Data Integrity:**  
  User input is validated and processed using string and list operations to ensure correctness and security.

These DSA applications make Routemate robust, fair, and scalable for both users and administrators.

---

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/routemate.git
   cd routemate
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up your MySQL database** (see `app.py` for schema or use the provided SQL script).
4. **Configure your email and database credentials** in `app.py`.
5. **Run the app:**
   ```sh
   python app.py
   ```
6. **Open your browser at** [http://localhost:5000](http://localhost:5000)

---

## Project Structure

```
routemate/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── /templates/             # HTML (Jinja2) templates
│   ├── home.html
│   ├── dashboard.html
│   └── ... (other pages)
├── /static/                # Static files (CSS, images, JS)
│   ├── style.css
│   ├── logo.png
│   └── home_bg.png
└── ... (other files)
```

---

## About Us

Routemate is developed by **Arpita Mishra**. Our mission is to make bus travel easy and reliable for everyone.

---

## Contact

- Developer: Arpita Mishra
- Email: arpitamishra2755@gmail.com

---

## Feedback

We value your feedback! Use the Feedback page on the website to send us your thoughts and suggestions.

--- 
