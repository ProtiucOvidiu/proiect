from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
import re
import mysql.connector as mariadb

#==============================================================================#

# the app variable used for app routing
app = Flask(__name__, static_url_path="/static", template_folder="templates")
user_name = [] # access it with user_name[0]
user_id = []

#==============================================================================#

# database login details
DB_HOST = 'sql11.freemysqlhosting.net'
DB_USER = 'sql11402476'
DB_PASSWORD = 'kS7DsFkJep'
DB_DATABASE = 'sql11402476'

#==============================================================================#

# must have function 
def init():
    app = Flask(__name__, static_url_path="/static", template_folder="templates")

#==============================================================================#
###
# set the user_name & user_id variable to a specific value
###
def set_user(id, username):
    global user_name, user_id
    user_id.insert(0, id)
    user_name.insert(0, username)

#==============================================================================#
###
# unset the user_name & user_id
###
def unset_user():
    global user_name, user_id
    user_id.pop(0)
    user_name.pop(0)

#==============================================================================#
###
# Check if Email has a valid format
###
def check_email(Email):
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if email_regex.match(Email):
      return True
    else:
      return False

#==============================================================================#
###
# Check if phone_number has a valid format
###
def check_phone(phone_number):
    if re.search(r"^(\d{3}\d{3}\d{4})$", phone_number):
        return True
    else:
        return False

#==============================================================================#
###
# Form the query used to load all the groups that a user is a part of
# if control = '=' creates the second part of the query, else creates
# the list of group_id_ columns separated by a comma
###
def create_group_query(control):

    # get all the group_id_ columns 
    query_1 = str("SELECT column_name FROM information_schema.columns where " 
    "table_name = 'user_groups_relation' order by ordinal_position;")

    # database connection 
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)

    try:
        cur = conn.cursor(buffered=True)
        # get all the group column names
        cur.execute(query_1)
        group_columns = cur.fetchall()
    except mariadb.Error as error:
        print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    query_2 = ""

    for i in range(0, len(group_columns) - 2):
        if control == "=":
            if i == len(group_columns) - 3:
                query_2 += f"g.id = result.group_id_{i + 1};"
                break
            else:
                query_2 += f"g.id = result.group_id_{i + 1} OR "
        else:
            if i == len(group_columns) - 3:
                query_2 += f"ug.group_id_{i + 1}"
                break
            else:
                query_2 += f"ug.group_id_{i + 1}, "

    return query_2    

#==============================================================================#
###
# Redirect the user to the login page if it's not logged in
###
def is_logged_in():
    # if the user is not logged in, redirect him/her to the login page
    if not session.get('logged_in'):
        return render_template('common_files/login.html')

#==============================================================================#
###
# Verify if a group name is in the list or not
###
def is_group_in_list(group_names, group):
    # verify if a specific group name is in the list or not
    for group_row in group_names:
        if group == group_row[0]:
            return True
    return False

#==============================================================================#
###
# Creates a string with the specified ids in the form of (1, 2, 3);
###
def form_delete_id_string(delete):
    # form the string 
    ids_string = "("
    for i in range(0, len(delete)):
        if i != len(delete) - 1:
            ids_string += delete[i] + ","
        else:
            ids_string += delete[i] + ");"
    return ids_string
#==============================================================================#
###
# Creates the query that deletes the id of a group from the user_groups_relation and replacing the row
# which contains the specific id
###
def create_delete_group_query(id):

    # get all the group_id_ columns 
    query_1 = str("SELECT column_name FROM information_schema.columns where " 
    "table_name = 'user_groups_relation' order by ordinal_position;")

    # database connection 
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)

    try:
        cur = conn.cursor(buffered=True)
        # get all the group column names
        cur.execute(query_1)
        group_columns = cur.fetchall()
    except mariadb.Error as error:
        print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    query_2 = ""
    for i in range(0, len(group_columns) - 2):
        
        if i == len(group_columns) - 3:
            query_2 += f"group_id_{i + 1} = " + id + ";"
            break
        else:
            query_2 += f"group_id_{i + 1} = " + id + " OR "

    return query_2

#==============================================================================#
###
# Creates a list separated by a comma of all the group_id_x columns from the 
# user_groups_relation table
###
def create_list_of_all_group_id_columns():
    # get all the group_id_ columns 
    query_1 = str("SELECT column_name FROM information_schema.columns where " 
    "table_name = 'user_groups_relation' order by ordinal_position;")

    # database connection 
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)

    try:
        cur = conn.cursor(buffered=True)
        # get all the group column names
        cur.execute(query_1)
        group_columns = cur.fetchall()
    except mariadb.Error as error:
        print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    groups = ""
    for i in range(2, len(group_columns) - 1):
        if i != len(group_columns) - 1:
            groups += str(group_columns[0][i]) + ","
        else:
            groups += str(group_columns[0][i])
    
    print(groups)

#==============================================================================#
###
# Creates a query to insert values back into the user_groups_relation without the 
# deleted group
###
def create_reinsert_query():
    query = "INSERT INTO user_groups_relation(user_id, "

#==============================================================================#


