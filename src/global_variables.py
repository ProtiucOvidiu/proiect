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
###
def create_group_query():

    # get all the pemission columns 
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
            query_2 += f"g.id = result.group_id_{i + 1};"
            break
        else:
            query_2 += f"g.id = result.group_id_{i + 1} OR "

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