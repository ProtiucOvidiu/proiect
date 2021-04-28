from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for

from global_variables import app

@app.route('/settings')
def settings():
    return render_template('common_files/settings.html')
    #return 'HELLO THERE!!!'