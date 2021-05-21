from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
import mysql.connector as mariadb
from passlib.hash import sha256_crypt
from global_variables import *

#==============================================================================#

@app.route('/admin_home')
def admin_home_run():
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
    return render_template('admin_files/admin_home.html', permissions = permissions)

#==============================================================================#

@app.route('/admin_groups')
def admin_groups_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    # list of queries
    queries = []
    # get all the groups 
    queries.append("SELECT name FROM groups;")
    # create query to get the groups that the current user is a part of
    queries.append(
        "SELECT g.name FROM groups g "
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
        admin_groups = cur.fetchall()        

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')

    # return the page with all the data stored in the groups variable which is a
    # dictionary with {name, yes/no} pairs
    groups = create_group_dict(group_names, admin_groups)
    #for key, value in groups.items():
    #    print(key + "-------" + value)
    return render_template('admin_files/admin_groups.html', groups = groups
        )

#==============================================================================#

@app.route('/admin_add')
def admin_add_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    return render_template('admin_files/admin_add.html')
    
#==============================================================================#

@app.route('/admin_modify')
def admin_modify_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    return render_template('admin_files/admin_modify.html')
    
#==============================================================================#

@app.route('/delete_user')
def delete_user_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    users = []
    query = ("SELECT id, username, full_name, email, phone_number, is_admin " 
        "FROM users ORDER BY id;")

    # database connection to get the groups
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)

    try:
        cur = conn.cursor(buffered=True)
        
        # get all the usernames and fullnames
        cur.execute(query)
        users = cur.fetchall()

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')
    
    return render_template('admin_files/admin_delete_user.html', users = users)
    
@app.route('/delete_user_exec', methods=['POST'])
def execute_delete_user():
    # get the list of ids that the admin wants to delete
    delete = request.form.getlist('checks')

    ids_string = form_delete_id_string(delete)    
    queries = []
    queries.append("DELETE FROM users WHERE id IN " + ids_string)

    # database connection to get the groups
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)

    try:
        cur = conn.cursor(buffered=True)
        
        # delete all the data related to the user/s
        cur.execute(queries[0])     
        conn.commit()

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')

    return redirect("/delete_user")
    

#==============================================================================#

@app.route('/delete_group')
def delete_group_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    groups = []
    query = "SELECT * FROM groups ORDER BY id;"

    # database connection to get the groups
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)

    try:
        cur = conn.cursor(buffered=True)
        
        # get all the groups
        cur.execute(query)
        groups = cur.fetchall()

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')

    return render_template('admin_files/admin_delete_group.html', groups = groups)

@app.route('/delete_group_exec', methods = ['POST'])
def execute_delete_group():
    # get the list of ids that the admin wants to delete
    delete = request.form.getlist('checks')

    ids_string = form_delete_id_string(delete)
    query = "DELETE FROM groups WHERE id IN " + ids_string + ";"
    
    # database connection to get the groups
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)

    try:
        cur = conn.cursor(buffered=True)

        # execute the query and commit the change
        cur.execute(query)
        conn.commit()

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')
    
    return redirect("/delete_group")

#==============================================================================#

@app.route('/delete_perm')
def delete_perm_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    perms = []
    query = "SELECT * FROM permissions ORDER BY id;"

    # database connection to get the groups
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered=True)

        # get all the permissions
        cur.execute(query)
        perms = cur.fetchall()

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')

    return render_template('admin_files/admin_delete_perm.html', perms = perms)

#==============================================================================#

@app.route('/delete_perm_exec', methods=['POST'])
def execute_delete_perm():
     # get the list of ids that the admin wants to delete
    delete = request.form.getlist('checks')

    ids_string = form_delete_id_string(delete)
    query = "DELETE FROM permissions WHERE id IN " + ids_string
    
    # database connection to get the groups
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)

    try:
        cur = conn.cursor(buffered=True)

        # execute the query and commit the change
        cur.execute(query)
        conn.commit()

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')
            
    return redirect('/delete_perm')

#==============================================================================#

@app.route('/admin_msg')
def admin_msg_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    return render_template('admin_files/admin_msg.html')

#==============================================================================#

@app.route('/admin_forum')
def admin_forum_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    return render_template('admin_files/admin_forum.html')

#==============================================================================#

@app.route('/admin_settings', methods =['POST','GET'])
def admin_settings_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    #id from global_varibles gotten from login
    id = str(user_id[0])
    #username from global_varibles gotten from login
    username= str(user_name[0]) 
    #select all data from user where id matches
    query = "SELECT * from users WHERE id ='" + id + "';"

    # database connection 
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)
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
    return render_template('admin_files/admin_settings.html', users = query)

#==============================================================================#

@app.route('/admin_settings_update', methods = ['POST'])
def admin_settings_update():
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

    return redirect("/admin_settings")

#==============================================================================#

@app.route('/admin_contact')
def admin_contact_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()
    
    return render_template('admin_files/admin_contact.html')

#==============================================================================#