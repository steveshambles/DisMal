"""
Dismal v0.45 (Disposable Email)

Simple desktop GUI to create
a disposable email address and go to
the inbox, all  accomplished in a few seconds
and just a few clicks.

By Steve Shambles Oct 2018.
Updated Nov 2019 and Jan 2021.

https://stevepython.wordpress.com/

Dependants:
pip3 install awesometkinter
pip3 install Pillow
pip3 install pyperclip

files required, in same location as this file:
dismal_logov2.png
dismal_help.txt

logo bg col ='#2a3f54'
"""
import os
from random import randint, choice
import string
import tkinter as tk
from tkinter import ttk
from tkinter import BOTTOM, E, END, Entry, Frame, Label, Listbox, Menu
from tkinter import messagebox, RIGHT, Scrollbar, W, X, Y
import webbrowser as web

import awesometkinter as atk
from PIL import Image, ImageTk
import pyperclip


root = tk.Tk()
root.title('Dismal v0.45. Feb 2021')
root.config(background=atk.DEFAULT_COLOR)
root.eval('tk::PlaceWindow . Center')

s = ttk.Style()
s.theme_use('default')

BASE_URL = 'https://www.mailinator.com/v3/index.jsp?zone=public&query='
BASE_EMAIL = '@mailinator.com'


check_file = os.path.isfile('dismal_help.txt')
if not check_file:
    messagebox.showerror('Question',
                         'The help file\ndismal_help.txt\n'
                         'is missing, not essential file\n'
                         'so continuing anyway...')


def load_emails():
    """Load in text file containing previously made emails."""
    if os.path.isfile('dismal-lb.txt'):
        with open('dismal-lb.txt', 'r') as f:
            emails = f.read().splitlines()

            if emails:
                for x in range(len(emails)):
                    list_box.insert('end', emails[x])
    else:
        with open('dismal-lb.txt', 'w') as _:
            pass


def clk_but():
    """Button was clicked so create Email address."""
    # Get contents of entry box.
    e_name = entry_box.get()

    if not e_name:
        # If no username entered, create random one.
        allchar = string.ascii_lowercase + string.digits
        e_name = ''.join(choice(allchar) for x in range(randint(6, 8)))

    # strip out any spaces in name.
    e_name = e_name.replace(" ", "")

    # Construct email address.
    email_address = e_name+BASE_EMAIL

    # Copy email address to clipboard.
    pyperclip.copy(email_address)

    # Clear entry box and insert new address in listbox.
    entry_box.delete(0, END)
    list_box.insert('end', email_address)

    # Append new email address to text file for reloding next.
    with open('dismal-lb.txt', 'a') as contents:
        save_it = str(email_address+'\n')
        contents.write(save_it)

    ask_yn = messagebox.askyesno('Info', 'your new email address is\n\n'
                                 + str(email_address)+'\n\n'
                                 'The address has been copied\n'
                                 'to your clipboard.\n\n'
                                 'Click "Yes" to go to your inbox now,\n')
    if not ask_yn:
        entry_box.focus()
        return

    # Open new adresses inbox in browser.
    web.open(BASE_URL+e_name)

    # Place cursor inside entry box awaiting next creation.
    entry_box.focus()


def about_menu():
    """About program."""
    messagebox.showinfo('About',
                        'Dismal v0.45 Freeware By Steve Shambles.\n'
                        'Last updated Feb 2021.')


def visit_blog():
    """Visit my blog."""
    web.open('https://stevepython.wordpress.com/')
    entry_box.focus()


def go_mailinator():
    """Logo was double-clicked, visit mailinator website."""
    web.open(BASE_URL)
    entry_box.focus()


def popup(event):
    """On right click display popup menu at mouse position."""
    rc_menu.post(event.x_root, event.y_root)


def copy_em_adr():
    """Called when Copy to clipboard selected from right click menu."""
    try:
        selection = list_box.curselection()
        slctd_adrs = list_box.get(selection[0])
    except IndexError:
        messagebox.showerror('Error:', 'Nothing selected')
        return
    pyperclip.copy(slctd_adrs)
    messagebox.showinfo('Info', slctd_adrs + '\nCopied to clipboard.')
    entry_box.focus()


def delete_all():
    """Delete all email addresses from listbox and text file."""
    ask_yn = messagebox.askyesno('Question', 'Delete all Email addresses?')

    if not ask_yn:
        return

    # Remove all items from the listbox.
    list_box.delete(0, 'end')

    # Blank the text file.
    with open('dismal-lb.txt', 'w') as _:
        pass

    entry_box.focus()


