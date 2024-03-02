'''
Title       :   Task 17 Capstone Task Manager Application
Author      :   Imran Bhatti IB23100009590
Date Created:   January 2024           
Last Updated:   January 2024
Description :   Program to handle and maintain users and tasks
                Sourcing data from files and creating report files
                The menu options are as follows:
                Initially login with username & password, will give you 
                an option to register also
                r  - Registering a user
                This option registers a user, checks if the username already
                exists and confirmation of password and writes to the user.txt
                a  - Adding a task
                This option adds a task and checks if the username assigned to the
                task already exists and outputs to the tasks.txt file 
                va - View all tasks
                Prints all the tasks to the terminal
                vm - View my task
                Prints all tasks to the user who is logged, allows user to choose a
                a task to amend and gives options to amend assigned username or due date 
                or mark as complete 
                gr - Generate reports
                Creates two files
                task_overview.txt which has summary details of the Tasks in the app
                user_overview.txt which has summary details of the users and user task details
                ds - Display statistics (ADMIN Only)
                Only able to be used by the Admin and gives options of to output all details
                to the terminal in the files tasks.txt and user.txt                
                e  - Exit
                Exits the application after confirmation
'''

# Importing libraries
import os
from datetime import datetime, date
from getpass import getpass
# Default date format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Filename variables

# Input/Output file
TASK_FILE = "tasks.txt"
USER_FILE = "user.txt"

# Report files
USER_OVERVIEW = "user_overview.txt"
TASK_OVERVIEW = "task_overview.txt"

# Dictionary to hold all username and passwords
username_password = {}
# Line separator
LINE = '=' * 80
CLEAR = "\n" * 10

def user_file_input():
    ''' Creates or loads file user.txt '''
    # If no user.txt file, create file with default admin account
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", encoding="utf-8-sig") as default_file:
            default_file.write("admin;password")
    # Read in user_data
    try:
        with open(USER_FILE, 'r', encoding="utf-8-sig") as user_f:
            user_file_data = user_f.read().split("\n")
            # Create username_password dictionary by splitting by ;
            for user_pass in user_file_data:
                username, password = user_pass.split(';')
                # username is key and password value
                username_password[username] = password
    except FileExistsError as file_error:
        print(f"user_file.txt {file_error}")
        # Returning user_file_data
    return user_file_data

def task_file_input():
    '''Creates or loads tasks.txt file and outputs as dictionary'''
    # Create tasks.txt if it doesn't exist
    task_list_local = [] # List to hold all tasks on file
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w", encoding="utf-8-sig"):
            pass
    try:
        # Open tasks.txt and read all tasks into task_data input list
        with open(TASK_FILE, 'r', encoding="utf-8-sig") as input_task_file:
            task_data_input = input_task_file.read().split("\n")
            # Removing any blank lines in the code
            task_data_input = [t for t in task_data_input if t != ""]
    except FileNotFoundError as file_error:
        print("Task file error", file_error)

    for t_str in task_data_input:
        curr_task = {}
        # Split by semicolon and add each component to dictionary
        task_components = t_str.split(";")
        curr_task['username'] = task_components[0]
        curr_task['title'] = task_components[1]
        curr_task['description'] = task_components[2]
        curr_task['due_date'] = datetime.strptime(task_components[3],
                                                  DATETIME_STRING_FORMAT)
        curr_task['assigned_date'] = datetime.strptime(task_components[4],
                                                       DATETIME_STRING_FORMAT)
        curr_task['completed'] = True if task_components[5] == "Yes" else False
        curr_task['task_id'] = task_components[6]
        # Add to task list
        task_list_local.append(curr_task)
    return task_data_input, input_task_file, task_list_local

def login():
    ''' This code reads usernames and password from the user.txt file to 
        allow a user to login also prompts user to register if required.
    '''
    # Outputs 10 blank lines
    print(CLEAR)
    # Set logged in to false as initial state
    logged_in = False
    # Welcome message
    print(f"\n\n{LINE}\n\t\tWELCOME TO THE TASK MANAGER APPLICATION\n{LINE}")
    while not logged_in:
        curr_user = input("Enter USERNAME or -1 to REGISTER or e to EXIT: ")
        # If there is no username then prompt user to register
        if curr_user == "-1":
            reg_user()
            break
        elif curr_user.lower() == "e":
            print("You have left the Task Manager program")
            exit()
        # Prompt user for password
        curr_pass = getpass("Enter Password: ")
        # If username does not exist prompt user again.
        if curr_user not in username_password:
            print("User does not exist")
            continue
        # If password does not match retry
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            # Assigns logged_in = True and returns current username
            print("Login Successful!")
            logged_in = True
            print(CLEAR)
            return curr_user
        break

