# import necessary modules
import os
import sys
from random import randint

import pymongo
from dotenv import load_dotenv

from flask import Flask, redirect, request, render_template
# from pymongo import MongoClient

load_dotenv()
CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")

DB_NAME = "feedbackbank"
COLLECTION_NAME = "feedbacks"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client[DB_NAME]



# define the flask app
app = Flask(__name__)


# home page route
@app.route('/', methods=["GET"])
def index():
    all_feedback = [fb for fb in db.feedbackbank.find({},{"_id": 0, "Feedback": 1})]
    if all_feedback:
        random_feedback = all_feedback[randint(0, len(all_feedback)-1)].get("Feedback")
    else:
        random_feedback = None
    
    return render_template("index.html", random_feedback=random_feedback)

# submission
@app.route('/submit', methods=["POST"])
def submit():
    data = {}
    data['Feedback'] = request.form['feedback']        
    db.feedbackbank.insert_one(data) 

    return redirect("/")


# route to get data from html form and insert data into database
# @app.route('/data', methods=["GET", "POST"])
# def data():
#     data = {}
#     if request.method == "POST":
#         data['Name'] = request.form['name']        
#         db.feedbackbank.insert_one(data)

    
       

#     return render_template("index.html")




#Get one random document from the mycoll collection.
#db.feedbackbank.aggregate([{ $sample: { size: 1 } }])


if __name__ == '__main__':
    app.run(debug=False)