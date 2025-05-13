import mysql.connector
from flask import render_template,request,redirect,url_for,session


def login():
    if request.method == "GET":
        return render_template("adminLogin.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        sql = '''select count(*) from userinfo where username=
                    %s and  password=%s and role=%s'''
        con =mysql.connector.connect(host='localhost',user='root',password='Priyanka@26',port='3309',database='cakeshopproject')
        cursor = con.cursor() 
        val = (uname,pwd,'admin')       
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if(int(count[0]) == 1):
            session["uname"]=uname
            return redirect("/adminHome")
            return "Success"
        else:
            return redirect(url_for("login"))
        

def adminHome():
    if "uname" in session:
        return render_template("adminHome.html")
    else:
        return redirect(url_for("login"))
    

    #  for login as admin login id admin2 and password is admin1@123