def check_task_file_empty():
    ''' Checking if file has tasks if not then prompting user to add tasks'''
    with open(TASK_FILE, "r", encoding="utf-8-sig") as tasks_file:
        # Content variable reading from file
        content = tasks_file.read().strip()
        if not content:
            print("No tasks to generate report, please add tasks")
            return True
        else:
            return False

def reg_user():
    '''Add a new user to the user.txt file and check if username already 
    exists confirming password 
    '''
    print(LINE)
    # Request input of a new username
    new_username = input("Enter new username or -1 to return to login or menu: ").strip()
    # Prompt for input username
    while True:
        # Return to menu if reg_user called by mistake
        if new_username == "-1" and 'user' in globals():
            # Return to menu if already logged in
            return menu_options()
            # Return to login if not already logged in
        elif new_username == "-1":
            # Return to login
            return login()
        else:
            break
    while True:
        # If username already exists prompt user for another
        if new_username in username_password:
            new_username = input("Username already exists please enter another username: ")
        else:
            break
    # Request input of a new password which are blank
    new_password = getpass("Enter New Password and press return: ")
    # Request input of password confirmation.
    confirm_password = getpass("Confirm Password and press return: ")
    # Check if the new password and confirmed password are the same.
    while True:
        if new_password == confirm_password:
            # If password matches, add the username and password to the user.txt file,
            username_password[new_username] = new_password
            with open(USER_FILE, "a", encoding="utf-8-sig") as out_file:
                for new_username, new_password in username_password.items():
                    user_data.append(f"{new_username};{new_password}")
                    out_file.write(f"\n{new_username};{new_password}")
            # Otherwise present relevant message.
            print("New user added")
            out_file.close()
            break
        else:
            print("Passwords do not match")
            new_password = getpass("Enter New Password and press return: ")
            # Request input of password confirmation.
            confirm_password = getpass("Confirm Password and press return: ")
            continue
    return menu_options()

def menu_options():
    ''' Function to output menu options and obtain input from user'''
    print(LINE)
    menu_input = input("Select one of the following OPTIONS below: \n"
     "\t r  - Registering a user\n"
     "\t a  - Adding a task\n"
     "\t va - View all tasks\n"
     "\t vm - View my task\n"
     "\t gr - Generate reports\n"
     "\t ds - Display statistics (ADMIN Only)\n"
     "\t e  - Exit\n" ": ").lower()
    while True:
         # If invalid option input then ask user to input again
        if menu_input not in ('r','a','va','vm', "gr", 'ds', 'e'):
            menu_input = input("You did not enter a valid option please try again: ").lower()
        else:
            break
    # Execution of menu option functions
    if menu_input == "r":
        reg_user() # Register new user
    elif menu_input == "a":
        add_task() # Add a task
    elif menu_input == "va":
        view_all() # View all tasks
    elif menu_input == "vm":
        view_mine(user) # View current user tasks
    elif menu_input == "gr":
        generate_reports() # Generate reports
    elif menu_input == "ds":
        display_statistics() # Display statistics
    elif menu_input == "e":
        # Exit the task manager
        confirm_exit = input("To confirm exit enter Y or return to menu enter N: ").lower()
        while True:
            if confirm_exit == 'y':
                print("You are exiting the Task Manager program")
                exit()
            elif confirm_exit == 'n':
                return menu_options()
            else:
                confirm_exit = input("To confirm exit enter Y or return "\
                                     "to menu enter N").lower()

def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''
    print(LINE)
    print ("Please enter task details without semi-colons:")
    task_file_input()
    while True:
        # Prompt for input username
        task_username = input("Name of person assigned to task: ")
        # Check if username exists otherwise prompt for another username
        if task_username == "-1":
            return menu_options()
        elif task_username not in username_password:
            print("User does not exist. Please enter a valid username or enter -1 to exit: \n")
            continue
        # Obtain the title of the new task
        task_title = input("Title of Task: ")
        # Obtain the task description of new task
        task_description = input("Description of Task: ")
        # initializing unwanted_chars_list
        unwanted_chars = [';', ':', '[',']','{','}','(',')']
        # remove the unwanted characters from strings
        for i in unwanted_chars:
            task_username = task_username.replace(i, '')
            task_title = task_title.replace(i, '')
            task_description = task_description.replace(i, '')
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ").strip(';')
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        # Obtain the current date to calculate assigned date.
        curr_date = date.today()
        # task_id
        task_id = str(len(task_list) + 1)
        # Add the data to the file task.txt and
        # Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False,
            "task_id": task_id
        }
        # Append the new task to the task_list at the end
        task_list.append(new_task)
        # Overwrite tasks file with updated task_list
        output_task()
        break
    print(f"Task: {task_title} added successfully")
    return menu_options()

