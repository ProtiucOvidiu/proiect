from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for

from global_variables import app


@app.route('/admin_home')
def admin_home_run():
    return render_teplate('admin_files/admin_home.html')


@app.route('/admin_groups')
def admin_groups_run():
    return render_template('admin_files/admin_groups.html')


@app.route('/admin_add')
def admin_add_run():
    return render_template('admin_files/admin_add.html')
    

@app.route('/admin_modify')
def admin_modify_run():
    return render_template('admin_files/admin_modify.html')
    

@app.route('/admin_delete')
def admin_delete_run():
    return render_template('admin_files/admin_delete.html')
    

@app.route('/admin_msg')
def admin_msg_run():
    return render_template('admin_files/admin_msg.html')


@app.route('/admin_forum')
def admin_forum_run():
    return render_template('admin_files/admin_forum.html')
