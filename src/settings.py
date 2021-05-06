from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
import mysql.connector as mariadb
from global_variables import *
import re

@app.route('/settings', methods =['POST','GET'])
def settings():
    conn = mariadb.connect(host='sql11.freemysqlhosting.net', user='sql11402476', password='kS7DsFkJep', database='sql11402476')
    cur = conn.cursor(buffered = True)
    #id from global_varibles gotten from login
    id = str(user_id[0])
    #username from global_varibles gotten from login
    username= str(user_name[0]) 
    #select all data from user where id matches
    query = "SELECT * from sql11402476.users WHERE id ='" + id + "';"
    cur.execute(query)
    query = cur.fetchall()
    cur.close()
    conn.close()
    #return settings and display user`s information (id, full_name, email, phone_number)
    return render_template('common_files/settings.html', users = query)

@app.route('/settings_update', methods = ['POST'])
def settings_update():
    #empty dictonary to store information about the user
    date_user = {}
    username = str(user_name[0])
    id = str(user_id[0])
    counter = 0
    # site method for update form is POST
    if request.method == 'POST':
        if request.form.get('full_name'):
            #if user completed full_name field it will be added to dictonary
            date_user['full_name'] = request.form.get('full_name')
            counter +=1
        if request.form.get('username'):
            date_user['username'] = request.form.get('username')
            counter +=1
        else: 
            date_user['username'] = 0
        if request.form.get('phone_number') and check_phone(request.form.get('phone_number')):
            date_user['phone_number'] = request.form.get('phone_number')
            counter +=1
        elif not request.form.get('phone_number'):
            date_user['phone_number'] = 0
        else:
             flash("Invalid phone number")
        if request.form.get('email') and check_email(request.form.get('email')) :
            date_user['email'] = request.form.get('email')
            counter +=1
        elif not request.form.get('email'):
            date_user['email'] = 0
        else:
            flash("Not a valid email. Try again.")
        if request.form.get('password') and  request.form.get('new_password'):
            if request.form.get('password') == request.form.get('new_password'):
                date_user['password'] = request.form.get('password')
                counter +=1
            else:
                flash("Password doesn`t match")
        elif not request.form.get('password') and not request.form.get('new_password'):
            date_user['password'] = 0
        
    
    sql = "UPDATE sql11402476.users SET "
    # looping throught dictonary and create the query to find which dates must be updated
    for key, value in date_user.items():
        if value != 0:
            sql += key + "= " + "'" + value + "'" 
            sql += ","
    
    # remove the last character ", "
    sql = sql[:-1]
    #update from id user
    sql += " WHERE id = " + id + ";" 
    conn = mariadb.connect(host='sql11.freemysqlhosting.net', user='sql11402476', password='kS7DsFkJep', database='sql11402476')
    cur = conn.cursor(buffered = True)

    if counter!=0:
        cur.execute(sql)
        flash("Succesfully updated!")

    conn.commit()
    cur.close()
    conn.close()
    return settings()


def check_email(Email):
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if email_regex.match(Email):
      return True
    else:
      return False

def check_phone(phone_number):
    if re.search(r"^(\d{3}\d{3}\d{4})$", phone_number):
        return True
    else:
        return False