def output_task():
    ''' Output task_list to the tasks.txt file'''
    with open(TASK_FILE, "w", encoding="utf-8-sig") as task_file_add:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No",
                t['task_id']
                ]
            with open("tasks.txt", "w", encoding="utf-8-sig") as task_fle:
                task_list_to_write.append(";".join(str_attrs))
                task_fle.write("\n".join(task_list_to_write))
    task_file_add.close()

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing and labelling) 
    '''
    print(LINE)
    # All tasks in task list outputted to the screen
    for t in task_list:
        display_str = f"Task ID: \t {t['task_id']}\n"
        display_str += f"Task: \t\t {t['title']}\n"
        display_str += f"Assigned to: \t {t['username']}\n"
        display_str += f"Date Assigned: \t {t['assigned_date'].strftime('%d-%b-%Y')}\n"
        display_str += f"Due Date:  \t {t['due_date'].strftime('%d-%b-%Y')}\n"
        display_str += f"Task Complete: \t {t['completed']}\n"
        display_str += f"Task Description: \n {t['description']}\n"
        print(display_str, end="")
        print(LINE)
    return menu_options()

def view_mine(curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing and labelling) 
    '''
    print(LINE)
    user_task_count = 0
    for t in task_list:
        if t['username'] == curr_user:
            user_task_count += 1
            display_str = f"Task ID: \t {t['task_id']}\n"
            display_str += f"Task Title: \t {t['title']}\n"
            display_str += f"Assigned To: \t {t['username']}\n"
            display_str += f"Date Assigned: \t {t['assigned_date'].strftime('%d-%b-%Y')}\n"
            display_str += f"Due Date:   \t {t['due_date'].strftime('%d-%b-%Y')}\n"
            display_str += f"Task Complete: \t {t['completed']}\n"
            display_str += f"Task Description: \n {t['description']}\n"
            print(display_str, end="")
            print(LINE)
    # if there are no tasks assigned to the current user load menu options
    if user_task_count == 0:
        print(f"No task assigned to {user}, returning to main menu")
        return menu_options()
    task_number = input("Please input task id number you want to amend or -1 to quit: ")
    valid_task_number = [True for t in task_list if t['task_id'] == task_number]
    while True:
        # Check if valid task number
        if task_number != "-1" and valid_task_number:
            complete_edit = input("To edit press 1 or to mark as complete enter 2: ")
            if complete_edit == "1":
                # Match task number to be edited
                for t in task_list:
                    if t['task_id'] == task_number:
                        # User to choose what needs to be edited
                        edit_due_user = input("Do you want to edit Due Date or Username?\n"
                                        "Enter D for Due Date or U for Username: ").lower()
                        if edit_due_user == "d":
                            # Enter new due date and validating the input date
                            while True:
                                try:
                                    task_due_date = input("Enter new due date of task "
                                    "(YYYY-MM-DD) or -1 to return to menu: "
                                    ).strip(';')
                                    # If -1 return to menu
                                    if task_due_date == "-1":
                                        menu_options()
                                    t['due_date'] = datetime.strptime(task_due_date,
                                                    DATETIME_STRING_FORMAT)
                                    break
                                # Error handling for incorrect format of date
                                except ValueError as date_error:
                                    print("Invalid datetime format. Please use the "
                                          "format specified", date_error)
                        # If user wants to edit username
                        elif edit_due_user == "u":
                            new_username = input("Enter the new username or -1 for menu: ")
                            while True:
                                # Check if new username entered is username exists
                                if new_username in username_password:
                                    # Assign new username to task
                                    t['username'] = new_username
                                    break
                                elif new_username == "-1":
                                    return menu_options()
                                else:
                                    # Ask user to enter username again
                                    new_username = input("Enter the new username AGAIN: ")
                                    continue
            elif complete_edit == "2":
                # Change the task to complete
                for t in task_list:
                    if t['task_id'] == task_number:
                        t['completed'] = True
            print("Task has been amended")
            task_number = input("Please input task number you want to amend or -1 to quit: ")
            continue
        elif task_number == "-1":
            break
        else:
            task_number = input("Invalid task number please enter task number again: ")
            continue
    # Update tasks.txt with the new tasks
    output_task()
    return menu_options()

