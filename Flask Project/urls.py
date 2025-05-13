from main import app
import category_op as cat
import cake_op as cake
import adminLogin as ad
import users
# Urls for Category
app.add_url_rule("/showAllCategories",view_func=cat.showAllCategories)
app.add_url_rule("/deleteCategory/<id>",view_func=cat.deleteCategory,methods=["GET","POST"])
app.add_url_rule("/editCategory/<id>",view_func=cat.editCategory,methods=["GET","POST"])
app.add_url_rule("/addCategory",view_func=cat.addCategory,methods=["GET","POST"])

#-------------url for cake-------------------
app.add_url_rule("/addCake",view_func=cake.addCake,methods=["GET","POST"])
app.add_url_rule("/showAllCakes",view_func=cake.showAllCakes)

#--------------url for admin-----------------
app.add_url_rule("/adminLogin",view_func=ad.login,methods=["GET","POST"])
app.add_url_rule("/adminHome",view_func=ad.adminHome)

#--------------url for User------------------------
app.add_url_rule("/",view_func=users.homepage)
app.add_url_rule("/showCakes/<cid>",view_func=users.showCakes)
app.add_url_rule("/Login",view_func=users.Login,methods=["GET","POST"])
app.add_url_rule("/Logout",view_func=users.Logout)
app.add_url_rule("/Register",view_func=users.Register,methods=["GET","POST"])
app.add_url_rule("/viewDetails/<cake_id>",view_func=users.viewDetails,methods=["GET","POST"])
app.add_url_rule("/Cart",view_func=users.showCartItems,methods=["GET","POST"])
app.add_url_rule("/MakePayment",view_func=users.MakePayment,methods=["GET","POST"])