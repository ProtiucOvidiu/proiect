from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for

app = Flask(__name__, static_url_path="/static", template_folder="templates")
user_name = []
user_id = []

def init():
    app = Flask(__name__, static_url_path="/static", template_folder="templates")

# set the user_name variable to a specific value
def set_user(id, username):
    global user_name, user_id
    user_id.append(id)
    user_name.append(username)