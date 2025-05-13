import mysql.connector
#from mysql.connector import Error
from flask import render_template,request,redirect,url_for,session,make_response
from werkzeug.utils import secure_filename
from datetime import datetime

def homepage():
    con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
    
    cursor = con.cursor()
    sql = '''select cake_id,cake_name,price,description,image_url,
     cname from cake as c
     inner join category as cat
     on c.cid=cat.cid;'''
    cursor.execute(sql)
    cakes = cursor.fetchall()
    sql1= "select * from Category"
    cursor.execute(sql1)
    cats= cursor.fetchall()
    return render_template("homepage.html",cakes=cakes,cats=cats)

def showCakes(cid):
    con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
    cursor = con.cursor()
    # updaate in sql query as cakes_vw
    sql = ''' select * from cakes_vw where  cat_id=%s'''
    val=(cid,)
    cursor.execute(sql,val)
    cakes = cursor.fetchall()
    sql1= "select * from Category"
    cursor.execute(sql1)
    cats= cursor.fetchall()
    return render_template("homepage.html",cakes=cakes,cats=cats)

def Login():
    if request.method =="GET": 
            if "message" in request.cookies:
                message = request.cookies.get("message")
            else:
             message = None
            return render_template("Login.html",message=message)
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        sql = '''select count(*) from userinfo where username=
                    %s and  password=%s and role=%s'''
        con =mysql.connector.connect(host='localhost',user='root',password='Priyanka@26',port='3309',database='cakeshopproject')
        cursor = con.cursor() 
        val = (uname,pwd,'user')       
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if(int(count[0]) == 1):
            session["uname"]=uname
            return redirect("/")
            
        else:
            return redirect(url_for("Login"))
        
def Register():
     if request.method == "GET":
            return render_template("Register.html")
     else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        email = request.form["email"]
        #problem solve aftera adding Port and database cakeshopproject
        con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
        cursor = con.cursor()
        sql = "insert into UserInfo (username,password,email_id,role) values (%s,%s,%s,%s)" 
        val = (uname,pwd,email,'user')
        try:
            cursor.execute(sql,val)
        except:
            message="User already exists,please enter different username"
            return render_template("Register.html",message=message)
        else:
            con.commit()    
 
        return redirect("/Login")
    
def Logout():
    session.clear()
    return redirect("/")

def viewDetails(cake_id):
    if request.method == "GET":
        con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
        cursor = con.cursor()
        sql = '''select * from cakes_vw where cake_id=%s'''
        val = (cake_id,)
        cursor.execute(sql,val)
        cake = cursor.fetchone()
        return render_template("viewDetails.html",cake=cake)
    else:
        con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
        cursor = con.cursor()
        uname = session["uname"]
        qty = request.form["qty"]
        if "uname" in session:            
            sql = "select count(*) from mycart where username=%s and cake_id=%s"
            val = (session["uname"],cake_id)
            cursor.execute(sql,val)
            count = cursor.fetchone()
            if(int(count[0]) == 1):
                message = "Item already in cart"
            else:
                sql = "insert into MyCart (username,cake_id,qty) values (%s,%s,%s)"
                val = (uname,cake_id,qty)
                cursor.execute(sql,val)
                con.commit()
                message = "Item added to cart successfully"
                
            return redirect(url_for("showCartItems",message=message))
        else:
            #message = "You need to login to perform Add to cart"
            #resp = make_response(redirect("/Login"))
            #resp.set_cookie("message",message)
            #return resp
            return redirect("/Login")

def showCartItems():
    if request.method == "GET":
        if "uname" in session:     
            if "message" in request.args :
                message = request.args["message"]
            else:
                message = ""
            uname = session["uname"]    
            sql = "select * from Cart_vw where username=%s"
            val = (uname,)
            con = mysql.connector.connect(host='localhost',user="root",
            password="Priyanka@26",port="3309",database="cakeshopproject")
            cursor = con.cursor()
            cursor.execute(sql,val)
            items = cursor.fetchall()

            sql = "select sum(subtotal) from cart_vw where username=%s"
            val = (session["uname"],)
            cursor.execute(sql,val)
            total = cursor.fetchone()[0]
            session["total"] = total


            return render_template("Cart.html",items=items,message=message)
        else:
            return redirect("/Login")
    else:
        action = request.form["action"]
        con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
        cursor = con.cursor()
        if action == "update":
            qty = request.form["qty"]
            sql = "update MyCart set qty = %s where username=%s and cake_id=%s"
            val =  ( qty,session["uname"],request.form["cake_id"])            
            cursor.execute(sql,val)
            con.commit()            
        else:
            sql = "delete from MyCart where username=%s and cake_id=%s"
            val = ( session["uname"],request.form["cake_id"])            
            cursor.execute(sql,val)
            con.commit()
            
        return redirect("/Cart")
def MakePayment():
    if request.method == "GET":
        return render_template("MakePayment.html")
    else:
        cardno = request.form["cardno"]
        cvv = request.form["cvv"]
        expiry = request.form["expiry"]
        con = mysql.connector.connect(host='localhost',user="root",password="Priyanka@26",port="3309",database="cakeshopproject")
        cursor = con.cursor()
        sql = "select count(*) from payment where cardno=%s and cvv=%s and expiry=%s"
        val = (cardno,cvv,expiry)
        cursor.execute(sql,val)
        count = int(cursor.fetchone()[0])
        if count == 1:
            total = session["total"]
            #Perform transaction
            sql1 = "update payment set balance = balance - %s where cardno=%s and cvv=%s and expiry=%s"
            val1 = (total,cardno,cvv,expiry)
            sql2 = "update payment set balance = balance + %s where cardno=%s and cvv=%s and expiry=%s"
            val2 = (total,'2222','222','12/2030')
            cursor.execute(sql1,val1)
            cursor.execute(sql2,val2)
            con.commit()
            dd = datetime.today().strftime('%Y-%m-%d')
            sql3 = "insert into order_master (username,date_of_order,amount) values (%s,%s,%s)"
            val3 = (session["uname"],dd,total)
         
            cursor.execute(sql3,val3)
            con.commit()
            print("Done till ordermaster")
            sql4 = "select id from order_master where username=%s and date_of_order=%s and amount=%s limit 1"
            val4 = (session["uname"],dd,total)
            print(val4)
            cursor.execute(sql4,val4)
            oid = cursor.fetchone()[0]
            
            sql5 = "update mycart set order_id = %s where username=%s and order_id is null"
            val5 = (oid,session["uname"])
            cursor.execute(sql5,val5)
            con.commit()
            return redirect("/")
        else:
            return redirect(url_for("MakePayment"))


# lines select karun tab press kela tr lines pudhe jatat
