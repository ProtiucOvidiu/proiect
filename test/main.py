from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
# from passlib.hash import sha256_crypt
import mysql.connector as mariadb
import os
import operator
app = Flask(__name__, static_url_path="/static")
mariadb_connect = mariadb.connect(host='sql11.freemysqlhosting.net', user='sql11402476', password='kS7DsFkJep', database='sql11402476')
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
  cur = mariadb_connect.cursor(buffered=  True)
  data = cur.execute("SELECT username, email, password FROM users WHERE password= %s ", (passWord,))
  data = cur.fetchall()

  if not data:
    error = 'Credentials doesn`t exist! '
    return render_template('login.html')

  for i in data[:][0]:
    if i == Email or i == userName or i == passWord:
      check += 1

  if check != 2:
    error = 'Wrong password or email'
    flash(error)
    return render_template('login.html', error = error, username = userName, password = passWord)

  if cont:
    session['logged_in'] = True
  else:
    flash('error')
  return home()

# @app.route('/sign_up', methods=['POST']) 
# def do_admin_login():
#   login = request.form
 
#   full_name = login['full_name'] 
#   userName = login['username']
#   password = login['password']
#   email = login['email']
#   print('{}'.format(email))
#   print('{}'.format(full_name))


#   cur = mariadb_connect.cursor(buffered=True)
#   data = cur.execute('SELECT * FROM users WHERE username=\'ovi\'')
#   data = cur.fetchone()[1]

#   # if sha256_crypt.verify(password, data):
#   account = True

#   if account:
#     session['logged_in'] = True
#   else:
#     flash('wrong password!')
#   return home()


@app.route('/logout')
def logout():
  session['logged_in'] = False
  return home()

if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=True, host='0.0.0.0', port=5000)
