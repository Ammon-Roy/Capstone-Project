import sqlite3
import bcrypt

connection = sqlite3.connect('capstone_database.db')
cursor = connection.cursor()

def get_user_id(email):
    user_id = cursor.execute("SELECT user_id FROM Users WHERE email =?",(email,)).fetchone()
    return user_id[0]

def create_schema():
    with open("capstone_scheme.sql") as sql_file:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
    connection.commit()

def cont_button():          
    while True:
        c_input = input("Press C to continue: ").upper()
        if c_input == "C":
            return None
        else: 
            continue

def store_password(password, user_id):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE Users SET password=? WHERE user_id = ?", (hashed_password, user_id))
    connection.commit()

def user_authentication(email, password):
    try:
        check_value = cursor.execute("SELECT password FROM Users WHERE email=?", (email,)).fetchone()
        if check_value[0] == '1234':
            if check_value[0] == password:
                print("!!!  PLEASE CHANGE YOUR PASSWORD FROM DEFAULT  !!!")
                return True
        elif check_value[0] == bcrypt.hashpw(password.encode('utf-8'), check_value[0]):
            return True
    except:
        return False

def change_password(user_id):
    while True:
        new_pass = input("Enter your new password: ")
        check = input("Type your new password again: ")
        if new_pass == check:
            store_password(new_pass, user_id)
            print("Password Changed!")
            cont_button()
            break
        else:
            print("Passwords do not Match")
            new_input = ("Press ENTER to try again, or anything else to go back.")
            if new_input == "":
                continue
            else:
                break

def change_name(user_id):
    first = input("Please enter your First name: ")
    last = input("Please enter your Last name: ")
    sql_string = "UPDATE Users SET first_name = ? last_name = ? Where user_id = ?",(first, last, user_id,)
    cursor.exevute(sql_string)
    final_check = input("do you want to commit these changes?(Y/N) ").upper()
    if final_check == "Y":
        connection.commit()
        print("Profile Updated!")
        cont_button()
    else:
        print("Data not commited.")
        cont_button()
