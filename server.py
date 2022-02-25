
from concurrent.futures.process import _ExceptionWithTraceback
from flask import Flask,render_template,request,redirect
import pymongo
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    client = pymongo.MongoClient(host = "localhost",port = 27017,serverSelectionTimeoutMS = 1000)
    db = client['Todopymongolist']
    client.server_info() #trigger the exception if not connected to the DB
except:
    print("ERROR - Cannot connect to the db")



@app.route("/",methods = ["GET","POST"])
def home():
    alltodos = db.users.find()
    count = db.users.count_documents({})
    if request.method == 'POST':
        try:
            user = {"title":request.form["title"],"description":request.form["desc"],"datetime":datetime.now()}
            print("title is",request.form["title"])
            print("Desc is",request.form["desc"])
            dbResponse = db.users.insert_one(user)
            print("todo with Id",dbResponse.inserted_id)
        except Exception as ex:
            print(ex)
    else:
        if request.method == 'GET':
            try:
                alltodos = db.users.find()
                count = db.users.count_documents({})
                print("all todos are",alltodos)
            except Exception as ex:
                print(ex)
   
    return render_template('index.html',allTodos = alltodos,allDocumentsCount = count)

@app.route("/about",methods = ["GET"])
def about():
    try:
        return render_template('test.html')
    except Exception as ex:
        print(ex)


@app.route("/update/<id>",methods = ["GET","POST"])
def update_todo(id):
    if request.method == 'POST':
        try:
            todo = db.users.find_one({"_id":ObjectId(id)})
            newvalues = { "$set": { "title": request.form["title"],"description":request.form["desc"] } }

            dbResponse = db.users.update_one(todo, newvalues)
            print("DB response is",dbResponse)
            
            return redirect("/")
           
        except Exception as ex:
            print(ex)

    
    try:
        todo = db.users.find_one({"_id":ObjectId(id)})
        print("todo is",todo)
        return render_template('updatesingletodo.html',todo = todo)
    except Exception as ex:
        print(ex)
    

@app.route("/delete/<id>")
def delete_todo(id):
    try:
        alltodos = db.users.find()
        document = db.users.find_one({"_id":ObjectId(id)})
        print("document is",document)
        dbResponse = db.users.delete_one(document)
        print("Db response is",dbResponse)
        return redirect("/",code = 302)
    except Exception as ex:
        print(ex)
    return render_template('index.html')
    #,allTodos = alltodos,count_of_todos = count





if __name__ == "__main__":
    app.run(debug = True)