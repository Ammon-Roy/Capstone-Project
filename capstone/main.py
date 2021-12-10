from capstone_functions import *
from csv_func import *
from datetime import date

create_schema()
while True:    
    
    portal = input("[M]anager\n[U]ser\n[Q]uit\n").upper()
    
    
    if portal == "U":    
        while True:
            # Login
            while True:
                global email
                email = input("Please enter your email: ").lower()
                password = input("Please enter your password: ")
                if user_authentication(email, password) == True:
                    global user_id
                    user_id = get_user_id(email)
                    break
                else:
                    print("Email or Password is incorrect. Please contact a manager if you need to create an account.")
                    cont_button()

            #menu
            while True:
                menu_input = input(
"""
Welcome to the Assessment Tracker
_________________________________

[1] View Report
[2] Options
[Q]uit
""").upper()
            
                if menu_input == '1':
                    user_report = UserReport(cursor, "user_report", user_id)
                    user_report.csv_creation(["name","comp_scores","avg_comp"])
                    user_report.csv_write()
                    with open("user_report.csv") as report:
                        row = list(csv.DictReader(report))
                        row = row[0]
                        print("\n\n")
                    print(f'''{row["name"]}'s Report:''')
                    item_list = "".join(row["comp_scores"]).strip("[]").replace("'", "").split(", (")
                    for test in item_list:
                        test = test.split(", ")
                        print(f"{test[0]:<25}{test[1]:<25}{test[2]:<25}")
                    cont_button()
                    continue
                
                
                
                #option sub menu
                if menu_input == '2':
                    while True:
                        option_input = input(
"""
OPTIONS:
--------
[1] Change Password
[2] Change Name
[3] Clear CSV file
[4] <--- Back
"""
                        )
                        
                        if option_input == "1":
                            change_password(user_id)
                        
                        if option_input == "2":
                            change_name(user_id)
                        
                        if option_input == "3":
                            clear_check = input("Are you sure you want to clear the user report csv file?(Y/N) ").upper()
                            if clear_check == "Y":
                                user_wipe = WriteCsv(cursor,"user_report")
                                user_wipe.wipe(["name","comp_scores","avg_comp"])
                                cont_button()
                            elif clear_check != "Y":
                                print("CSV files not Erased...")
                                cont_button()
                        
                        else:
                            break



                else: 
                    print("Session Closing...")
                    user_wipe = WriteCsv(cursor,"user_report")
                    user_wipe.wipe(["name","comp_scores","avg_comp"])
                    print("Session Closed. Goodbye.")
                    quit()
        

    
    
    
    
    if portal == "M":
        while True:
            # manager Login
            while True:
                
                email = input("Please enter your email: ")
                password = input("Please enter your password: ")
                
                if user_authentication(email, password) == True:
                    user_id = get_user_id(email)
                    user_type = cursor.execute("SELECT user_type FROM Users WHERE user_id = ?",(user_id,)).fetchone()
                    user_type = user_type[0]
                    if user_type == "user":
                        print("You do not have permissions to enter the manager portal. Shutting down application.")
                        exit()
                    else:
                        break
                else:
                    print("Email or Password is incorrect. Please contact a manager if you need to create an account.")
                    cont_button()
            
            # Manager menu
            while True:
                menu_input = input(
'''
Welcome to the Assesssment Tracker (Manager View)
_________________________________________________

[1] View all Users
[2] Search Users
[3] Competency Report
[4] List of Assessments by User
[5] Options
[Q]UIT
'''
                ).upper()
                if menu_input == "1":
                    user_list = cursor.execute("SELECT user_id, first_name, last_name FROM Users WHERE user_type = 'user' AND active = 1").fetchall()
                    print("List of Users:\n")
                    for i in user_list:
                        i = ' '.join(i)
                        print(i)
                    cont_button()
                    continue
                
                if menu_input == "2":
                    while True:    
                        search_input = input(
'''
[F]irst name search
[L]ast name search
[1] <--- Back
'''
                            ).upper()
                        if search_input == "F":
                            search_first = input("Search by first name(press ENTER to go back main menu): ")
                            if search_first == "":
                                continue
                            else:
                                user_list = cursor.execute("SELECT user_id, first_name, last_name FROM Users WHERE first_name LIKE '%'||?||'%' AND user_type = 'user' AND active = 1",(search_first,)).fetchall()
                                if user_list == []:
                                    print("!!!NOT FOUND!!!")
                                    cont_button()
                                    continue
                                else:
                                    print(f"Results for Search '{search_first}':\n")
                                    for i in user_list:
                                        i = ' '.join(i)
                                        print(i)
                                    cont_button()
                                    continue
                        if search_input == "L":
                            search_last = input("Search by last name(press ENTER to go back main menu): ")
                            if search_last == "":
                                continue
                            else:
                                user_list = cursor.execute("SELECT user_id,first_name, last_name FROM Users WHERE last_name LIKE '%'||?||'%' AND user_type = 'user' AND active = 1",(search_last,)).fetchall()
                                if user_list == []:
                                    print("!!!NOT FOUND!!!")
                                    cont_button()
                                    continue
                                else:
                                    print(f"Results for Search '{search_last}':\n")
                                    for i in user_list:
                                        i = ' '.join(i)
                                        print(i)
                                    cont_button()
                                    continue
                        
                        if search_input == "1":
                            break
                        else: continue
                
                
                if menu_input == "3":
                    comp_id = input("What is the Competency ID: ")
                    comp_name = cursor.execute("SELECT name FROM Competencies WHERE comp_id = ?",(comp_id,)).fetchone()[0]
                    comp_report = CompReport(cursor, "comp_report", comp_id)
                    comp_list = comp_report.csv_write()
                    print(f'\n{comp_name}')
                    for item in comp_list:
                        print(f'{item[0]} {item[1]}')
                    print('\n')
                    cont_button()
                    continue

                if menu_input == "4":
                    user_id_input = input("What is the ID of the user's assessments you want to view: ")
                    assessment_report = cursor.execute("SELECT u.first_name, u.last_name, ar.assessment_id, ar.date_taken, a.name FROM Assessments_results ar, Assessments a, Users u WHERE u.user_id = ar.user_id AND ar.assessment_id = a.assessment_id AND u.user_id = ? AND u.active = 1 ORDER BY date_taken",(user_id_input)).fetchall()
                    if assessment_report == []:
                        print("!!! User Not Found !!!")
                        cont_button()
                        continue
                    else:
                        ar = assessment_report[0]
                        user_name = f'{ar[0]} {ar[1]}'
                        user_assessment_list = []
                        for row in assessment_report:  
                            assessment = f'{row[4]}, {row[3]}'
                            user_assessment_list.append(assessment)
                        print(f'{user_name}\'s test history:')
                        for i in user_assessment_list:
                            print(i)
                        cont_button()
                        continue

                if menu_input == "5":
                    while True:    
                        option_input = input(
'''
OPTIONS:
--------
[1] Change Password
[2] Change Name
[3] ADD
[4] EDIT
[5] DELETE
[6] Wipe ALL CSV
[7] <--- Back
'''
                        )
                        if option_input == "1":
                            change_password(user_id)
                        if option_input == "2":
                            change_name(user_id)
                        if option_input == "3":
                            while True:
                                add_input = input(
'''
ADD:
[U]ser
[C]ompetency
[A]ssessment
[R]esults
[1] <--- Back
'''
                                ).upper()
                                if add_input == "U":
                                    print("Adding New User...")
                                    first_name = input("Enter first name: ")
                                    last_name = input("Enter last name: ")
                                    email = input("Enter Email: ")
                                    creation_date = date.today()
                                    creation_date = creation_date.strftime("%m/%d/%Y")
                                    try:    
                                        cursor.execute("INSERT INTO Users (first_name,last_name,email,date_created) VALUES (?,?,?,?)",(first_name,last_name,email,creation_date,))
                                        connection.commit()
                                        print("New user added!")
                                        cont_button()
                                        continue
                                    except:
                                        print("!!! User email already in system or data inputed is not correct !!!")
                                        cont_button()
                                        continue
                                if add_input == "C":
                                    print("Adding New Competency")
                                    comp_name = input("new Competency's name: ")
                                    creation_date = date.today
                                    creation_date = creation_date.strftime("%m/%d/%Y")
                                    try:    
                                        cursor.execute("INSERT INTO Competencies (name, date_created) VALUES (?,?)",(comp_name,creation_date,))
                                        connection.commit()
                                        print("New Competency Created!")
                                        cont_button()
                                        continue
                                    except:
                                        print("!!! Invalid Input Data !!!")
                                        cont_button()
                                        continue
                                if add_input == "A":
                                    print("Adding New Assessment")
                                    Assessment_name = input("new Competency's name: ")
                                    creation_date = date.today
                                    creation_date = creation_date.strftime("%m/%d/%Y")
                                    try:    
                                        cursor.execute("INSERT INTO Assessments (name, date_created) VALUES (?,?)",(Assessment_name,creation_date,))
                                        connection.commit()
                                        print("New Competency Created!")
                                        cont_button()
                                        continue
                                    except:
                                        print("!!! Invalid Input Data !!!")
                                        cont_button()
                                        continue
                                if add_input == "R":
                                    add_u_id = input("User ID: ")
                                    add_c_id = input("Competency ID: ")
                                    add_a_id = input("Assessment ID: ")
                                    score = input("Score of Assessment: ")
                                    date_taken = date.today
                                    date_taken = date_taken.strftime("%m/%d/%Y")
                                    manager = input("Manager ID: ")
                                    try:    
                                        cursor.execute("INSERT INTO Assessments_results (user_id, comp_id, assessment_id, socre, date_taken, manager) VALUES(?,?,?,?,?)",(add_u_id,add_c_id,add_a_id,date_taken,manager))
                                        connection.commit()
                                        print("Result Added!")
                                        cont_button()
                                        continue
                                    except:
                                        print("!!! Invalid Data !!!")
                                        cont_button()
                                        continue
                                if add_input == "1":
                                    break
                                else:continue

                        if option_input == "4":
                            while True:
                                edit_input = input(
'''
EDIT:
[U]ser
[C]ompetency
[A]ssessment
[R]esults
[1] <--- Back
'''
                                ).upper()
                                if edit_input == "U":
                                    update_u_id = input("ID of User that needs edit: ")
                                    first_name = input("Enter first name: ")
                                    last_name = input("Enter last name: ")
                                    email = input("Enter Email: ")
                                    try:
                                        cursor.execute("UPDATE Users SET first_name = ?, last_name = ?, email = ? WHERE user_id =?",(first_name,last_name,email, update_u_id,))
                                        connection.commit()
                                        print("Database Updated")
                                        cont_button()
                                        continue
                                    except:
                                        print("!!! INVALID DATA !!!")
                                        cont_button()
                                        continue
                                if edit_input == "C":
                                    competency_id = input("Competency ID that needs name changed: ")
                                    name = input("Enter new Competency name: ")
                                    try:
                                        cursor.execute("UPDATE Competencies SET name = ? WHERE comp_id = ?",(name,competency_id,))
                                        connection.commit()
                                        print("Database Updated")
                                        cont_button()
                                        continue
                                    except:
                                        print("!!! INVALID DATA !!!")
                                        cont_button()
                                        continue
                                if edit_input == "A":
                                    Assessment_id = input("Assessment ID that needs name changed: ")
                                    name = input("Enter new Assessment name: ")
                                    try:
                                        cursor.execute("UPDATE Assessments SET name = ? WHERE comp_id = ?",(name,Assessment_id,))
                                        connection.commit()
                                        print("Database Updated")
                                        cont_button()
                                        continue
                                    except:
                                        print("!!! INVALID DATA !!!")
                                        cont_button()
                                        continue
                                if edit_input == "R":
                                    result_id = input("What is the Result ID that needs changing: ")
                                    u_id = input("User ID: ")
                                    c_id = input("Competency ID: ")
                                    a_id = input("Assessment ID")
                                    score = input("Update Score: ")
                                    manager = input("Manager ID: ")
                                    try:
                                        cursor.execute("UPDATE Assessments_results SET user_id = ?, comp_id = ?, assessment_id = ?, score = ?, manager = ?",(u_id,c_id,a_id,score,manager))
                                        connection.commit()
                                        print("Database Updated")
                                        cont_button()
                                        continue
                                    except:
                                        print("!!! INVALID DATA !!!")
                                        cont_button()
                                        continue
                                if edit_input == "1":
                                    break
                                else:continue

                        if option_input == "5":
                            while True:
                                delete_input = input(
"""
DETETE:
[U]ser
[C]ompetency
[A]ssessment
[R]esults
[1] <--- Back
"""
                                ).upper()
                                if delete_input == "U":
                                    print("Option Coming soon!")
                                    cont_button()
                                    continue
                                if delete_input == "C":
                                    print("Option Coming soon!")
                                    cont_button()
                                    continue
                                if delete_input == "A":
                                    print("Option Coming soon!")
                                    cont_button()
                                    continue
                                if delete_input == "R":
                                    print("Option Coming soon!")
                                    cont_button()
                                    continue
                                if delete_input == "1":
                                    break
                                else:continue
                        if option_input == "6":
                            clear_check = input("Are you sure you want to clear the user report csv file?(Y/N) ").upper()
                            if clear_check == "Y":
                                user_wipe = WriteCsv(cursor,"user_report")
                                result_wipe = WriteCsv(cursor,"result_csv")
                                comp_wipe = WriteCsv(cursor, "comp_report")
                                user_wipe.wipe(["name","comp_scores","avg_comp"])
                                result_wipe.wipe(["user_id","comp_id","assessment_id","score","date_taken","manager"])
                                comp_wipe.wipe(["User","Score"])
                                print("Wipe Complete!")
                                cont_button()
                            elif clear_check != "Y":
                                print("CSV files not Erased...")
                                cont_button()
                        if option_input == "7":
                            break
                        else:continue
                
                
                if menu_input == "Q":
                    print("Session Closing...")
                    user_wipe = WriteCsv(cursor,"user_report")
                    result_wipe = WriteCsv(cursor,"result_csv")
                    comp_wipe = WriteCsv(cursor, "comp_report")
                    user_wipe.wipe(["name","comp_scores","avg_comp"])
                    result_wipe.wipe(["user_id","comp_id","assessment_id","score","date_taken","manager"])
                    comp_wipe.wipe(["User","Score"])
                    print("Session Closed. Goodbye.")
                    quit()
                else:continue






    if portal == "Q":
        print("Thank you for using an Ammon Roy product my venmo is...")
        quit()
    else:continue