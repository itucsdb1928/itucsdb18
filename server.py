from flask import Flask, redirect, render_template,flash,url_for,current_app,request
from forms import RegistrationForm,LoginForm

from datetime import datetime
from urllib.parse import urlparse
import os
import psycopg2 as dbapi2
from arrangement import Database
from datetime import date

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db=Database()

@app.route('/')
@app.route('/Home',methods=['GET','POST'])
def homepage():

    if request.method == "POST":
        if request.form["btn"] == "search":
            db.book_name=request.form["search_book"]
            print(db.book_name)
            My_list=db.Search(db.book_name)
        elif request.form["btn"] == "detail":
            print("detail")
            db.book_name=request.form["Book_name"]
            print(db.book_name)
            db.book_detail=db.get_detail_page(db.book_name)
            #db.update_rewiev(db.book_name)
            return redirect(url_for('detail_page'))
    else:
        My_list=db.get_home_page()
    return render_template('home.html',Status =db.UserId,title = "Home Page",titles=My_list)


@app.route('/SignIn',methods=['GET','POST'])
def sign_in_page():
    db.UserId= 0
    check = True
    form = LoginForm()
    if form.validate_on_submit():
        db.UserId = db.checkLogin(form.email.data,form.password.data)
        if db.UserId > 0:
            flash('Başarılı bir şekilde giriş yaptınız!', 'success')
            return redirect(url_for('profile_page'))
    
    return render_template('login.html',Status =db.UserId,title = "SıgnIn Page", form=form)

@app.route('/SignUp',methods=['GET','POST'])
def sign_up_page():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        db.UserId =  db.insertNewUser(form)
        if db.UserId > 0:
             return redirect(url_for('profile_page'))

    return render_template('register.html',Status=db.UserId,title = "SıgnUp Page",form= form )

@app.route('/Profile',methods=['GET','POST'])
def profile_page():
    profile=db.show_profile(db.UserId)
    if request.method == "POST":
        if request.form["btn"] == "edit_profile" :
            return redirect(url_for('edit_profile_page'))

    print("*******   ",profile)
    print(" User Id In profile func",db.UserId)
    return render_template('profile.html', Status=db.UserId, title = "Profile Page", profile=profile)

@app.route('/EditProfile',methods=['GET','POST'])
def edit_profile_page():
    profile = db.show_profile(db.UserId)
    if request.method == "POST":

        if request.form["btn"] == "cancel" :
            return redirect(url_for('profile_page'))
        elif request.form["btn"] == "save_changes" :
            name = request.form["name"]
            surname = request.form["surname"]
            gender = request.form["gender"]
            age = request.form["age"]
            email = request.form["email"]
            db.edit_profile(name,surname,gender,age,email,db.UserId)
            print(name,surname,gender,age,email)
            return redirect(url_for('profile_page'))

        # elif request.form["btn"] == "delete_profile":
        #     db.delete_profile(db.UserId)
        #     db.UserId=0
        #     return redirect(url_for('sign_in_page'))


    return render_template('edit_profile.html', Status=db.UserId, title="Edit Profile Page", profile=profile)


@app.route('/Detail',methods=['GET','POST'])
def detail_page():
    bookId = db.book_detail[5]
    today = date.today()
    bookRateInfo = db.getRewiev(bookId)
    detailStat = db.UserId
    commentCheck = db.checkUser(db.UserId,bookId)

    print(bookRateInfo)

    if(commentCheck == False):
        detailStat = -1

    if request.method == "POST":
        print("-----Form--", request.form["btn"])
        if request.form["btn"] == "ratingBtn" :
            userWiev = request.form
            today = today.strftime("%m/%d/%Y")
            print(userWiev)
            result = db.insertRate(db.UserId,bookId,userWiev,today)
            if(result):
                return redirect(url_for('detail_page'))
        elif request.form["btn"] == "updateBtn" :
            newContent = request.form['comment']
            db.book_detail[4] = newContent 
            db.updateBookContent(bookId,newContent)
            return redirect(url_for('homepage'))

    return render_template('detail.html',Status=detailStat,user=db.UserId,title = " %s Detail Page"%(db.book_name),details=db.book_detail,
                           name=db.book_name,rateInfo = bookRateInfo,today=today) 

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

