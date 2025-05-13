import mysql.connector
#from mysql.connector import Error
from flask import render_template,request,redirect,url_for

def addCategory():
    if request.method == "GET":
        return render_template("addCategory.html")
    else:
        cname = request.form["cname"]
        #problem solve aftera adding Port and database cakeshopproject
        con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
    
        cursor = con.cursor()
        sql = "insert into Category (cname) values (%s)" 
        val = (cname,)
        cursor.execute(sql,val)
        con.commit()
        return redirect(url_for("showAllCategories"))
    

def showAllCategories():
    con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
    
    cursor = con.cursor()
    sql = "select * from category" 
    cursor.execute(sql)
    cats=cursor.fetchall()
    return render_template("showAllCategories.html",cats=cats)


    #cats = Set Of categories

def deleteCategory(id):
    if request.method == "GET":
        return render_template("deleteConfirm.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            con =mysql.connector.connect(host='localhost',user='root',password='Priyanka@26',port='3309',database='cakeshopproject')
            cursor = con.cursor()
            sql = "delete from category where cid = %s"
            val = (id,)
            cursor.execute(sql,val)
            con.commit()
        return redirect(url_for("showAllCategories"))
def editCategory(id):
    if request.method == "GET":
        con =mysql.connector.connect(host='localhost',user='root',password='Priyanka@26',port='3309',database='cakeshopproject')
        cursor = con.cursor()
        sql = "select * from category where cid=%s"
        val = (id,)
        cursor.execute(sql,val)
        cat = cursor.fetchone()
        return render_template("editCategory.html",cat=cat)
    else:
        cname = request.form["cname"]
        con =mysql.connector.connect(host='localhost',user='root',password='Priyanka@26',port='3309',database='cakeshopproject')
        cursor = con.cursor()
        sql = "update category set cname=%s where cid=%s"
        val = (cname,id)
        cursor.execute(sql,val)
        con.commit()
        return redirect(url_for("showAllCategories"))
