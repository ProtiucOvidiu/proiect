from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
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

    return render_template('admin_files/admin_add_user.html')
    
#==============================================================================#

@app.route('/admin_modify', methods = ['POST', 'GET'])
def admin_modify_run():
    modify = request.form
    print('\n\n\n\n'+str(user_id[0])+'\n\n\n\n')
    query = ("SELECT distinct g.* FROM groups g "
        "INNER JOIN user_groups_relation ug ON ug.group_id = g.id "
        "WHERE ug.user_id = " + str(user_id[0]) + ";")
    query2 = (
        "SELECT distinct p.* FROM permissions p "
        "INNER JOIN groups_perm_relation gp ON gp.perm_id = p.id "
        "WHERE gp.group_id IN ( "
        "SELECT g.id FROM groups g "
        "INNER JOIN user_groups_relation ug ON ug.group_id = g.id "
        "WHERE ug.user_id = " + str(user_id[0]) + ");")
    query3 = "Select * from users;"
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()
    try:
        conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
        cur = conn.cursor(buffered = True)
        (groups, perm, users) = temp(query, query2, query3)
        if request.method == 'POST':
                if update_group(modify) != '':
                    cur.execute(update_group(modify))
                if update_permissions(modify) != '':
                    cur.execute(update_permissions(modify))
                conn.commit()
        elif request.method == 'GET':
            return render_template('admin_files/admin_modify.html', groups = groups, perm = perm, users = users)
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
    (groups, perm, users) = temp(query, query2, query3)
    return render_template('admin_files/admin_modify.html', groups = groups, perm = perm,  users = users)

# use this function to get groups and permission, without reloading the page
def temp(query, query2, query3):
    groups = ''
    permissions = ''
    users = ''
    try: 
        conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
        cur = conn.cursor(buffered = True)
        cur.execute(query)
        groups = cur.fetchall()
        cur.execute(query2)
        permissions = cur.fetchall()
        cur.execute(query3)
        users = cur.fetchall()
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
    return (groups, permissions, users)

# The actual function for update data in groups
def update_group(modify):
    update_query = ""
    if (modify.get('id') and modify.get('name')) or \
    (modify.get('id') and modify.get('description')): 
        update_query = "UPDATE groups"
        if modify.get('name') != '' and modify.get('description') != '':
            update_query += " SET name = \'" + modify['name'] + '\', description = \''\
            + modify['description'] + '\''
        if modify.get('description') == '':
            update_query += " SET name = \'" + modify['name'] + '\''
        if modify.get('name') == '':
            update_query += " SET description = \'" + modify['description'] + '\''
        update_query += " WHERE id = " + modify['id'] + ';'
    return update_query

# The actual function for update data in permissions
def update_permissions(modify):
    update_query = ""
    if (modify.get('id_perm') and modify.get('name_perm')) or \
    (modify.get('id_perm') and modify.get('desc_perm')): 
        update_query = "UPDATE permissions"
        if modify.get('name_perm') != '' and modify.get('desc_perm') != '':
            update_query += " SET name = \'" + modify['name_perm'] + '\', description = \''\
            + modify['desc_perm'] + '\''
        if modify.get('desc_perm') == '':
            update_query += " SET name = \'" + modify['name_perm'] + '\''
        if modify.get('name_perm') == '':
            update_query += " SET description = \'" + modify['desc_perm'] + '\''
        update_query += " WHERE id = " + modify['id_perm'] + ';'
    return update_query
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

@app.route('/delete_app')
def delete_app_run():
    # if the user is not logged in, redirect him/her to the login page
    is_logged_in()

    apps = []
    query = "SELECT * FROM apps ORDER BY id;"

    # database connection to get the apps
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered=True)

        # get all the permissions
        cur.execute(query)
        apps = cur.fetchall()

        # close the connection
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')

    return render_template('admin_files/admin_delete_app.html', apps = apps)

#==============================================================================#

