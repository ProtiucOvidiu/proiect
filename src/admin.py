from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
import mysql.connector as mariadb

from global_variables import *

#==============================================================================#

@app.route('/admin_home')
def admin_home_run():
    # list of queries
    queries = []
    # get all the pemission columns 
    queries.append("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS " 
    "where table_name = 'groups_perm_relation' "
    "order by ordinal_position;")

    # database connection 
    conn = mariadb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
        database=DB_DATABASE)
    try:
        cur = conn.cursor(buffered=True)
        # get all the group names
        cur.execute(queries[0])
        group_names = cur.fetchall()

        # create query to get the pemissions of the user
        queries.append("SELECT "
        "perm.name FROM permissions perm, "
        "(SELECT "+ temp_str(group_names, "gp") +" FROM user_groups_relation ug "
        "INNER JOIN users u ON u.id = ug.user_id "
        "INNER JOIN groups_perm_relation gp ON ug.group_id_1 = gp.group_id) temp "
        "where " + temp_str(group_names, "perm") + ";")

        # get all the permissions names for this user
        cur.execute(queries[1])
        permissions = cur.fetchall()   

        # close the connection
        cur.close()
        conn.close()
    except sqlite3.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    # return the page with all the data stored in the permissions variable
    return render_template('admin_files/admin_home.html', permissions = permissions)

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

@app.route('/admin_groups')
def admin_groups_run():
    # list of queries
    queries = []
    # get all the groups 
    queries.append("SELECT name FROM groups;")
    # create query to get the groups that the current user is a part of
    queries.append("SELECT g.name FROM groups g, (SELECT ug.group_id_1,"
    + "ug.group_id_2, ug.group_id_3 FROM user_groups_relation ug "
    + "INNER JOIN users u ON u.id = ug.user_id WHERE u.username = '" 
    + user_name[0] + "') result WHERE g.id = result.group_id_1" 
    + " OR g.id = result.group_id_2 OR g.id = result.group_id_3;")

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
    except sqlite3.Error as error:
            print("Failed to read data from table", error)
    finally:
        if (conn):
            conn.close()
            print('Connection to db was closed!')

    # create the dictionary with {name, yes/no} pairs
    groups = {}
    for group_row in admin_groups:
        if is_group_in_list(group_names, group_row[0]):
            groups[ group_row[0] ] = "Yes"
        else:
            groups[ group_row[0] ] = "No"

    # return the page with all the data stored in the groups variable
    return render_template('admin_files/admin_groups.html', groups = groups)

def is_group_in_list(group_names, group):
    # verify if a specific group name is in the list or not
    for group_row in group_names:
        if group == group_row[0]:
            return True
    return False

#==============================================================================#

@app.route('/admin_add')
def admin_add_run():
    return render_template('admin_files/admin_add.html')
    
#==============================================================================#

@app.route('/admin_modify')
def admin_modify_run():
    return render_template('admin_files/admin_modify.html')
    
#==============================================================================#

@app.route('/admin_delete')
def admin_delete_run():
    return render_template('admin_files/admin_delete.html')
    
#==============================================================================#

@app.route('/admin_msg')
def admin_msg_run():
    return render_template('admin_files/admin_msg.html')

#==============================================================================#

@app.route('/admin_forum')
def admin_forum_run():
    return render_template('admin_files/admin_forum.html')

#==============================================================================#

@app.route('/admin_settings', methods =['POST','GET'])
def admin_settings_run():
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
    except sqlite3.Error as error:
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
    except sqlite3.Error as error:
            print("Failed to read data from table", error)
    finally:
        if conn:
            conn.close()
            print('Connection to db was closed!')

    return admin_settings_run()

#==============================================================================#

@app.route('/admin_contact')
def admin_contact_run():
    return render_template('admin_files/admin_contact.html')

#==============================================================================#