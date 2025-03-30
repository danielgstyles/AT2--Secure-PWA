from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import user_management as dbHandler
import html

from flask import session                           #race condition prevention


# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.secret_key = "dfjkasjdfljadfklja;dfkj;akdslf"   #race condition prevention

@app.route("/success.html", methods=["POST", "GET"])
def addFeedback():
        
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    
    if request.method == "GET": # this entire if and nested if is for race condition prevention. This use to be somewhat delt with the last else of the function
        if "user" in session:
            dbHandler.listFeedback()
            user = session["user"]
            return render_template("/success.html", state=True, value=user)
        else:
            return render_template("/index.html")       #down to here
        
    if request.method == "POST":
        feedback = request.form["feedback"]
        sanitised_feedback = html.escape(feedback)
        username = session["user"]                              # this get the username from the session and places it in the variable username
        dbHandler.insertFeedback(sanitised_feedback, username)  #Added username to the call to add the username to each entry of 
                                                                #feedback for login. need to add new field to feedback database for this to work
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="FeedBack")
    #else:

@app.route("/signup.html", methods=["POST", "GET"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["user"] = username  #race condition prevention (Activates the session). To close a session the browswer need to be closed to disconnected
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html", is_done=True)
    else:
        return render_template("/index.html")


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