@app.route('/delete_app_exec', methods=['POST'])
def execute_delete_app():
     # get the list of ids that the admin wants to delete
    delete = request.form.getlist('checks')

    ids_string = form_delete_id_string(delete)
    query = "DELETE FROM apps WHERE id IN " + ids_string
    
    # database connection to execute the query
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
            
    return redirect('/delete_app')

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

@app.route('/add_user')
def admin_add_user():
    query1 = "SELECT id, name FROM groups ORDER BY id;"
    query2 = "SELECT id, name FROM permissions;"

    # database connection 
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)
        cur.execute(query1)
        groups = cur.fetchall()
        cur.execute(query2)
        perms = cur.fetchall()
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    return render_template('admin_files/admin_add_user.html', groups = groups, perms = perms)

#==============================================================================#

@app.route('/submit_user', methods = ['GET','POST'])
def submit_user_form():
    #get the list of group/groups
    g = request.form.getlist('groups')
    #get the list of extra perms
    p = request.form.getlist('perms')
    l = []

    print('--------')
    print(g)
    print(p)
    if request.method == 'POST':
        full_name = str(request.form.get('first_name')) + " " + str(request.form.get('last_name'))
        l.append(full_name)
        if check_email(request.form.get('email')):
            l.append(request.form.get('email'))
        else:
            flash("Invalid email. Try again!")
        if check_phone(request.form.get('phone_number')):
            l.append(request.form.get('phone_number'))
        else:
            flash("Invalid phone number. Try again!")
        if request.form.get('password') == request.form.get('confirm_password'):
            l.append(sha256_crypt.hash(request.form.get('password')))
        else:
            flash('Password does not correspond. Try again!')
        if check_username(request.form.get('username')) == True:
            l.append(request.form.get('username'))
        else:
            flash("Username already exist!")
            return redirect('/add_user')

    print(l)
    print("==================")
    
    if len(l) == 5 and g:
        flash("Succesfully created user!")
    create_query(g, l)
    return redirect('/add_user')

#==============================================================================#
def create_query(groups, lista):
    query = ""
    user_name = str(lista[4])
    user_query = ( "INSERT INTO users (username, password, full_name, email, " 
    "phone_number, is_admin) VALUES ( '" + user_name + "' , '" + str(lista[3])
    + "', '" + str(lista[0]) + "', '" + str(lista[1]) + "', '" + str(lista[2]) + "', ")
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        user_id = "SELECT id FROM users WHERE username = '" + user_name + "' ;"
        cur = conn.cursor(buffered = True)

        if groups[0] == '1':
            user_query += "1);"
        else:
            user_query += "0);"
            
        print(user_query)
        cur.execute(user_query)
        conn.commit()

        cur.execute(user_id)
        user_id = str(cur.fetchone()[0])
        print(user_id)
        query = "INSERT INTO user_groups_relation (user_id, group_id) VALUES (" + str(user_id) + ", "
        queries = []
        
        for i in range(0, len(groups)):
            #query += str(groups[i]) + ");"
            #queries.append(query)
            #query = query[:-3]
            queries.append(query + str(groups[i])+ ");")

        for i in range(0,len(queries)):
            cur.execute(str(queries[i]))
            conn.commit()
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    return query

#==============================================================================#
def check_username(username):
    check = True
    user_query = "SELECT username FROM users;"
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)
        cur.execute(user_query)
        user_query = cur.fetchall()
        for i in user_query:
            if i[0] == username:
                check = False
                break
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')
    print(check)
    return check
#==============================================================================#

@app.route('/add_group', methods=['POST','GET'])
def admin_add_group():

    #print('\n\n\n\n'+str(user_id[0])+'\n\n\n\n')
    query = ("SELECT * from groups;")
    query2 = "SELECT id, username from users;"
    query3 = "SELECT id, name from permissions;"
    (groups, users, permissions)= query_for_user_groups_relation(query, query2, query3)
    #insert_groups()
    
    # insert into groups_perm_relation group id nou creat + perm id selectat
    return render_template('admin_files/admin_add_group.html', groups = groups, users = users, permissions = permissions)
