import sqlite3
from flask import session


def set_dict():
    global db_dict
    db_dict={}



def match_password(username):
    connection = sqlite3.connect('Database.db',check_same_thread = False)
    cursor =connection.cursor()
    cursor.execute(""" SELECT password FROM users WHERE username = '{username}' ORDER BY pk DESC;""".format(username = username))
    password = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return password

def signup(username,password,email):
    if(username == '' or password == '' or email == ''):
       return ('please fill all fields')
    connection = sqlite3.connect('Database.db',check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT password FROM users WHERE email = '{email}';""".format(email = email))
    exist = cursor.fetchone()

    if exist is None : # if there is no record of password regarding to emailaddress then it means that email address is unique
        cursor.execute(
        """ INSERT INTO users(
        username,
        password,
        email
        )VALUES(
        '{username}',
        '{password}',
        '{email}'
        );""".format(username = username ,password = password , email = email))
        connection.commit()
        cursor.close()
        connection.close()

    else:
       return('User with this email address already exists')

    return('you are signedup sucessfully and now go to home for login')


def insert_listName(name):
    if name != "":
        connection = sqlite3.connect('Database.db',check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute(""" INSERT INTO list(
         listName,
        UserId
        )VALUES(
        '{name}',
        (SELECT pk FROM users WHERE username = '{user}')
    );""".format(name=name,user = session['username'])
       )
        connection.commit()
        cursor.close()
        connection.close()

def insert_listItem(item,listname):
    if item != "" and listname != "":
        connection = sqlite3.connect('Database.db',check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO listTasks(
        taskName,
        listId
        )VALUES(
        '{item}',
         (SELECT listId FROM list WHERE listName = '{listname}')
    );""".format(item = item,listname = listname)
      
       )
        connection.commit()
        cursor.close()
        connection.close()

def delete_listItem(item,listname):
    if item != "" and listname != "":
        connection = sqlite3.connect('Database.db',check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM listTasks WHERE taskName = '{item}';""".format(item = item))
        connection.commit()
        cursor.close()
        connection.close()

def delete_listitemsAll(name):
      if name != "":
        connection = sqlite3.connect('Database.db',check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM listTasks WHERE listId = (SELECT listId FROM list WHERE listName = '{name}');""".format(name=name))
        connection.commit()
        cursor.close()
        connection.close()

def delete_list(name):
    delete_listitemsAll(name)
    if name != "":
        connection = sqlite3.connect('Database.db',check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM list WHERE listName = '{name}';""".format(name=name))
        connection.commit()
        cursor.close()
        connection.close()

def rename_list(oldName,newName):
    if oldName != "" and newName != "":
        connection = sqlite3.connect('Database.db',check_same_thread = False)
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE list SET listName ='{newName}' WHERE listName ='{oldName}';""".format(oldName = oldName , newName = newName))
        connection.commit()
        cursor.close()
        connection.close()

def get_listitems(temp_listname):
    temp_items=[]
    connection = sqlite3.connect('Database.db',check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT taskName FROM listTasks WHERE listId =( SELECT listId FROM list where listName = '{listname}');""".format(listname = temp_listname))
    db_items = cursor.fetchall()

    for i in range(len(db_items)):
        temp_items.append(db_items[i][0])
    
    db_dict[temp_listname] = temp_items

    

def get_list(username):
    
    connection = sqlite3.connect('Database.db',check_same_thread = False)
    cursor = connection.cursor()
    cursor.execute(""" SELECT listName FROM list WHERE UserId =( SELECT pk FROM users where username = '{username}');""".format(username = username))
    db_list = cursor.fetchall()
    set_dict()
    
    for i in range(len(db_list)):
        get_listitems(db_list[i][0])

    connection.commit()
    cursor.close()
    connection.close()
 
    return db_dict








        

