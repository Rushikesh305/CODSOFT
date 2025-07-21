import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DATA_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_contacts():
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)


def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if not name or not phone:
        messagebox.showerror("Error", "Name and Phone number are required!")
        return

    contacts[name] = {
        "Phone": phone,
        "Email": email,
        "Address": address
    }

    save_contacts()
    messagebox.showinfo("Success", f"Contact '{name}' added.")
    clear_entries()
    refresh_contact_list()


def refresh_contact_list():
    contact_listbox.delete(0, tk.END)
    for name, info in contacts.items():
        contact_listbox.insert(tk.END, f"{name} - {info['Phone']}")


def search_contact():
    query = search_entry.get().lower()
    contact_listbox.delete(0, tk.END)
    for name, info in contacts.items():
        if query in name.lower() or query in info["Phone"]:
            contact_listbox.insert(tk.END, f"{name} - {info['Phone']}")


def delete_contact():
    selected = contact_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a contact to delete.")
        return

    selected_text = contact_listbox.get(selected[0])
    name = selected_text.split(" - ")[0]

    if name in contacts:
        del contacts[name]
        save_contacts()
        messagebox.showinfo("Deleted", f"Contact '{name}' deleted.")
        refresh_contact_list()


def load_selected_contact():
    selected = contact_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Select a contact to update.")
        return

    selected_text = contact_listbox.get(selected[0])
    name = selected_text.split(" - ")[0]
    info = contacts[name]

    name_entry.delete(0, tk.END)
    name_entry.insert(0, name)
    phone_entry.delete(0, tk.END)
    phone_entry.insert(0, info["Phone"])
    email_entry.delete(0, tk.END)
    email_entry.insert(0, info["Email"])
    address_entry.delete(0, tk.END)
    address_entry.insert(0, info["Address"])


def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)


contacts = load_contacts()

root = tk.Tk()
root.title("Contact Book")
root.geometry("600x500")


tk.Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky='e')
tk.Label(root, text="Phone").grid(row=1, column=0, padx=5, pady=5, sticky='e')
tk.Label(root, text="Email").grid(row=2, column=0, padx=5, pady=5, sticky='e')
tk.Label(root, text="Address").grid(row=3, column=0, padx=5, pady=5, sticky='e')

name_entry = tk.Entry(root, width=40)
phone_entry = tk.Entry(root, width=40)
email_entry = tk.Entry(root, width=40)
address_entry = tk.Entry(root, width=40)

name_entry.grid(row=0, column=1, padx=5, pady=5)
phone_entry.grid(row=1, column=1, padx=5, pady=5)
email_entry.grid(row=2, column=1, padx=5, pady=5)
address_entry.grid(row=3, column=1, padx=5, pady=5)


tk.Button(root, text="Add Contact", command=add_contact).grid(row=4, column=0, padx=5, pady=10)
tk.Button(root, text="Update Contact", command=add_contact).grid(row=4, column=1, padx=5, pady=10, sticky='w')
tk.Button(root, text="Delete Selected", command=delete_contact).grid(row=4, column=1, padx=5, pady=10, sticky='e')
tk.Button(root, text="Load Selected", command=load_selected_contact).grid(row=5, column=0, padx=5, pady=5)
tk.Button(root, text="Clear Fields", command=clear_entries).grid(row=5, column=1, padx=5, pady=5, sticky='w')


tk.Label(root, text="Search:").grid(row=6, column=0, padx=5, pady=10)
search_entry = tk.Entry(root, width=30)
search_entry.grid(row=6, column=1, padx=5, pady=10, sticky='w')
tk.Button(root, text="Search", command=search_contact).grid(row=6, column=1, padx=5, pady=10, sticky='e')

contact_listbox = tk.Listbox(root, width=60, height=10)
contact_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

refresh_contact_list()

root.mainloop()