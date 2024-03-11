# This is a Task Manager app that assists businesses in allocating tasks for employees and has tools to manage the workplace and tasks that have been allocated.
# admin can see reports and register users.
# Use 'admin, admin1' to enter.

import re
import contextlib

import calendar
from datetime import date, datetime
current_dateTime = date.today().strftime('%d %b %Y')
today = datetime.today()

# Load tasks from tasks.txt file
def load_tasks():
    with open("tasks.txt", "r") as tasks_file:
        tasks = [line.strip().split(", ") for line in tasks_file]
    return tasks

# Load users from user.txt file
def load_users():
    with open("user.txt", "r") as user_file:
        users = {}
        for line in user_file:
            username, password = line.strip().split(", ")
            users[username] = password
    return users

# Updating to file
def update_task_file(filename, file_lines):
    with open(filename, "w") as file:
        for i, task in enumerate(file_lines):
            file.write(", ".join(map(str, task)))
            if i < len(file_lines) - 1:
                file.write("\n")

# Validating users due date
def valid_due_date(current_date_time):
    valid_date = False
    while not valid_date:
        task_due_date = input(f"Due date for task completion (current date: {current_date_time} (DD MMM YYYY): ")
        if re.match(r"^\d{2} [a-zA-Z]{3} \d{4}$", task_due_date): # checking if date input is the correct format
            day, month, year = task_due_date.split(" ")
            month = month.capitalize()
            task_due_date_str = f"{day} {month} {year}"
            try:
                task_due_date = date(int(year), list(calendar.month_abbr).index(month), int(day))
                task_due_date = datetime.strptime(task_due_date_str, "%d %b %Y")
                today = datetime.today()
                if task_due_date.date() >= today.date():
                    valid_date = True
                else:
                    print("Due date is before today, please add a due date from today onwards")
            except ValueError:
                print("Invalid date format.")
        else:
            print("Invalid date format.")   
    return task_due_date.strftime("%d %b %Y")


# Login authorization
def login():
    print("Task Manager\n")
    print("Please login\n")

    users = load_users()
    while True:
        user_login = input("Enter your username: ")
        password_login = input("Enter your password: ")
        if user_login in users and users[user_login] == password_login:
            print("\nYou have successfully logged in.")
            return user_login
        print("Invalid username or password.")

# Register user - Adding new users to task manager
def register_user():
    if current_user == "admin":
        users = load_users()
        while True:
            new_user = input("Enter the new user's name: ")
            if new_user not in users:
                new_user_password = input("Enter the new user's password: ")

                password_double_check = ""
                while new_user_password != password_double_check:
                    password_double_check = input("Re-enter the new password to confirm: ")
                    if password_double_check != new_user_password:
                        print("Passwords do not match.")

                else:
                    with open('user.txt', 'a') as user_file:
                        user_file.write(f"\n{new_user}, {new_user_password}")
                    print(f"\nPasswords match, and the new user '{new_user}' has been registered successfully.")
                    return
            else:
                print(f"Username '{new_user}' already exists. Please choose a different name.")
    else:
        print("\nOnly admin can register new users.")


# Adding new tasks to users
def add_task():
    tasks = load_tasks()
    users = load_users()

    while True:
        task_assigned_user = input("Which user will be assigned to the task: ")
        if task_assigned_user in users:
            task_title = input("Enter a title for the task: ")
            task_description = input("Enter a description of the task: ")      
            task_due_date_str = valid_due_date(current_dateTime) # using due date function to check format of due date entered
            task_completed = "No"
            task_data = [task_assigned_user, task_title, task_description, current_dateTime, task_due_date_str, task_completed]
            tasks.append(task_data)
            print(f"""\nTask assigned to user '{task_assigned_user}' has been added successfully as follows:

Assigned user:       {task_assigned_user}
Task title:          {task_title}
Task description:    {task_description}
Task due date:       {task_due_date_str}
Date assigned:       {current_dateTime}""")
            break
        else:
            print("Invalid username. Please use a registered username or contact admin to create a new user.")

    with open('tasks.txt', 'a') as tasks_file:
        tasks_file.write(f"\n{task_assigned_user}, {task_title}, {task_description}, {current_dateTime}, {task_due_date_str}, No")


# View all users tasks
def view_all():
    print("All tasks:")

    tasks = load_tasks()
    for task in tasks:
        
        print(f"""
Task:               {task[1]}
Assigned to:        {task[0]}
Date Assigned:      {task[3]}
Due Date:           {task[4]}
Task Complete?      {task[5]}
Task Description:   {task[2]}""")


