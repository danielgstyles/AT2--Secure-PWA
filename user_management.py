import sqlite3 as sql
import time
import random
import bcrypt


def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    
    encodedPassword = password.encode('utf-8')

    hashedPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt())

    print("This the hashed password at submission: " + str(hashedPassword))
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hashedPassword, DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    bytePassword = bytes(password,"utf-8")
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    ##cur.execute("""SELECT * FROM users WHERE username = ? """, (username))
    query = "SELECT * FROM users WHERE username = ?"
    cur.execute(query, (username,))
    if cur.fetchone() == None:
        con.close()
        return False
    else:
        cur.execute(f"SELECT password FROM users WHERE username = '{username}'")
        hashedPassword = cur.fetchone()
##        hashedPassword = cur.fetchall()
        print("This the hashed password converted to a string for printing: " + str(hashedPassword))
##        hashedPassword = hashedPassword.replace("[(b'", "")
##        hashedPassword = hashedPassword.replace("',)]", "")

##        print("This the hashed password: " + hashedPassword)
##        hashedPassword = hashedPassword.encode("utf-8")

        
        #cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        
##        print(bcrypt.checkpw(password.encode(), hashedPassword.encode()))
        if bcrypt.checkpw(password.encode(), hashedPassword[0]):
            con.close()
            return True
        else:

            hashedEnteredPassword = bcrypt.hashpw(b"password", bcrypt.gensalt())
            print("This is the Hash of the password just entered: " + str(hashedEnteredPassword))
            print("This the Saved hashed password: " + str(hashedPassword))
            con.close()
            return False



def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
