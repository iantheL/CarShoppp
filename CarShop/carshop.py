import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
import os
if not os.path.exists('database'):
       os.makedirs('database')
   

# Database setup
def init_db():
    if not os.path.exists('database'):
        os.makedirs('database')
        
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database', 'carshop.db'))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            hashed_password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# User registration
def register_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect('database/carshop.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

# User login
def login_user(username, password):
    conn = sqlite3.connect('database/carshop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        messagebox.showinfo("Success", "Login successful!")
        # Here you can call the function to show the dashboard
    else:
        messagebox.showerror("Error", "Invalid username or password.")
    conn.close()

# GUI setup
def setup_gui():
    root = Tk()
    root.title("CarShop")

    # Registration
    Label(root, text="Register").grid(row=0, column=0)
    Label(root, text="Username").grid(row=1, column=0)
    username_entry = Entry(root)
    username_entry.grid(row=1, column=1)
    Label(root, text="Password").grid(row=2, column=0)
    password_entry = Entry(root, show='*')
    password_entry.grid(row=2, column=1)
    Button(root, text="Register", command=lambda: register_user(username_entry.get(), password_entry.get())).grid(row=3, column=0, columnspan=2)

    # Login
    Label(root, text="Login").grid(row=4, column=0)
    Label(root, text="Username").grid(row=5, column=0)
    username_entry_login = Entry(root)
    username_entry_login.grid(row=5, column=1)
    Label(root, text="Password").grid(row=6, column=0)
    password_entry_login = Entry(root, show='*')
    password_entry_login.grid(row=6, column=1)
    Button(root, text="Login", command=lambda: login_user(username_entry_login.get(), password_entry_login.get())).grid(row=7, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    init_db()
    setup_gui()
