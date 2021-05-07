from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
import re

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

# set the user_name & user_id variable to a specific value
def set_user(id, username):
    global user_name, user_id
    user_id.insert(0, id)
    user_name.insert(0, username)

#==============================================================================#

# unset the user_name & user_id
def unset_user():
    global user_name, user_id
    user_id.pop(0)
    user_name.pop(0)

#==============================================================================#

def check_email(Email):
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if email_regex.match(Email):
      return True
    else:
      return False

#==============================================================================#

def check_phone(phone_number):
    if re.search(r"^(\d{3}\d{3}\d{4})$", phone_number):
        return True
    else:
        return False

#==============================================================================#