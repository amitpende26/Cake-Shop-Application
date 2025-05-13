import mysql.connector
#from mysql.connector import Error
from flask import render_template,request,redirect,url_for
from werkzeug.utils import secure_filename



def addCake():
    if request.method == "GET":
        con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
    
        cursor = con.cursor()
        sql = "select * from category" 
        cursor.execute(sql)
        cats=cursor.fetchall()
        return render_template("addCake.html",cats=cats)
    else:
        cname = request.form["cname"]
        price= request.form["price"]
        description=request.form["description"]
        f = request.files['image_url'] 
        filename = secure_filename(f.filename)
        filename = "static/Images/"+f.filename
        #This will save the file to the specified location
        f.save(filename)   
        filename = "Images/"+f.filename
        #image url
        cat_id=request.form["cat"]


        con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
    
        cursor = con.cursor()
        sql = "insert into Cake (Cake_name,price,description,image_url,cid) values (%s,%s,%s,%s,%s)" 
        val = (cname,price,description,filename,cat_id)
        cursor.execute(sql,val)
        con.commit()
        return redirect(url_for("showAllCakes"))
    

def showAllCakes():
    con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
    
    cursor = con.cursor()
    sql = '''select cake_id,cake_name,price,description,image_url,
     cname from cake as c
     inner join category as cat
     on c.cid=cat.cid;'''
    cursor.execute(sql)
    cakes=cursor.fetchall()
    return render_template("showAllCakes.html",cakes=cakes)




    #cats = Set Of categories

'''def deleteCategory(id):
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
        return redirect(url_for("showAllCategories"))'''
