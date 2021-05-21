from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
import mysql.connector as mariadb

from global_variables import *

#==============================================================================#

@app.route('/user_home')
def user_home_run():  
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()
        
    # list of queries
    queries = []

     # create query to get the pemissions of the user
    queries.append(
        "SELECT p.name FROM permissions p "
        "INNER JOIN groups_perm_relation gp ON gp.perm_id = p.id "
        "WHERE gp.group_id IN ( "
        "SELECT g.id FROM groups g "
        "INNER JOIN user_groups_relation ug ON ug.group_id = g.id "
        "WHERE ug.user_id = " + str(user_id[0]) + ");")

    # database connection 
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered=True)       

        # get all the permissions names for this user
        cur.execute(queries[0])
        permissions = cur.fetchall()    

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    # return the page with all the data stored in the permissions variable
    return render_template('user_files/user_home.html', permissions = permissions)

def temp_str(group_names, abbreviation):
    temp = ""
    for i in range(0,len(group_names)-2):
        if abbreviation == "gp":
            if i == len(group_names)-3:
                temp += f"gp.perm_id_{i+1} "
            else:
                temp += f"gp.perm_id_{i+1}, "
        else:
            if i == len(group_names)-3:
                temp += f"temp.perm_id_{i+1} = perm.id "
            else:
                temp += f"temp.perm_id_{i+1} = perm.id or "
    
    return temp

#==============================================================================#

@app.route('/user_groups')
def user_groups_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    # list of queries
    queries = []
    # get all the groups 
    queries.append("SELECT name FROM groups;")
    # create query to get the groups that the current user is a part of
    queries.append(
        "SELECT g.id, g.name FROM groups g "
        "INNER JOIN user_groups_relation ug ON ug.group_id = g.id "
        "WHERE ug.user_id = " + str(user_id[0]) + ";")

    # database connection to get the groups
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered=True)

        # get all the group names
        cur.execute(queries[0])
        group_names = cur.fetchall()

        # get all the group names for this user
        cur.execute(queries[1])
        user_groups = cur.fetchall()        

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

   # return the page with all the data stored in the groups variable which is a
    # dictionary with {name, yes/no} pairs
    return render_template('user_files/user_groups.html', groups = create_group_dict(group_names, user_groups))

#==============================================================================#

@app.route('/user_msg')
def user_msg_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    return render_template('user_files/user_msg.html')

#==============================================================================#

@app.route('/user_forum')
def user_forum_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    return render_template('user_files/user_forum.html')

#==============================================================================#

@app.route('/user_settings', methods =['POST','GET'])
def user_settings_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    #id from global_varibles gotten from login
    id = str(user_id[0])
    #username from global_varibles gotten from login
    username= str(user_name[0]) 

    # database connection
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)

        #select all data from user where id matches
        query = "SELECT * from users WHERE id ='" + id + "';"
        cur.execute(query)
        query = cur.fetchall()
        cur.close()
        conn.close()

    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    #return settings and display user`s information (id, full_name, email, phone_number)
    return render_template('user_files/user_settings.html', users = query)

#==============================================================================#

@app.route('/user_settings_update', methods = ['POST'])
def user_settings_update():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

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
                date_user['password'] = sha256_crypt.hash(request.form.get('password'))
                counter +=1
            else:
                flash("Password doesn`t match")
        elif not request.form.get('password') and not request.form.get('new_password'):
            date_user['password'] = 0
        
    
    sql = "UPDATE users SET "
    # looping throught dictonary and create the query to find which dates must be updated
    for key, value in date_user.items():
        if value != 0:
            sql += key + "= " + "'" + value + "'" 
            sql += ","
    
    # remove the last character ", "
    sql = sql[:-1]
    #update from id user
    sql += " WHERE id = " + id + ";" 
    # database connection 
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)

        if counter!=0:
            cur.execute(sql)
            flash("Succesfully updated!")

        conn.commit()
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')
    return user_settings_run()

#==============================================================================#

@app.route('/user_contact')
def user_contact_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    return render_template('user_files/user_contact.html')

#==============================================================================#