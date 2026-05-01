import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),  '..'))
from database.database import initialize_database, insert_user, get_all_users, get_user_by_id, update_balance, log_transaction, get_transactions, close_connection

DB_file = "banking.db"
conn = initialize_database(DB_file)

def refresh_user_list():
    user_listbox.delete(0, tk.END)
    for user in get_all_users(conn):
        user_listbox.insert(tk.END, f"[{user[0]}] {user[1]} — ${user[4]:.2f}")

def get_id():
    selection = user_listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select a user first")
        return None
    text = user_listbox.get(selection[0])
    return int(text.split("]")[0][1:])

def create_account():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    email = entry_email.get().strip()
    balance = entry_init_balance.get().strip()
    if not name or not email:
        messagebox.showerror("Error", "Name and email are required")
        return
    insert_user(conn, name, int(age) if age else 0, email, float(balance) if balance else 0.0)
    messagebox.showinfo("Success", f"Account created for {name}")
    refresh_user_list()

def deposit():
    user_id = get_id()
    if user_id is None:
        return
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount")
        return
    except Exception as e:
        messagebox.showerror(f"An unexpected error has occurred: {e}")
        return
    user = get_user_by_id(conn, user_id)
    new_balance = user[4] + amount
    update_balance(conn, user_id, new_balance)
    log_transaction(conn, user_id, amount, "deposit")
    messagebox.showinfo("Deposit", f"Deposited ${amount:.2f}. New balance: ${new_balance:.2f}")
    refresh_user_list()

def withdraw():
    user_id = get_id()
    if user_id is None:
        return
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount")
        return
    except Exception as e:
        messagebox.showerror(f"An unexpected error has occurred: {e}")
        return
    user = get_user_by_id(conn, user_id)
    if amount > user[4]:
        messagebox.showerror("Error", "Insufficient balance")
        return
    new_balance = user[4] - amount
    update_balance(conn, user_id, new_balance)
    log_transaction(conn, user_id, amount, "withdrawal")
    messagebox.showinfo("Withdrawal", f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")
    refresh_user_list()

def view_transactions():
    user_id = get_id()
    if user_id is None:
        return
    transactions = get_transactions(conn, user_id)
    transaction_listbox.delete(0, tk.END)
    if not transactions:
        transaction_listbox.insert(tk.END, "No transactions found")
    for t in transactions:
        transaction_listbox.insert(tk.END, f"{t[5][:10]} | {t[2]:10} | ${t[3]:.2f} | {t[4]}")

def on_close():
    close_connection(conn)
    root.destroy()
root = tk.Tk()
root.title("Neo Banking App")
root.geometry("650x550")
frame_create = tk.LabelFrame(root, text="Create Account", padx=10, pady=10)
frame_create.pack(fill="x", padx=10, pady=5)

tk.Label(frame_create, text="Name:").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(frame_create)
entry_name.grid(row=0, column=1)
tk.Label(frame_create, text="Age:").grid(row=0, column=2, sticky="w")
entry_age = tk.Entry(frame_create, width=5)
entry_age.grid(row=0, column=3)
tk.Label(frame_create, text="Email:").grid(row=1, column=0, sticky="w")
entry_email = tk.Entry(frame_create, width=25)
entry_email.grid(row=1, column=1)
tk.Label(frame_create, text="Initial Balance:").grid(row=1, column=2, sticky="w")
entry_init_balance = tk.Entry(frame_create, width=10)
entry_init_balance.grid(row=1, column=3)
tk.Button(frame_create, text="Create Account", command=create_account).grid(row=2, column=0, columnspan=4, pady=5)

frame_users = tk.LabelFrame(root, text="Users", padx=10, pady=5)
frame_users.pack(fill="x", padx=10, pady=5)
user_listbox = tk.Listbox(frame_users, height=5, width=70)
user_listbox.pack()
tk.Button(frame_users, text="Refresh List", command=refresh_user_list).pack(pady=3)

frame_actions = tk.LabelFrame(root, text="Deposit / Withdraw", padx=10, pady=5)
frame_actions.pack(fill="x", padx=10, pady=5)
tk.Label(frame_actions, text="Amount: $").pack(side="left")
entry_amount = tk.Entry(frame_actions, width=10)
entry_amount.pack(side="left")
tk.Button(frame_actions, text="Deposit", command=deposit).pack(side="left", padx=5)
tk.Button(frame_actions, text="Withdraw", command=withdraw).pack(side="left", padx=5)
tk.Button(frame_actions, text="View Transactions", command=view_transactions).pack(side="left", padx=5)

frame_history = tk.LabelFrame(root, text="Transaction History", padx=10, pady=5)
frame_history.pack(fill="both", expand=True, padx=10, pady=5)

transaction_listbox = tk.Listbox(frame_history, height=8, width=80)
transaction_listbox.pack(fill="both", expand=True)

refresh_user_list()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()