# View current users tasks
def view_mine():
    tasks = load_tasks()
    print(f"{current_user}'s tasks:")

    user_tasks = []
    user_task_number = 1

    for task_number, task in enumerate(tasks, 1):
        Tab_user, Tab_task, Tab_description, Tab_assigned_date, Tab_due_date, task_complete = task
        task_complete = task_complete.replace("\n", "")

        if current_user == Tab_user:
            user_tasks.append((user_task_number, task)) 
            user_task_number += 1

    if not user_tasks:
        print("No tasks found for the current user.")
        return

    for task_number, task in user_tasks:
        Tab_user, Tab_task, Tab_description, Tab_assigned_date, Tab_due_date, task_complete = task
        printed_tasks = f"""
Task number:        {task_number}
Task:               {Tab_task}
Assigned to:        {Tab_user}
Date Assigned:      {Tab_assigned_date}
Due Date:           {Tab_due_date}
Task Complete:      {task_complete}
Task Description:   {Tab_description}"""
        print(printed_tasks)

    user_task_selection = None
    go_back_to_menu = False

    while user_task_selection != -2: # using -2 for indexing purposes
        try:
            user_task_selection = int(input("""
Would you like to view a specific task or return to the main menu?

- Input task number to view task
- Input '-1' to return to the menu
: """)) - 1
            
            if user_task_selection == -2:
                continue

            if user_task_selection <= -1 or user_task_selection >= len(user_tasks):
                print("Task not found")
                continue

            task_number, task = user_tasks[user_task_selection]
            Tab_user, Tab_task, Tab_description, Tab_assigned_date, Tab_due_date, task_complete = task

            printed_tasks = f"""
Task number:        {task_number}
Task:               {Tab_task}
Assigned to:        {Tab_user}
Date Assigned:      {Tab_assigned_date}
Due Date:           {Tab_due_date}
Task Complete:      {task_complete}
Task Description:   {Tab_description}"""
            print(printed_tasks)

            edit_task_selection = ""
            while edit_task_selection not in ("r", "m", "ed") and not go_back_to_menu:
                edit_task_selection = input("""
Would you like to mark the task complete, edit the task, or return to the main menu?

- Input 'm' to mark the task complete
- Input 'ed' to edit the task's username or due date
- Input 'r' to return to the menu
: """).lower()

                if edit_task_selection == "m":
                    if task_complete == "No":
                        task_complete = "Yes"
                        print(f"Task {task_number} has been marked as complete")
                        task[5] = "Yes"
                        update_task_file("tasks.txt", tasks) #using update task function as using it repeatedly
                    else:
                        print("Task is already marked as complete")

                elif edit_task_selection == "ed":
                    if task_complete == "No":

                        user_choice = ""
                        while user_choice != "no" and user_choice != "yes":
                            user_choice = input("Would you like to update the username? (yes/no): ").lower()

                            if user_choice == "yes":
                                usernames = set([line[0] for line in tasks])
                                edited_username = ""
                                while edited_username not in usernames:
                                    edited_username = input("Please enter the new username: ")
                                    if edited_username in usernames:
                                        print(f"\nTask has been updated and assigned to {edited_username}")
                                        Tab_user = edited_username
                                        task[0] = Tab_user

                                        user_choice = ""
                                        while user_choice != "no" and user_choice != "yes":
                                            user_choice = input("Would you like to update the due date? (yes/no): ").lower()
                                            if user_choice == "yes":
                                                edited_due_date = valid_due_date(current_dateTime) #valid due date function
                                                print(f"\nCurrent due date {Tab_due_date} has been updated to {edited_due_date}")
                                                Tab_due_date = edited_due_date
                                                task[4] = Tab_due_date
                                                go_back_to_menu = True
                                                update_task_file("tasks.txt", tasks)
                
                                            elif user_choice == "no":
                                                print(f"Due date {Tab_due_date} has not been updated.")
                                                go_back_to_menu = True
                                                update_task_file("tasks.txt", tasks)
                                            else:
                                                print("\nYou have input an incorrect option. Please input yes or no.\n")
                                    else:
                                        print(f"\nUsername {edited_username} does not exist, please assign a registered user or contact admin to create a new registered user.")

                            elif user_choice == "no":
                                print(f"Username {Tab_user} has not been updated.")
                                user_choice = ""
                                while user_choice != "no" and user_choice != "yes":
                                    user_choice = input("Would you like to update the due date? (yes/no): ").lower()
                                    if user_choice == "yes":
                                        edited_due_date = valid_due_date(current_dateTime) #valid due date function
                                        print(f"\nCurrent due date {Tab_due_date} has been updated to {edited_due_date}")
                                        Tab_due_date = edited_due_date
                                        task[4] = Tab_due_date
                                        update_task_file("tasks.txt", tasks)
                                        go_back_to_menu = True

                                    elif user_choice == "no":
                                        print(f"Due date {Tab_due_date} has not been updated.")
                                        go_back_to_menu = True
                                    else:
                                        print("\nYou have input an incorrect option. Please input yes or no.\n")
                            else:
                                print("\nYou have input an incorrect option. Please input yes or no.\n")
                    else:
                        print("Task is already complete")

                elif edit_task_selection != "r":
                    print("\nYou have input an incorrect option. Please input an option from the menu.")

            if go_back_to_menu:
                break

        except ValueError:
            print("Invalid input. Please enter a valid task number or '-1' to return to the menu.")


