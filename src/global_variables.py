from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for

app = Flask(__name__, static_url_path="/static", template_folder="templates")

def init():
    app = Flask(__name__, static_url_path="/static", template_folder="templates")