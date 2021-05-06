from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for

app = Flask(__name__, static_url_path="/static", template_folder="templates")
user_name = [] # access it with user_name[0]
user_id = []

# database login details
DB_HOST = 'sql11.freemysqlhosting.net'
DB_USER = 'sql11402476'
DB_PASSWORD = 'kS7DsFkJep'
DB_DATABASE = 'sql11402476'

def init():
    app = Flask(__name__, static_url_path="/static", template_folder="templates")

# set the user_name variable to a specific value
def set_user(id, username):
    global user_name, user_id
    user_id.append(id)
    user_name.append(username)