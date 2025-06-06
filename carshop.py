import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import bcrypt
from datetime import datetime

DB_PATH = 'carshop.db'

# Colors (Maroon and Light Blue Theme)
COLOR_BG = '#800000'       # Maroon background
COLOR_FG = '#FFFFFF'       # White text
COLOR_BTN_BG = '#ADD8E6'   # Light Blue buttons
COLOR_BTN_FG = '#000000'   # Black text on buttons
COLOR_ENTRY_BG = '#FFC0CB' # Light pink for entry background as accent

# Database helper functions
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer'
        )
    ''')
    # Cars Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            price REAL NOT NULL,
            available INTEGER NOT NULL DEFAULT 1,
            preorder_allowed INTEGER NOT NULL DEFAULT 1
        )
    ''')
    # Orders Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            car_id INTEGER NOT NULL,
            order_type TEXT NOT NULL, -- "buy" or "preorder"
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(car_id) REFERENCES cars(id)
        )
    ''')
    # Messages Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()

    # Insert default cars if empty
    c.execute('SELECT COUNT(*) FROM cars')
    if c.fetchone()[0] == 0:
        default_cars = [
            ('Toyota Camry', 24000, 1, 1),
            ('Honda Accord', 26000, 1, 1),
            ('Tesla Model 3', 35000, 0, 1),  # unavailable but preorder allowed
            ('Ford Mustang', 30000, 1, 0),   # no preorder allowed
            ('BMW 3 Series', 40000, 1, 1),
        ]
        c.executemany('INSERT INTO cars (model, price, available, preorder_allowed) VALUES (?, ?, ?, ?)', default_cars)
        conn.commit()

    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

class CarShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CarShop")
        self.root.geometry("700x500")
        self.root.configure(bg=COLOR_BG)
        self.conn = sqlite3.connect(DB_PATH)
        self.user_id = None
        self.username = None

        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg=COLOR_BG)
        frame.pack(expand=True)

        title = tk.Label(frame, text="CarShop Login", font=('Helvetica', 24, 'bold'), fg=COLOR_FG, bg=COLOR_BG)
        title.grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(frame, text="Username:", fg=COLOR_FG, bg=COLOR_BG, font=('Helvetica', 12)).grid(row=1, column=0, sticky='e', pady=5)
        self.entry_username = tk.Entry(frame, font=('Helvetica', 12), bg=COLOR_ENTRY_BG)
        self.entry_username.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Password:", fg=COLOR_FG, bg=COLOR_BG, font=('Helvetica', 12)).grid(row=2, column=0, sticky='e', pady=5)
        self.entry_password = tk.Entry(frame, font=('Helvetica', 12), bg=COLOR_ENTRY_BG, show='*')
        self.entry_password.grid(row=2, column=1, pady=5)

        login_btn = tk.Button(frame, text="Login", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12, 'bold'), command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')

        register_btn = tk.Button(frame, text="Register", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12), command=self.create_register_screen)
        register_btn.grid(row=4, column=0, columnspan=2, pady=5, sticky='ew')

    def create_register_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg=COLOR_BG)
        frame.pack(expand=True)

        title = tk.Label(frame, text="CarShop Register", font=('Helvetica', 24, 'bold'), fg=COLOR_FG, bg=COLOR_BG)
        title.grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(frame, text="Username:", fg=COLOR_FG, bg=COLOR_BG, font=('Helvetica', 12)).grid(row=1, column=0, sticky='e', pady=5)
        self.entry_reg_username = tk.Entry(frame, font=('Helvetica', 12), bg=COLOR_ENTRY_BG)
        self.entry_reg_username.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Password:", fg=COLOR_FG, bg=COLOR_BG, font=('Helvetica', 12)).grid(row=2, column=0, sticky='e', pady=5)
        self.entry_reg_password = tk.Entry(frame, font=('Helvetica', 12), bg=COLOR_ENTRY_BG, show='*')
        self.entry_reg_password.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Confirm Password:", fg=COLOR_FG, bg=COLOR_BG, font=('Helvetica', 12)).grid(row=3, column=0, sticky='e', pady=5)
        self.entry_reg_confirm = tk.Entry(frame, font=('Helvetica', 12), bg=COLOR_ENTRY_BG, show='*')
        self.entry_reg_confirm.grid(row=3, column=1, pady=5)

        register_btn = tk.Button(frame, text="Register", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12, 'bold'), command=self.register)
        register_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')

        back_btn = tk.Button(frame, text="Back to Login", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12), command=self.create_login_screen)
        back_btn.grid(row=5, column=0, columnspan=2, pady=5, sticky='ew')

        self.var_checkbox = tk.IntVar()

        self.is_admin_cbox = tk.Checkbutton(frame, text="Register as admin", bg=COLOR_BTN_BG, fg=COLOR_FG, var=self.var_checkbox, onvalue=1, offvalue=0 )
        self.is_admin_cbox.grid(row=6, column=0, columnspan=2, pady=5, sticky='ew')

        self.is_admin_cbox.config(bg="lightgrey", fg="blue", font=("Arial", 12),
                           selectcolor="green", relief="raised", padx=10, pady=5)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter username and password.")
            return
        c = self.conn.cursor()
        c.execute("SELECT id, password, role FROM users WHERE username=?", (username,))
        row = c.fetchone()
        if row and verify_password(password, row[1]):
            self.user_id = row[0]
            self.username = username
            self.user_role = row[2]
            self.create_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.entry_reg_username.get().strip()
        password = self.entry_reg_password.get()
        confirm = self.entry_reg_confirm.get()
        role = "customer"
        if not username or not password or not confirm:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return
        if password != confirm:
            messagebox.showwarning("Input Error", "Passwords do not match.")
            return
        if self.var_checkbox.get() == 1:
            role = 'admin'
        c = self.conn.cursor()
        try:
            hashed_pw = hash_password(password)
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_pw, role))
            self.conn.commit()
            messagebox.showinfo("Success", "Registered successfully! You can now login.")
            self.create_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

    def create_dashboard(self):
        self.clear_screen()
        top_frame = tk.Frame(self.root, bg=COLOR_BG)
        top_frame.pack(fill='x', pady=10)
        welcome_label = tk.Label(top_frame, text=f"Welcome, {self.username}!", font=('Helvetica', 18, 'bold'), fg=COLOR_FG, bg=COLOR_BG)
        welcome_label.pack(side='left', padx=20)

        logout_btn = tk.Button(top_frame, text="Logout", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12), command=self.logout)
        logout_btn.pack(side='right', padx=20)

        contact_btn = tk.Button(top_frame, text="Contact Us", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12), command=self.create_contact_screen)
        contact_btn.pack(side='right', padx=20)

        if self.user_role == "admin":
            messages_btn = tk.Button(top_frame, text="Messages", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12), command=self.view_messages)
            messages_btn.pack(side='right', padx=20)

        # Cars List
        self.car_list_frame = tk.Frame(self.root, bg=COLOR_BG)
        self.car_list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.load_cars()

    def view_messages(self):
        messages_window = tk.Toplevel(self.root)
        messages_window.title("Messages")
        messages_window.geometry("1280x720")

        top_frame = tk.Frame(messages_window, bg=COLOR_BG)
        top_frame.pack(fill='x', pady=10)

        welcome_label = tk.Label(top_frame, text="Messages", font=('Helvetica', 18, 'bold'),
                                 fg=COLOR_FG, bg=COLOR_BG)
        welcome_label.pack(side='left', padx=20)

        table_columns = ("ID", "Username", "Message")

        message_list = ttk.Treeview(messages_window, show="headings", columns=table_columns)

        for column in table_columns:
            message_list.heading(column, text=column)

            if column == "ID":
                message_list.column(column, width=40)
            elif column == "Username":
                message_list.column(column, width=120)

        message_list.pack(fill='both', expand=True, padx=20, pady=10)

        def get_messages():
            try:
                c = self.conn.cursor()
                c.execute("SELECT * FROM messages")
                messages_data = c.fetchall()

                if not messages_data:
                    return

                for messages in messages_data:
                    c.execute('SELECT username FROM users WHERE id=?', (messages[1],))
                    username = c.fetchone()[0]

                    message_list.insert("", "end", values=(messages[0], username, messages[2]))
            except Exception as e:
                print(e)
                return

        get_messages()
        messages_window.mainloop()


    def load_cars(self):
        for widget in self.car_list_frame.winfo_children():
            widget.destroy()

        c = self.conn.cursor()
        c.execute("SELECT id, model, price, available, preorder_allowed FROM cars")
        cars = c.fetchall()

        if not cars:
            no_cars_label = tk.Label(self.car_list_frame, text="No cars available.", fg=COLOR_FG, bg=COLOR_BG, font=('Helvetica', 14))
            no_cars_label.pack(pady=20)
            return

        for car in cars:
            car_id, model, price, available, preorder_allowed = car
            car_frame = tk.Frame(self.car_list_frame, bg='#330000', bd=2, relief='groove')
            car_frame.pack(fill='x', pady=6)

            car_info = tk.Label(car_frame, text=f"{model} - ${price:,.2f}", fg=COLOR_BTN_BG, bg='#330000', font=('Helvetica', 14, 'bold'))
            car_info.pack(side='left', padx=10, pady=10)

            btn_frame = tk.Frame(car_frame, bg='#330000')
            btn_frame.pack(side='right', padx=10)

            if available:
                buy_btn = tk.Button(btn_frame, text="Buy", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12, 'bold'),
                                    command=lambda c_id=car_id: self.place_order(c_id, 'buy'))
                buy_btn.pack(side='left', padx=5)
            else:
                # Show buy disabled if not available
                buy_btn = tk.Button(btn_frame, text="Buy", bg='grey', fg='white', font=('Helvetica', 12, 'bold'), state='disabled')
                buy_btn.pack(side='left', padx=5)

            if preorder_allowed:
                preorder_btn = tk.Button(btn_frame, text="Preorder", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12, 'bold'),
                                         command=lambda c_id=car_id: self.place_order(c_id, 'preorder'))
                preorder_btn.pack(side='left', padx=5)
            else:
                preorder_btn = tk.Button(btn_frame, text="Preorder", bg='grey', fg='white', font=('Helvetica', 12, 'bold'), state='disabled')
                preorder_btn.pack(side='left', padx=5)

    def place_order(self, car_id, order_type):
        c = self.conn.cursor()
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO orders (user_id, car_id, order_type, date) VALUES (?, ?, ?, ?)", (self.user_id, car_id, order_type, date_str))
        self.conn.commit()
        messagebox.showinfo("Success", f"Your {order_type} order has been placed successfully!")

    def create_contact_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.root, bg=COLOR_BG)
        frame.pack(expand=True, fill='both', padx=30, pady=30)

        title = tk.Label(frame, text="Contact Us", font=('Helvetica', 24, 'bold'), fg=COLOR_FG, bg=COLOR_BG)
        title.pack(pady=10)

        tk.Label(frame, text="Send us a message below:", fg=COLOR_FG, bg=COLOR_BG, font=('Helvetica', 14)).pack(anchor='w')

        self.text_message = tk.Text(frame, font=('Helvetica', 14), height=8, bg=COLOR_ENTRY_BG, fg='black')
        self.text_message.pack(fill='both', pady=10)

        send_btn = tk.Button(frame, text="Send Message", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 14, 'bold'),
                             command=self.send_message)
        send_btn.pack(pady=10)

        back_btn = tk.Button(frame, text="Back to Dashboard", bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, font=('Helvetica', 12),
                             command=self.create_dashboard)
        back_btn.pack(pady=5)

    def send_message(self):
        message = self.text_message.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Input Error", "Please enter a message before sending.")
            return
        c = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO messages (user_id, message, timestamp) VALUES (?, ?, ?)", (self.user_id, message, timestamp))
        self.conn.commit()
        messagebox.showinfo("Thank you", "Your message has been sent successfully!")
        self.create_dashboard()

    def logout(self):
        self.user_id = None
        self.username = None
        self.create_login_screen()

    def on_close(self):
        self.conn.close()
        self.root.destroy()

if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = CarShopApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
