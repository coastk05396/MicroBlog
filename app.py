import datetime
import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# def create_app():
app = Flask(__name__)
client = MongoClient(os.getenv("MONGODB_URI"))
app.db = client.microblog
print("connection sucessful")


@app.route("/", methods=["GET", "POST"]) #get = refresh page  #post = sumbit form
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        print(entry_content, formatted_date)
        # entries.append((entry_content, formatted_date)) #put in Tuple
        app.db.entries.insert_one({"content": entry_content, "date":formatted_date})
        return redirect("/")  
    entries_with_dates = [
        (
        entry["content"],
        entry["date"],
        datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"), 
        ) #datetime.datetime.strftime(datetime.datetime, format) 日期格式轉為字串格式。
          #datetime.datetime.strptime(string, format) 字串格式轉為日期格式。
        for entry in app.db.entries.find({})      
            
        ]
    
    return render_template("home.html", entries=entries_with_dates)          
  # return render_template("home.html", entries=entries_with_dates)

if __name__ == "__main__":
  app.run

  
