from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
# from passlib.hash import sha256_crypt
import mysql.connector as mariadb
import os
import operator
from sign_up import sign_up_pers
app = Flask(__name__, static_url_path="/static")
conn = mariadb.connect(host='127.0.0.1', user='root', password='cvscvs', database='test')
@app.route('/')
def home():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return render_template('index.html')

@app.route('/login', methods=['POST']) 
def do_admin_login():
  login = request.form
  passWord = login['password']
  Email = login['email-username']
  userName = login['email-username']
  cont = True
  check = 0
  cur = conn.cursor(buffered=  True)
  data = cur.execute("SELECT username, email, password FROM users WHERE password= %s ", (passWord,))
  data = cur.fetchall()
  if not data:
    error = 'Wrong password or email '
    flash(error)
    return render_template('login.html')

  for i in data[:][0]:
    if i == Email or i == userName or i == passWord:
      check += 1

  if check != 2:
    error = 'Wrong password or email'
    flash(error)
    return render_template('login.html', error = error, username = userName, password = passWord)

  cur.close()
  conn.close()
  if cont:
    session['logged_in'] = True
  else:
    flash('error')
  return home()

@app.route('/sign_up', methods=['POST', 'GET']) 
def do_admin_sign_up():
  cur = conn.cursor(buffered=True)
  request_sign = request.form
  full_name = request_sign['full_name'] 
  user_name = request_sign['user_name']
  email = request_sign['email']
  phone = request_sign['phone']
  password = request_sign['password']
  pass_conf = request_sign['confirm_password']

  sign_up_pers1 = sign_up_pers(full_name, user_name, email, phone, password, pass_conf)
  cur.execute(sign_up_pers1.select())
  users_rows = cur.fetchall()
  for row in users_rows:
      if user_name == row[0]:
        flash('Invalid User Name.')
        return render_template('sign_up.html')

  if not (sign_up_pers1.check_pass(pass_conf) and sign_up_pers1.check_email()):
    flash('Please check your sign up details and try again.')
    return render_template('sign_up.html')
  
  data = cur.execute(sign_up_pers1.insert())
  conn.commit()
  cur.close()
  conn.close()
  return render_template('login.html')

@app.route('/logout')
def logout():
  session['logged_in'] = False
  return home()

if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=True, host='0.0.0.0', port=5000)
