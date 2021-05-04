from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, flash, url_for
import mysql.connector as mariadb

from global_variables import *

#=============================================================================#

@app.route('/admin_home')
def admin_home_run():
     # database connection to get the groups
    conn = mariadb.connect(host='sql11.freemysqlhosting.net', user='sql11402476', password='kS7DsFkJep', database='sql11402476')
    cur = conn.cursor(buffered=True)

    # list of queries
    queries = []
    # get all the pemission columns 
    queries.append("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS " 
    "where table_name = 'groups_perm_relation' "
    "order by ordinal_position;")

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

@app.route('/admin_groups')
def admin_groups_run():

     # database connection to get the groups
    conn = mariadb.connect(host='sql11.freemysqlhosting.net', user='sql11402476', 
           password='kS7DsFkJep', database='sql11402476')
    cur = conn.cursor(buffered=True)

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

    # get all the group names
    cur.execute(queries[0])
    group_names = cur.fetchall()

    # get all the group names for this user
    cur.execute(queries[1])
    admin_groups = cur.fetchall()        

    # close the connection
    cur.close()
    conn.close()

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

#=============================================================================#

@app.route('/admin_add')
def admin_add_run():
    return render_template('admin_files/admin_add.html')
    
#=============================================================================#

@app.route('/admin_modify')
def admin_modify_run():
    return render_template('admin_files/admin_modify.html')
    
#=============================================================================#

@app.route('/admin_delete')
def admin_delete_run():
    return render_template('admin_files/admin_delete.html')
    
#=============================================================================#

@app.route('/admin_msg')
def admin_msg_run():
    return render_template('admin_files/admin_msg.html')

#=============================================================================#

@app.route('/admin_forum')
def admin_forum_run():
    return render_template('admin_files/admin_forum.html')

#=============================================================================#