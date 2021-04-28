from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for

from global_variables import app


@app.route('/user_home')
def user_home_run():
    return render_template('user_files/user_home.html')


@app.route('/user_groups')
def user_groups_run():
    return render_template('user_files/user_groups.html')
    

@app.route('/user_msg')
def user_msg_run():
    return render_template('user_files/user_msg.html')


@app.route('/user_forum')
def user_forum_run():
    return render_template('user_files/user_forum.html')