#To generate reports from tasks.txt and users.txt
def generate_reports():
    if current_user == 'admin':
        user_overview_report = ""
        task_overview_report = ""

        total_tasks = 0
        total_completed_tasks = 0
        total_uncompleted_tasks = 0
        uncomplete_and_overdue = 0

        with open("tasks.txt", "r") as tasks_file:
            for line in tasks_file:
                tab_user = line.split(', ')[0]
                tasks_complete = line.split(', ')[5].replace("\n", "").lower()
                tab_due_date = line.split(', ')[4]
                due_date = datetime.strptime(tab_due_date, '%d %b %Y')

                total_tasks += 1
                if tasks_complete == "yes":
                    total_completed_tasks += 1
                elif tasks_complete == "no":
                    total_uncompleted_tasks += 1

                    if due_date < today:
                        uncomplete_and_overdue += 1

            uncomplete_percentage = int(round((total_uncompleted_tasks / total_tasks) * 100))
            overdue_percentage = int(round((uncomplete_and_overdue / total_tasks) * 100))


            task_overview_report = f"""
Total tasks:                        {total_tasks}
Total completed tasks:              {total_completed_tasks}
Total incomplete tasks:             {total_uncompleted_tasks}
Total incomplete & overdue tasks:   {uncomplete_and_overdue}
Tasks incomplete                    {uncomplete_percentage}%
Tasks overdue                       {overdue_percentage}%"""

        with open('task_overview.txt', 'w') as task_overview_file:
            task_overview_file.write("Task overview report:\n" + task_overview_report)

        total_users = 0

        with open("user.txt", "r") as user_file:
            for user_line in user_file:
                total_users += 1

                user_tab_user = user_line.split(', ')[0]

                user_total_tasks = 0
                user_completed_tasks = 0
                user_uncompleted_tasks = 0
                user_overdue_tasks = 0

                with open("tasks.txt", "r") as tasks_file:
                    for task_line in tasks_file:
                        tab_user = task_line.split(', ')[0]
                        tasks_complete = task_line.split(', ')[5].replace("\n", "").lower()
                        tab_due_date = task_line.split(', ')[4]
                        due_date = datetime.strptime(tab_due_date, '%d %b %Y')

                        if user_tab_user == tab_user:
                            user_total_tasks += 1
                            if tasks_complete == "yes":
                                user_completed_tasks += 1
                            elif tasks_complete == "no":
                                user_uncompleted_tasks += 1
                                if due_date < today:
                                    user_overdue_tasks += 1

                if total_tasks > 0:
                    user_total_task_percentage = int(round(user_total_tasks / total_tasks * 100))
                else:
                    user_total_task_percentage = 0

                if user_total_tasks > 0:
                    completed_user_tasks_percentage = int(round(user_completed_tasks / user_total_tasks * 100))
                    uncompleted_user_tasks_percentage = int(round(user_uncompleted_tasks / user_total_tasks * 100))
                    user_overdue_percentage = int(round(user_overdue_tasks / user_total_tasks * 100))
                else:
                    completed_user_tasks_percentage = 0
                    uncompleted_user_tasks_percentage = 0
                    user_overdue_percentage = 0

                user_overview_report += f"""
\nUser:                                       {user_tab_user}
Total user tasks:                           {user_total_tasks}
Percentage of total tasks:                  {user_total_task_percentage}%    
Percentage of completed tasks:              {completed_user_tasks_percentage}%
Percentage of incomplete tasks:             {uncompleted_user_tasks_percentage}%
Percentage of overdue & incomplete tasks:   {user_overdue_percentage}%"""

            with open('user_overview.txt', 'w') as user_overview_file:
                user_overview_file.write(f"""User overview report:

Total users registered: {total_users}
Total tasks generated:  {total_tasks}
{user_overview_report}""")

                print("task overview report and user overview report have been generated")

    else:
        print("Invalid menu option")


# displaying Statistics 
def display_statistics():
    if current_user == 'admin':

        with contextlib.redirect_stdout(None): #prevents the print statement from generate_reports to show
            generate_reports()
        
        report_selction = ""

        while report_selction != "e":
            report_selction = input("""\nEnter in the report you would like to view or exit to main menu:
Task overview report:   "t"
User overview report:   "u"
exit to main menu:      "e"
> """).lower()
            
            if report_selction == "t":

                with open('task_overview.txt', "r") as f:
                    for line in f:
                        print(line.strip())

            elif report_selction == "u":

                with open('user_overview.txt', "r") as f:
                    for line in f:
                        print(line.strip())
            elif report_selction == "e":
                break
            else:
                print("Menu option not invalid")
    else:
        print("Invalid menu option")


# Prompt user for login
current_user = login()

# Display menu and prompt for action
while True:
    menu_options = """
r   - Register a user
a   - Adding a task
va  - View all tasks
vm  - View my tasks"""

    if current_user == "admin":
        menu_options += """
gr  - Generate reports
ds  - Display Statistics"""

    menu_options += '''
e   - Exit'''

    print(menu_options)
    
    choice = input("\nSelect one of the menu options: ").lower()

    if choice == "r":
        register_user()
    elif choice == "a":
        add_task()
    elif choice == "va":
        view_all()
    elif choice == "vm":
        view_mine()
    elif choice == "ds":
        display_statistics()
    elif choice == "gr":
        generate_reports()
    elif choice == "e":
        print("Exiting the Task Manager. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")