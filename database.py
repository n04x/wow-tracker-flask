import sqlite3

# ========================================================
# Function to run the query in the database and return rows.
# ========================================================
def runDatabase(query, edit_db):
    db_con = sqlite3.connect('bis.db')
    db_con.row_factory = sqlite3.Row
    db_cur = db_con.cursor()
    db_cur.execute(query[0], query[1])
    if not edit_db:
        return db_cur.fetchall()
    else:
        return None
        db_cur.execute(query[0])

# ========================================================
# Function to display the default BIS for each class 
# ========================================================    
def defaultBISDisplay(bis_class, bis_specialization):
    query = "SELECT * FROM BIS WHERE Class = ? AND Specialization = ?", (bis_class, bis_specialization)

    default_bis_list = runDatabase(query, False)

    return default_bis_list

# ========================================================
# Function to display the user BIS for each class
# It has the Obtained status for each item.
# ========================================================   
def userBISDisplay(bis_class, bis_specialization):
    item_bis_query = "SELECT * FROM BIS WHERE Class = ? AND Specialization = ?", (bis_class, bis_specialization)
    user_query = "SELECT * FROM USER_BIS WHERE Name = ?", ('Bob',)

    db_con = sqlite3.connect('bis.db')
    db_con.row_factory = sqlite3.Row
    db_cur = db_con.cursor()
   
    db_cur.execute(item_bis_query[0], item_bis_query[1])
    default_bis_list = db_cur.fetchall()

    db_cur.execute(user_query[0], user_query[1])
    user_bis_list = db_cur.fetchall()

    for i in default_bis_list:
        for u in user_bis_list:
            if i['ID'] == u['ID']:
                print('found a match! {}'.format(i['ID']))
                id_txt = i['ID']
                db_cur.execute("UPDATE BIS set Obtained = ? WHERE ID = ?", (1, id_txt))
                print('updated!')
                print(i['Obtained'])
    
    db_cur.execute(item_bis_query[0], item_bis_query[1])
    bis_obtained = db_cur.fetchall()

    return bis_obtained          
    