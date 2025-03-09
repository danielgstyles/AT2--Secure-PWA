import sqlite3 as sql
import time
import random
import bcrypt

# User sign up to site. Eters their details into the SQL database
def insertUser(username, password, DoB):
    byte_Password = password.encode('utf-8')
    hash_Password = bcrypt.hashpw(byte_Password, bcrypt.gensalt())
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, hash_Password, DoB),
    )
    con.commit()
    con.close()

# Check if a user exists and checks their password is correct
def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cur.fetchone() == None: #this is checking the sql database if the username exists. if not it returns false back to Main.py
        con.close()
        return False
    else:
        cur.execute(f"SELECT password FROM users WHERE username = '{username}'")
        savedPassword = cur.fetchone()
        print(savedPassword)
##        cur.execute(f"SELECT * FROM users WHERE password = '{password}'")
        # Plain text log of visitor count as requested by Unsecure PWA management
        with open("visitor_log.txt", "r") as file:
            number = int(file.read().strip())
            number += 1
        with open("visitor_log.txt", "w") as file:
            file.write(str(number))
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        byte_Password = password.encode('utf-8')
        if bcrypt.checkpw(byte_Password, savedPassword[0]):
            con.close()
            return True
        else:
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
