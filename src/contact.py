from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for

from global_variables import app

@app.route('/contact')
def contact():
    return render_template('common_files/contact.html')