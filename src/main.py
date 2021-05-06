from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
from passlib.hash import sha256_crypt
import mysql.connector as mariadb
import os
import operator
import re
from sign_up import sign_up_pers
from global_variables import *
import user, admin, settings, contact

@app.route('/')
def home():
  if not session.get('logged_in'):
    return render_template('common_files/login.html')
  else:
    # connection to the db
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
          database=DB_DATABASE)
    cur = conn.cursor(buffered = True)

    # get the id of the first group for this user which represents the
    # admins' group
    query = "SELECT group_id_1 FROM user_groups_relation WHERE user_id = "
    + data[0][0] + ";"
    cur.execute(query)
    is_admin = cur.fetchall()
    return user.user_home_run()
    
def check_email(Email):
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if email_regex.match(Email):
      return True
    else:
      return False

@app.route('/login', methods=['POST','GET']) 
def do_admin_login():
  conn = mariadb.connect(host='sql11.freemysqlhosting.net', user='sql11402476', password='kS7DsFkJep', database='sql11402476')
  login = request.form
  password = login['password']
  email = login['email-username']
  username = login['email-username']

  check = 0
  conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
  cur = conn.cursor(buffered = True)
  if check_email(email):
    data = cur.execute("SELECT id, username, email, password FROM users WHERE email= %s ", (email,))  #check dupa username sau email
  else:
    data = cur.execute("SELECT id, username, email, password FROM users WHERE username= %s ", (username,))

  data = cur.fetchall()

 

  # close the connection
  cur.close()
  conn.close()

  # if the sign up button was pressed
  if login.get('sign_up'):
    return render_template('common_files/sign_up.html')

  # if there is no data from db aka there is no user stored in db with that
  # username or email  
  if not data:
    error = 'Invalid credentials'
    flash(error)
    return render_template('common_files/login.html')

  # check the username/email if it matches with the one stored
  for i in data[:][0]:
    if i == email or i == username:
      check += 1
  
  # verify if the hash matches the string from the form 
  if sha256_crypt.verify(password, data[0][2]):
    check += 1

  if check != 2:
    error = 'Wrong password or email'
    flash(error)
    return render_template('common_files/login.html', error = error)

  # if it reaches this code than it means that all the login details are 
  # correct
  session['logged_in'] = True
    
  # save the username in a global variable so that you can access it from other scripts
  set_user(data[0][0], data[0][1])

  # return the appropriate page
  return home()

@app.route('/sign_up', methods=['POST', 'GET']) 
def do_admin_sign_up():
  conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
  cur = conn.cursor(buffered=True)
  request_sign = request.form
  full_name = request_sign['full_name'] 
  user_name = request_sign['user_name']
  email = request_sign['email']
  phone = request_sign['phone']
  password = request_sign['password']
  pass_conf = request_sign['confirm_password']

  if request_sign.get('login'):
    return render_template('common_files/login.html')
  
  sign_up_pers1 = sign_up_pers(full_name, user_name, email, phone, password, pass_conf)
  cur.execute(sign_up_pers1.select())
  users_rows = cur.fetchall()
  for row in users_rows:
      if user_name == row[0]:
        flash('Invalid User Name.')
        return render_template('common_files/sign_up.html')

  if not (sign_up_pers1.check_pass(pass_conf) and sign_up_pers1.check_email()):
    flash('Please check your sign up details and try again.')
    return render_template('common_files/sign_up.html')

  pass_hash = sha256_crypt.hash(password)
  
  cur.execute(sign_up_pers1.insert(pass_hash))
  conn.commit()
  cur.close()
  conn.close()
  return render_template('common_files/login.html')

@app.route('/logout')
def logout():
  session['logged_in'] = False
  return home()

if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=True, host='0.0.0.0', port=5000)