def generate_reports():
    '''Generate files for output reports TASK_OVERVIEW.txt and 
    USER_OVERVIEW.txt '''
    num_of_tasks = len(task_list)   # Number of tasks variable
    completed_tasks = 0             # Completed tasks variable
    overdue_tasks = 0               # Overdue task variable

    # Check if tasks.txt is empty if empty prompts user to add tasks
    if check_task_file_empty():
        print("Task file contains no tasks please add tasks")
        return menu_options()
    for t in task_list:
        if t['completed'] is True:
            completed_tasks += 1
        else:
            if t['due_date'] < datetime.now():
                overdue_tasks +=1
            else:
                continue
    # Task overview variables calculation rounding to 1 decimal place
    try:
        incomplete_tasks = num_of_tasks - completed_tasks
        percentage_incomplete = round((incomplete_tasks/num_of_tasks) * 100,1)
        percentage_overdue = round((overdue_tasks/num_of_tasks) * 100,1)
    except ZeroDivisionError as zero_division_error:
        print("Error: Cannot divide by zero.", zero_division_error)
    task_overview_str = ''
    user_no_task_str = ''
    with open(TASK_OVERVIEW, "w", encoding="utf-8-sig") as f:
        # Title of file
        task_overview_str ="\t\t TASK OVERVIEW FILE \n\n"
        # Output the calculated variables in the task overview file
        task_overview_str += "The total number of tasks which have been generated"
        task_overview_str += " and tracked by the task manager is "
        task_overview_str += str(num_of_tasks)+".\n\n"
        task_overview_str += "The total number of completed tasks is "
        task_overview_str += str(completed_tasks)+".\n\n"
        task_overview_str += "The total number of incomplete tasks is "
        task_overview_str += str(incomplete_tasks)+ ".\n\n"
        task_overview_str += "The total number of incomplete and overdue "
        task_overview_str += "tasks are " +str(overdue_tasks)+".\n\n"
        task_overview_str += "The percentage of tasks that are incomplete is "\
                             +str(round(percentage_incomplete,1))+"%.\n\n"
        task_overview_str += "The percentage of tasks that are overdue is "\
                             +str(round(percentage_overdue,1)) +"%."
        f.write(task_overview_str)
        # Close the file
    f.close()
    # user overview
    num_of_users = len(username_password)
    # Create the USER_OVERVIEW file and write the header details
    with open(USER_OVERVIEW, "w", encoding="+utf-8-sig") as user_overview_f:
        user_overview_str = ''
        # Title of file
        user_overview_str = "\t\t USER OVERVIEW FILE \n\n"
        # Output the calculated variables in the USER_OVERVIEW file
        user_overview_str += "The total number of users handled by the task manager is "
        user_overview_str += (str(num_of_users)+".\n\n")
        user_overview_str += "The total number of tasks which have been generated and "\
                              "tracked by the task manager is "+str(num_of_tasks)+".\n\n"\
                              "USER TASK SUMMARY (Only shows users with Tasks assigned)\n"
        user_overview_f.write(user_overview_str)
        user_overview_f.close()
    user_no_task_str = ''
    for u, username_task in enumerate (username_password):
        user_task_count = 0             # User task count variable
        user_task_completed = 0         # User task completed variable
        user_task_overdue = 0           # User task overdue variable
        for t in task_list:
            if t['username'] == username_task:
                # Count of tasks assigned to user
                user_task_count +=1
                if t['completed'] is True:
                    # Count of completed user tasks
                    user_task_completed +=1
                else:
                    # Count of overdue user tasks
                    if t['due_date'] < datetime.now():
                        user_task_overdue += 1
        # Create string listing usernames without a task assigned
        if user_task_count == 0:
            user_no_task_str += username_task + "\n"
            continue
        # User statistics calculations
        try:
            # User task percentage of all the tasks
            user_task_percent = (user_task_count/num_of_tasks) * 100
            # User completed task percentage out of all user tasks
            user_completed_percent = (user_task_completed/user_task_count) * 100
            # User incomplete task percentage out of all user tasks
            user_incomplete_percent = ((user_task_count - user_task_completed)\
                                       /user_task_count) * 100
            # User overdue task percentage out of all user tasks
            user_overdue_percent = (user_task_overdue/user_task_count) * 100
        except ZeroDivisionError as zero_division_error:
            print("Error: Cannot divide by zero.", zero_division_error)
        # Append to the USER_OVERVIEW file the calculated summary user values
        with open(USER_OVERVIEW, "a", encoding="+utf-8-sig") as user_overview_f:
            user_overview_str = LINE
            user_overview_str += ("\nUSERNAME: " +str(username_task)+"\n")
            user_overview_str += ("USER NUMBER: " +str(u + 1)+"\n")
            user_overview_str += ("USER TASK COUNT: "+str(user_task_count)+"\n")
            user_overview_str += ("OVERALL USER TASK PERCENTAGE: "
                                 +str(round(user_task_percent,1))+"\n")
            user_overview_str += ("USER COMPLETED TASK PERCENTAGE: "
                                 +str(round(user_completed_percent,1))+"\n")
            user_overview_str += ("USER OVERDUE TASKS PERCENTAGE: "
                                 +str(round(user_overdue_percent,1))+"\n")
            user_overview_str += ("USER INCOMPLETE TASKS PERCENTAGE: "
                                 +str(round(user_incomplete_percent,1))+"\n")
            user_overview_f.write(user_overview_str)
        user_overview_f.close()
    # Append the list of usernames without tasks assigned
    with open("USER_OVERVIEW.txt", "a", encoding="+utf-8-sig") as user_overview_f:
        user_overview_f.write("\nUSERS WITH NO TASKS ASSIGNED\n"+user_no_task_str)
    user_overview_f.close()
    print (f"\nThe report files {USER_OVERVIEW} and {TASK_OVERVIEW} have been generated!\n")
    return menu_options()

