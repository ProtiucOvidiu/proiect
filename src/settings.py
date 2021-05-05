from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
import mysql.connector as mariadb
from global_variables import *
import re

@app.route('/settings', methods =['POST','GET'])
def settings():
    conn = mariadb.connect(host='sql11.freemysqlhosting.net', user='sql11402476', password='kS7DsFkJep', database='sql11402476')
    cur = conn.cursor(buffered = True)
    id = str(user_id[0])
    username= str(user_name[0]) #username-ul primit global in momentul login-ului
    #query1= "SELECT id from sql11402476.users where username= '" + username +"';"
    #cur.execute(query1)
    #query1 = cur.fetchall()
    #query1 = str(query1)
    #for i in query1[0]:
    #    query1 = str(i)
    #print(query1)
    query = "SELECT * from sql11402476.users WHERE id ='" + id + "';"
    cur.execute(query)
    query = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('common_files/settings.html', users = query)

@app.route('/settings_update', methods = ['POST'])
def settings_update():
    date_user = {}
    username = str(user_name[0])
    id = str(user_id[0])
    counter = 0

    #query= "SELECT id from sql11402476.users where username= '" + username +"';"
    conn = mariadb.connect(host='sql11.freemysqlhosting.net', user='sql11402476', password='kS7DsFkJep', database='sql11402476')
    cur = conn.cursor(buffered = True)
    #cur.execute(query)
    #query = cur.fetchone()[0]

    if request.method == 'POST':
        if request.form.get('full_name'):
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
        
        #print('=========================')
        #print(date_user)
    
    sql = "UPDATE sql11402476.users SET "
    for key, value in date_user.items():
        if value != 0:
            sql += key + "= " + "'" + value + "'" 
            sql += ","
    
    sql = sql[:-1]
    #query = str(query)
    sql += " WHERE id = " + id + ";" #update dupa id user, nu dupa username, altfel nu merge
    #print(sql)
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