def delete_em_adr():
    """Called when delete address is selected from right click menu."""
    # Get the file that is selected in the list box.
    try:
        selection = list_box.curselection()
        slctd_adrs = list_box.get(selection[0])
    except IndexError:
        messagebox.showerror('Error:', 'Nothing selected')
        return

    ask_yn = messagebox.askyesno('Question', 'Delete selected Email?')
    if not ask_yn:
        return

    # Delete email.
    list_box.delete(selection)
    # Remove email from text file by re-opening as a blank file
    # and re-saving with current listbox contents.
    with open('dismal-lb.txt', 'w') as g:
        g.write('\n'.join(list_box.get(0, END)))
        g.write('\n')

    entry_box.focus()


def open_inbox():
    """Open currently selected email address at malinator.com."""
    try:
        selection = list_box.curselection()
        slctd_adrs = list_box.get(selection[0])
    except IndexError:
        messagebox.showerror('Error:', 'Nothing selected')
        return
    #  Remove @malinator.com from value.
    value2 = slctd_adrs.replace('@mailinator.com', '')
    eml_adrs = BASE_URL+value2
    web.open(eml_adrs)
    entry_box.focus()


def open_in_txt():
    """Open the text file that stores the list of emails."""
    web.open('dismal-lb.txt')
    entry_box.focus()


def help_me():
    """Opens a help, using systems default text viewer."""
    web.open('dismal_help.txt')
    entry_box.focus()


def exit_app():
    """Don't go.I love you and want to have your children, I'm rich too!."""
    ask_yn = messagebox.askyesno('Question', 'Confirm exit Dismal?')
    if not ask_yn:
        return
    root.destroy()


logo_frame = Frame(root)
logo_frame.grid(padx=8, pady=8)

main_frame = atk.Frame3d(root)
main_frame.grid(padx=10, pady=10)

listbox_frame = atk.Frame3d(root)
listbox_frame.grid(padx=10, pady=10)

# Load and display logo.
if not os.path.isfile('dismal_logov2.png'):
    messagebox.showerror('File Error:', 'dismal_logov2.png\nIs missing.')
    root.destroy()
logo_image = Image.open('dismal_logov2.png')
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(logo_frame, image=logo_photo)
logo_label.logo_image = logo_photo
logo_label.grid(padx=2, pady=2, row=0, column=0)

# Create entry box.
entry_box = Entry(main_frame, bd=3, bg='slategray1')
entry_box.grid(sticky=W+E, padx=5, pady=5)

# Create Email button.
create_mail_btn = atk.Button3d(main_frame, text='Create Email',
                               command=clk_but)
create_mail_btn.grid(pady=15, padx=15)

# Listbox with scrollbars.
list_box = Listbox(
    master=listbox_frame,
    selectmode='single',
    width=25,
    height=8,
    bg='powderblue',
    fg='navyblue')

sbar_vert = Scrollbar(listbox_frame, orient='vertical')
sbar_vert.pack(side=RIGHT, fill=Y)
list_box.configure(yscrollcommand=sbar_vert.set)
sbar_vert.configure(command=list_box.yview)

sbar_hor = Scrollbar(listbox_frame, orient='horizontal')
sbar_hor.pack(side=BOTTOM, fill=X)
list_box.configure(xscrollcommand=sbar_hor.set)
sbar_hor.configure(command=list_box.xview)

list_box.pack()

# Bind mouse right click to listbox for right-click pop up menu.
list_box.bind('<Button-3>', popup)

# Create the popup menu.
rc_menu = Menu(root, tearoff=0)

rc_menu.add_command(label='Open inbox',
                    command=open_inbox)
rc_menu.add_command(label='Copy address to clipboard',
                    command=copy_em_adr)
rc_menu.add_separator()
rc_menu.add_command(label='Delete this address',
                    command=delete_em_adr)
rc_menu.add_command(label='Delete all addresses',
                    command=delete_all)
rc_menu.add_separator()
rc_menu.add_command(label='Open all addresses in a text file',
                    command=open_in_txt)
rc_menu.add_command(label='Visit mailinator.com',
                    command=go_mailinator)
rc_menu.add_separator()
rc_menu.add_command(label='Help',
                    command=help_me)

# Drop-down menu.
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=file_menu)
file_menu.add_command(label='Help', command=help_me)
file_menu.add_command(label='About', command=about_menu)
file_menu.add_separator()
file_menu.add_command(label='Visit my Blog', command=visit_blog)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exit_app)
root.config(menu=menu_bar)

entry_box.focus()
load_emails()

root.protocol("WM_DELETE_WINDOW", exit_app)

root.mainloop()

"""
How to find out what exception name occurs when error.
https://www.programiz.com/python-programming/exception-handling
 import sys
 in the try except loop insert this:
 print("Oops!", sys.exc_info()[0], "occurred.")
"""
