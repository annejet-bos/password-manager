from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv('EMAIL')

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    password_input.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            'email': email,
            'password': password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title = 'Oops', message = "Please don't leave any fields empty")
    else:
        try:
            with open('data.json', 'r') as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent = 4)
        else:
            #Updating old data with new data
            data.update(new_data)

            with open('data.json', 'w') as data_file:
                #Saving updated data
                json.dump(data, data_file, indent = 4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)
            email_input.delete(0, END)
            email_input.insert(END, EMAIL)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    website = website_input.get()

    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title = 'Error', message = "No Data File Found")
    else:
        if website in data.keys():
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}"
                                                       f"\nPassword: {password}")
        else:
            messagebox.showinfo(title='Error', message="No details for the website exists")
    finally:
        website_input.delete(0, END)



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx = 50, pady = 50)


canvas = Canvas(width = 200, height = 200)
logo_img = PhotoImage(file = 'logo.png')
canvas.create_image(100, 100, image = logo_img)
canvas.grid(column = 1, row = 0)


#Website label
website_label = Label(text = 'Website:')
website_label.grid(column = 0, row = 1)

#Website input
website_input = Entry()
website_input.focus()
website_input.grid(column = 1, row = 1, sticky = 'EW')

#Email/username label
email_label = Label(text = 'Email/Username:')
email_label.grid(column = 0, row = 2)

#Email input
email_input = Entry()
email_input.insert(END, EMAIL)
email_input.grid(column = 1, row = 2, columnspan = 2, sticky = 'EW')

#Password label
password_label = Label(text = 'Password:')
password_label.grid(column = 0, row = 3)

#Password input
password_input = Entry()
password_input.grid(column = 1, row = 3, sticky = 'EW')

#Generate password button
gen_password = Button(text = 'Generate Password', command = password_generator)
gen_password.grid(column = 2, row = 3)

#Add button
add_button = Button(text = 'Add', command=save)
add_button.grid(column = 1, row = 4, columnspan= 2, sticky = 'EW')

#search button
search_button = Button(text = 'Search', command = find_password)
search_button.grid(column = 2, row = 1, sticky = 'EW')


window.mainloop()

