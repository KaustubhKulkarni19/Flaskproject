from flask import Flask, render_template, redirect, request, url_for
import pymysql

db = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "junebatch"
    )

cursor = db.cursor()


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    name = "Kaustubh"
    mylist = [50,20,20,20]
    return render_template("about.html",username=name,mylist=mylist)

@app.route("/allusers")
def allusers():
    cursor.execute("select * from user")
    data = cursor.fetchall()
    return render_template("allusers.html",userdata = data)

@app.route("/create",methods=["POST"])
def create():
    Username = request.form.get('Username')
    Password = request.form.get('Password')
    Contact = request.form.get('Contact')
    
    insq = "insert into user(Username,Password,Contact) values ('{}','{}','{}')".format(Username,Password,Contact)    
    try:
        cursor.execute(insq)
        db.commit()
        return redirect(url_for("allusers"))
    except:    
        db.rollback()
        return "Error in Query..."

@app.route("/delete")
def delete():
    id = request.args.get('id')
    delq = "delete from user where id='{}'".format(id)
    try:
        cursor.execute(delq)
        db.commit()
        return redirect(url_for("allusers"))
    except:    
        db.rollback()
        return "Error in Query..."

@app.route("/edit")
def edit():
    id = request.args.get('id')
    selq = "select * from user where id='{}'".format(id)
    cursor.execute(selq)
    data = cursor.fetchone()
    return render_template("edit.html",row = data)


@app.route("/update",methods=["POST"])
def update():
    Username = request.form.get('Username')
    Password = request.form.get('Password')
    Contact = request.form.get('Contact')
    uid = request.form.get('uid')
    
    updq = "update user set name='{}',password='{}',contact='{}' where id='{}'".format(Username,Password,Contact,uid)
    
    try:
        cursor.execute(updq)
        db.commit()
        return redirect(url_for("allusers"))
    except:    
        db.rollback()
        return "Error in Query..."

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/getdata",methods=["POST"])
def getdata():
    id = request.form.get('id')
    selq = "select * from user where id={}".format(id)
    cursor.execute(selq)
    data = cursor.fetchone()
    return render_template("search.html",row=data)

if __name__=='__main__':
    app.run(debug=True)
    
    