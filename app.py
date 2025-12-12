
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
import sqlite3
import random

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key="HelloRhys"
#configuration for the session

@app.route("/game")
def game():

    if "score" not in session:
        session["score"] = 0
        #sets up a score in the session if their isnt one already 

    conn = sqlite3.connect('fakeNewsUpdated.db')
    test = conn.execute('SELECT * FROM FakeNews').fetchall()
    conn.close()
    #connects to the database and queries it for what is needed

    newslist = random.choice(list(test))
    randomnews = newslist[1]
    trueorfalse = newslist[3]
    link = newslist[2]
    #filters out the list to get the data that is neccesary 

    return render_template("index.html", randomnews=randomnews, trueorfalse=trueorfalse, link=link, score=session["score"]) 
    #returns all the data to the html file to be used and displayed 

@app.route("/check_answer", methods=["POST"])
def check_answer():
    user_choice = request.json.get("choice")
    correct_answer = request.json.get("correct")
    #gets the answer the user chose and the answer that is correct

    is_correct = (user_choice == correct_answer)
    #variable so the program can decide if the users answer is correct or not 

    if is_correct:
        session["score"] += 1
        #if is correct is made then the user gets another score if not nothing happens

    return jsonify({
        "is_correct": is_correct,
        "score": session["score"]
    })
    #returns this to the JSON for the script to use 

@app.route("/api")
def api():
    conn = sqlite3.connect('fakeNewsUpdated.db')
    conn.row_factory =sqlite3.Row

    news=conn.execute("SELECT * FROM FakeNews").fetchall()
    return render_template("api.html",news=news)

@app.route("/apiaddnewsstories",methods=["POST"])
def addnewsJSON():
    if request.method=="POST":
        jsonreq=request.get_json()
        content=jsonreq.get('content')
        url=jsonreq.get('url','no url')
        realOrFake=jsonreq.get('realOrFake')
        conn = sqlite3.connect('fakeNewsUpdated.db')
        conn.row_factory =sqlite3.Row
        conn.execute('INSERT INTO FakeNews (content,url,realOrFake) VALUES (?,?,?)', (content, url, realOrFake))
        conn.commit()
        conn.close()
        return redirect(url_for('api'))

@app.route('/10news', methods=['GET'])
def top10scores():
    conn = sqlite3.connect('fakeNewsUpdated.db')
    conn.row_factory =sqlite3.Row

    newsvalues = conn.execute('SELECT content, url, realOrFake FROM FakeNews ORDER BY RANDOM() LIMIT 10').fetchall()
    conn.close()
    
    news_list = [dict(row) for row in newsvalues]
    
    return jsonify(news_list)

if __name__ == '__main__':
    app.run(debug=True)
#runs the flask app