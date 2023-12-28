
from flask import abort, render_template,redirect,url_for,request,flash
from . import user_bp
from .forms import SingUpForm,LoginForm, UserDetails
from flask_login import LoginManager, current_user,login_user,logout_user,login_required
from .user import User

@user_bp.route("/register",methods=["POST","GET"])
def register_user():
    form = SingUpForm()
    #if form is submitted 
    if form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        second_last_name = form.second_last_name.data
        email = form.email.data
        password = form.password.data
        #Creeate a User object with the data from the form
        new_user = User()
        result =  new_user.register_user(name,last_name,second_last_name,email,password)
        # if user has been created 
        if result == 0:
            #User has been created successfully, login it
            result = login_user(new_user, remember=True)
            #Redirect to the main page
            return redirect(url_for('public.landpage'))
        elif result == 1:
            #Email  already exist, throw error and redirect to form again
            form.form_errors = ["Existe un usuario registrado con ese email"]
            return render_template("register.html", form=form)
        else:
            #Error creating user
            form.form_errors = ["No se ha podido crear el usuario"]
            return render_template("register.html", form=form)

    else:    
        return render_template("register.html", form=form)
@user_bp.route("/login" ,methods=["GET","POST"])
def do_login():
   #If user is already authenticatted redirect to index.html
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    #if the user is not authenticated, do login
    else:
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            #Create user object 
            user = User()
            #Check if email and password corresponds to an user in the database
            if user.login_user(email,password):
                #Login the user into the app as user exists in the database
                login_user(user, remember=form.remember_me.data)
                #Redirect to the main page after loging
                return redirect(url_for('public.landpage'))
            else:
                #User doesn't exist into the database, redirect to login page and indicate the error
               form.form_errors = ["Usuario o contraseña erroneo"]
               return render_template("login.html", form=form)

        else:
            return render_template("login.html", form=form)

@user_bp.route("/logout" ,methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@user_bp.route("/details",methods=['GET','POST'])
@login_required
def user_details():
     user_details_form = UserDetails()
     user = User.get_user(current_user.get_id())

     if request.method == "GET":
        # if request is a GET render the template and fill with data
        # already retrieved from the DB
        user_details_form.name.data = user.get_name()
        user_details_form.last_name.data = user.get_last_name()
        user_details_form.second_last_name.data = user.get_second_last_name()
        user_details_form.email.data = user.get_email()
        return render_template("user_details.html", form = user_details_form)
     
     elif request.method == "POST":
        if request.form.get("change_user"):
             #if user modifies profile, save it
            if user_details_form.validate_on_submit():
             name = user_details_form.name.data
             last_name = user_details_form.last_name.data
             second_last_name = user_details_form.second_last_name.data
             email = user_details_form.email.data
             password = user_details_form.password.data
             result = user.update_user(name,last_name,second_last_name,email,password)

             if result:
                 flash("Usuario modificado",category="info")
                 return redirect(url_for('user.user_details'))
             else:
                 flash("Error al actualizar el usuario", category="error")
                 return redirect(url_for('user.user_details'))
        elif request.form.get("delete_user"):
            result = user.delete_user()

            if result:
                logout_user()
                return redirect(url_for('public.index'))
            else:
                flash("Error al eliminar el usuario",category="error")     
                return redirect(url_for('user.user_details'))