def display_statistics():
    ''' Display contents of user.txt and tasks.txt to screen'''
    # load user.txt file data into list
    user_data_screen = user_file_input()
    # load task.txt file data into dictionary after check if file is empty
    if check_task_file_empty():
        print("Task file does not contain any tasks please add tasks.")
        menu_options()
    task_file_input()
    # Checking if current user is admin if not return to main menu
    if user == "admin":
        # 2 options for user to output either tasks or user details
        try:
            while True:
                user_or_task = input ("Enter 1 for user details and 2 for"\
                                     " task details or to return to menu enter -1 :")
                if user_or_task not in ('-1','1','2'):
                    user_or_task = input ("Enter 1 for user details and 2 for"\
                                    " task details or to return to menu enter -1 :")
                else:
                    break
        except ValueError as user_or_task_error:
            print("User or task error", user_or_task_error)
        while True:
            # Output user details from text file
            if user_or_task == '1':
                print("\n")
                print("User Details from user.txt")
                for u in (user_data_screen):
                    print(LINE)
                    username, password = u.split(';')
                    print(f"Username: {username}")
                    print(f"Password: {password}")
                break
            elif user_or_task == '-1':
                menu_options()
            elif user_or_task == '2':
                # Checking if file has tasks if not then prompting user to add tasks
                with open("tasks.txt", "r", encoding="utf-8-sig") as tasks_file:
                    content = tasks_file.read().strip()
                    if not content:
                        print("No tasks to generate report, please add tasks")

                        return menu_options()
                # Output task details to screen
                print("Task Details from task.txt")
                for t in (task_list):
                    display_str = f"\nTask ID: \t {t['task_id']}\n"
                    display_str += f"Task: \t\t {t['title']}\n"
                    display_str += f"Assigned to: \t {t['username']}\n"
                    display_str += "Date Assigned: \t "
                    display_str += f"{t['assigned_date'].strftime('%d-%b-%Y')}\n"
                    display_str += f"Due Date:  \t {t['due_date'].strftime('%d-%b-%Y')}\n"
                    display_str += f"Task Complete: \t {t['completed']}\n"
                    display_str += f"Task Description: \n {t['description']}\n"
                    print(display_str, end="")
                    print(LINE)
                break
            else:
                user_or_task =input("Please enter 1 for User details" \
                                    "and 2 for Task details or -1 to return to menu.")
                continue
    else:
        print("\nYou cannot display statistics you are not ADMIN\n")
    return menu_options()
# Main program execution
try:
    # Loading user.txt file
    user_data = user_file_input()
    # Loading tasks.txt
    task_data, task_file, task_list = task_file_input()
    # Logging into Task Manager with valid username and password
    user = login()
    # Menu options for user to choose from
    menu_options()
except (ValueError, TypeError, IndexError, ZeroDivisionError, EOFError, NameError,
        OSError, UnicodeError, UnicodeTranslateError, KeyError, SyntaxError) as raised_error:
    print("Error in task_manager.py:\n", raised_error)
