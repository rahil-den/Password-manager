import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import pyperclip

from db import init_db, add_entry, get_entries_by_site, get_entries, delete_entry, list_all_sites
from crypto_utils import generate_key, encrypt_passsword, decrypt_password

import os
from dotenv import load_dotenv
load_dotenv()
MASTER_PASSWORD = os.getenv("MASTER_PASSWORD")  # Use dotenv in real apps


class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Manager")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        generate_key()
        init_db()
        self.login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="🔐 Enter Master Password", font=("Arial", 16, "bold")).pack(pady=30)
        self.password_entry = tk.Entry(self.root, show="*", width=25, font=("Arial", 12))
        self.password_entry.pack()
        tk.Button(self.root, text="Login", command=self.check_password, width=20).pack(pady=10)

    def check_password(self):
        if self.password_entry.get() == MASTER_PASSWORD:
            self.main_screen()
        else:
            messagebox.showerror("Access Denied", "Incorrect master password!")

    def main_screen(self):
        self.clear_window()
        tk.Label(self.root, text="📘 Password Manager", font=("Arial", 18, "bold")).pack(pady=15)

        options = [
            ("➕ Add Entry", self.add_entry_screen),
            ("🔍 Retrieve Entry", self.retrieve_screen),
            ("📃 View All Entries", self.view_all_entries),
            ("📁 List All Sites", self.list_sites),
            ("🗑️ Delete Entry", self.delete_entry_screen),
        ]

        for text, cmd in options:
            tk.Button(self.root, text=text, width=25, command=cmd).pack(pady=5)

    def add_entry_screen(self):
        self.clear_window()
        tk.Label(self.root, text="➕ Add New Entry", font=("Arial", 16, "bold")).pack(pady=10)

        self.site_entry = tk.Entry(self.root, width=30)
        self.site_entry.insert(0, "Site")
        self.site_entry.pack(pady=5)
        self.site_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.site_entry, "Site"))

        self.user_entry = tk.Entry(self.root, width=30)
        self.user_entry.insert(0, "Username")
        self.user_entry.pack(pady=5)
        self.user_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.user_entry, "Username"))

        self.pass_entry = tk.Entry(self.root, width=30)
        self.pass_entry.insert(0, "Password")
        self.pass_entry.pack(pady=5)
        self.pass_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.pass_entry, "Password"))

        tk.Button(self.root, text="💾 Save Entry", command=self.save_password, width=20).pack(pady=10)
        tk.Button(self.root, text="🔙 Back", command=self.main_screen).pack()

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def save_password(self):
        site = self.site_entry.get().strip()
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        if site and user and pwd:
            encrypted = encrypt_passsword(pwd)
            add_entry(site, user, encrypted)
            messagebox.showinfo("Saved", "Password saved successfully!")
            self.main_screen()
        else:
            messagebox.showerror("Error", "All fields are required.")

    def retrieve_screen(self):
        self.clear_window()
        tk.Label(self.root, text="🔍 Retrieve Entry", font=("Arial", 16, "bold")).pack(pady=15)

        self.retrieve_entry = tk.Entry(self.root, width=30)
        self.retrieve_entry.insert(0, "Enter Site")
        self.retrieve_entry.pack(pady=5)
        self.retrieve_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.retrieve_entry, "Enter Site"))

        tk.Button(self.root, text="🔎 Search", command=self.retrieve_password, width=20).pack(pady=5)
        tk.Button(self.root, text="🔙 Back", command=self.main_screen).pack()

    def retrieve_password(self):
        site = self.retrieve_entry.get().strip()
        entries = get_entries_by_site(site)

        if entries:
            result_text = ""
            for _, s, u, p in entries:
                decrypted = decrypt_password(p)
                result_text += f"Site: {s}\nUsername: {u}\nPassword: {decrypted}\n\n"
                pyperclip.copy(decrypted)
            messagebox.showinfo("Result", result_text + "\nPassword copied to clipboard.")
        else:
            messagebox.showerror("Not Found", f"No entry found for site: {site}")

    def delete_entry_screen(self):
        self.clear_window()
        tk.Label(self.root, text="🗑️ Delete Entry", font=("Arial", 16, "bold")).pack(pady=15)

        self.delete_entry_field = tk.Entry(self.root, width=30)
        self.delete_entry_field.insert(0, "Enter Site")
        self.delete_entry_field.pack(pady=5)
        self.delete_entry_field.bind("<FocusIn>", lambda e: self.clear_placeholder(self.delete_entry_field, "Enter Site"))

        tk.Button(self.root, text="❌ Delete", command=self.delete, width=20).pack(pady=5)
        tk.Button(self.root, text="🔙 Back", command=self.main_screen).pack()

    def delete(self):
        site = self.delete_entry_field.get().strip()
        delete_entry(site)
        messagebox.showinfo("Deleted", f"Deleted entry for {site}")
        self.main_screen()

    def list_sites(self):
        self.clear_window()
        tk.Label(self.root, text="📁 All Saved Sites", font=("Arial", 16, "bold")).pack(pady=10)

        sites = list_all_sites()

        scroll_frame = scrolledtext.ScrolledText(self.root, width=45, height=15, font=("Courier", 10))
        scroll_frame.pack(pady=5)
        for site in sites:
            scroll_frame.insert(tk.END, f"• {site}\n")
        scroll_frame.config(state=tk.DISABLED)

        tk.Button(self.root, text="🔙 Back", command=self.main_screen).pack(pady=10)

    def view_all_entries(self):
        self.clear_window()
        tk.Label(self.root, text="📃 All Entries", font=("Arial", 16, "bold")).pack(pady=10)

        entries = get_entries()
        if not entries:
            tk.Label(self.root, text="No entries found.", font=("Arial", 12)).pack(pady=10)
            tk.Button(self.root, text="🔙 Back", command=self.main_screen).pack()
            return

        scroll_frame = scrolledtext.ScrolledText(self.root, width=50, height=20, font=("Courier", 9))
        scroll_frame.pack(pady=5)

        for _, site, user, enc_pwd in entries:
            pwd = decrypt_password(enc_pwd)
            scroll_frame.insert(tk.END, f"Site: {site}\nUser: {user}\nPassword: {pwd}\n\n")

        scroll_frame.config(state=tk.DISABLED)

        tk.Button(self.root, text="🔙 Back", command=self.main_screen).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