#==============================================================================#
def query_for_user_groups_relation(query, query2, query3):
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)
        cur.execute(query)
        query = cur.fetchall()
        cur.execute(query2)
        query2 = cur.fetchall()
        cur.execute(query3)
        query3 = cur.fetchall()
        print(query3)
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')
    return (query, query2, query3)
#==============================================================================#
@app.route('/add_group_run', methods = ['POST'])
def insert_groups():
    add = request.form
    name = add.get('name')
    description = add.get('description')
    users = request.form.getlist('users')
    #print(users)
    #print(name, description)
    query = "INSERT INTO groups (name, description) VALUES ('" + str(name) + "', '" + str(description) + "');"
    query2 = "SELECT id from groups WHERE name = '" + str(name) +"';"
    #print(query)
    #print(query2)
    print("----------------")
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)
        cur.execute(query)
        conn.commit()
        cur.execute(query2)
        query2 = cur.fetchone()[0]
        print(query2)
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')
    insert_group_relation(query2, users)
    return redirect('/add_group')
#==============================================================================#
def insert_group_relation(query, users):
    query2 = "INSERT INTO user_groups_relation (group_id, user_id) VALUES (" + str(query) + ","
    queries = []
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)
        for i in range(0, len(users)):
            queries.append(query2 + str(users[i])+ ");")

        for i in range(0,len(queries)):
            cur.execute(str(queries[i]))
            conn.commit()
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')
    return redirect('/add_group_run')

#==============================================================================#

@app.route('/add_perms', methods = ['POST','GET'])
def admin_add_perms():
    query = "SELECT * from permissions;"
    groups = "SELECT * from groups;"
    apps = "SELECT id, name from apps"
    (query, groups, apps) = exec_query(query, groups, apps)
    return render_template('admin_files/admin_add_perm.html', perms = query, groups = groups, apps = apps)

def exec_query(query1, query2, query3):
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)
        cur.execute(query1)
        query1 = cur.fetchall()
        cur.execute(query2)
        query2 = cur.fetchall()
        cur.execute(query3)
        query3 = cur.fetchall()
        
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')
    return (query1, query2, query3)

@app.route('/add_perms_run', methods = ['POST'])
def insert_perms():
    add_perms = request.form
    name = add_perms.get('name')
    description = add_perms.get('description')
    id_apps = add_perms.getlist('apps')
    id_groups = add_perms.getlist('groups')
    perm_id = "SELECT id from permissions"
    print("{} {}".format(id_apps, id_groups))
    insert = "INSERT INTO permissions (name, description, app_id) VALUES ('" + str(name) + "', '" + str(description) + "', " 
    queries = []
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered = True)
        for i in range(0, len(id_apps)):
            queries.append(insert + str(int(id_apps[i]))+ ");")
        print(queries)
        for i in range(0,len(queries)):
            cur.execute(str(queries[i]))
            conn.commit()
        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    #group_id = id_groups
    # name = id
    insert_groups_perm_relation(id_groups, name)
    return redirect('/add_perms')

def insert_groups_perm_relation(group_id, name):
    print("-------------------")
    query = "INSERT INTO groups_perm_relation (perm_id, group_id) VALUES (" 
    query2 = "SELECT id from permissions WHERE name= '" + str(name) + "';"
    queries = []
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    
    try:
        cur = conn.cursor(buffered = True)
        cur.execute(query2)
        query2 = cur.fetchone()[0]
        query += str(query2) + ", "
        print(query2)
        for i in range(0, len(group_id)):
            queries.append(query + str(group_id[i])+ ");")
        #print(queries)
        for i in range(0,len(queries)):
            cur.execute(str(queries[i]))
            conn.commit()
            print(queries[i])

        cur.close()
        conn.close()
    except mariadb.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    print("---------------")

    return redirect('/add_perms_run')