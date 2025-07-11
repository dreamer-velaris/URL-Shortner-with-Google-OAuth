# 🔗 URL Shortener with Google OAuth

A simple and secure URL shortening service built using **Flask**, with **Google OAuth** for authentication.

Users can:
- Sign in with their Google account
- Create custom or auto-generated short links
- Set expiration dates for links
- View link statistics (click count, creation/expiry date)
- Manage all links from a personal dashboard

---

## 🚀 Features

- ✅ Google Login (OAuth 2.0)
- ✅ Custom alias support (e.g., `/my-link`)
- ✅ Expiry dates for links
- ✅ Link analytics (click tracking)
- ✅ User dashboard to view/manage links
- ✅ Delete links
- ✅ Session logout on app restart

---

## 🖥️ Tech Stack

- **Python (Flask)**
- **SQLite** – lightweight backend database
- **Fla** – handles Google OAuth
- **Jinja2** – for templating
- Hosted and tested using **Replit**

---

## 📸 Screenshots


---

## 🚀 Setup Instructions

### 1. Clone the Repository

If you're running this locally:


git clone https://github.com/dreamer-velaris/URL-Shortner-with-Google-OAuth.git
cd URL-Shortner-with-Google-OAuth
Or fork it on GitHub and open in Replit directly.

### 2. Install Dependencies
If you're using Replit, it should auto-install based on requirements.txt.

If running locally:

bash
Copy
Edit
pip install -r requirements.txt
### 3. Set Up the Database
bash
Copy
Edit
python
>>> from models import db
>>> from main import app
>>> with app.app_context():
...     db.create_all()
... 
>>> exit()
This creates the necessary User and Url tables in the SQLite database.

### 4. Google OAuth Setup
To use Google OAuth:

Visit https://console.cloud.google.com/

Create a project → APIs & Services → Credentials

Create OAuth client ID for a Web Application

Authorized redirect URI:

php-template
Copy
Edit
https://<your-repl-username>.<your-repl-name>.repl.co/login/google/authorized
Copy the Client ID and Client Secret into main.py:

python
Copy
Edit
google_bp = make_google_blueprint(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    ...
)
### 5. Run the App
If you're on Replit: it runs automatically when you hit "Run".

Locally:

bash
Copy
Edit
python main.py
### 📌 Features
🔐 Google OAuth + optional signup/login

🔗 URL shortening with optional custom alias + expiry

📊 Link stats + CSV/JSON export

📋 Dashboard to view and manage your links

🗑️ Delete link with confirmation

✅ Session logout on app stop

🎨 Clean and minimal frontend using HTML (CSS optional)
