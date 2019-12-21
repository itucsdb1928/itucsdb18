Parts Implemented by Muhammed Emin Topuz
========================================

My Tables in Database
---------------------

Users Table
-----------

.. code-block::

    CREATE TABLE IF NOT EXISTS Users(
                      UserID SERIAL PRIMARY KEY,
                      name VARCHAR (50)  NOT NULL,
                      surname VARCHAR (50)  NOT NULL,
                      gender VARCHAR (6) NOT NULL,
                      age VARCHAR (3) NOT NULL,
                      email VARCHAR (50) UNIQUE NOT NULL,
                      password VARCHAR (100)  NOT NULL,
                      isAdmin INTEGER DEFAULT 0
                     );

======  =========  ============  ========  =====  ==================  =======================  =========
UserID  name       surname       gender    age    email               password                 isAdmin
======  =========  ============  ========  =====  ==================  =======================  =========
1       admin      admin         None      0      admin@gmail.com      AAAAABd9BaEELg95qbxr7   1
2       Micheal    Holmes        Male      34     micholmes1@xyz.com   ggGShsghs53sggsfsgsgs   0
======  =========  ============  ========  =====  ==================  =======================  =========


I designed the SignUp, SignIn and Profile page for registering new user, entering the website and create a new profile.
I write a bunch of codes for user interface and provide easily travel in the website for users. I also use Crypto
module to encryp the passwords for protecting user privacy.

SignUp Page:

.. code-block::

    @app.route('/SignUp',methods=['GET','POST'])
    def sign_up_page():
        form = RegistrationForm()
        if form.validate_on_submit():
            print("submited")
            form.password.data = crp.password2secret(form.password.data)
            db.UserId = db.insertNewUser(form)
            if db.UserId > 0:
                flash('Başarılı bir şekilde giriş yaptınız!', 'success')
                return redirect(url_for('profile_page'))

        return render_template('register.html', Status=db.UserId, title="SıgnUp Page", form=form)

I checeked inputs for validation in the HTML files with using Jinja:

.. code-block::

    <div class="content-section">
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Joy In</legend>
            <div class="form-group">
                {{ form.name.label(class="form-control-label") }}
                {% if form.name.errors %}
                {{ form.name(class="form-control form-control-lg is-invalid") }}
                <div class="invalid-feedback">
                    {% for error in form.name.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
                {% else %}
                {{ form.name(class="form-control form-control-lg") }}
                {% endif %}
            </div>
            <div class="form-group">
                {{ form.surname.label(class="form-control-label") }}
                {% if form.surname.errors %}
                {{ form.surname(class="form-control form-control-lg is-invalid") }}
                <div class="invalid-feedback">
                    {% for error in form.surname.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
                {% else %}
                {{ form.surname(class="form-control form-control-lg") }}
                {% endif %}
            </div>
            <div class="form-group">
                {{ form.age.label(class="form-control-label") }}
                {% if form.age.errors %}
                {{ form.age(class="form-control form-control-lg is-invalid") }}
                <div class="invalid-feedback">
                    {% for error in form.age.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
                {% else %}
                {{ form.age(class="form-control form-control-lg") }}
                {% endif %}
            </div>

            <div class="form-group">
                {{ form.gender.label(class="form-control-label") }}
                {{ form.gender(class="form-control form-control-lg") }}

            </div>

            <div class="form-group">
                {{ form.email.label(class="form-control-label") }}
                {% if form.email.errors %}
                {{ form.email(class="form-control form-control-lg is-invalid") }}
                <div class="invalid-feedback">
                    {% for error in form.email.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
                {% else %}
                {{ form.email(class="form-control form-control-lg") }}
                {% endif %}
            </div>
            <div class="form-group">
                {{ form.password.label(class="form-control-label") }}
                {% if form.password.errors %}
                {{ form.password(class="form-control form-control-lg is-invalid") }}
                <div class="invalid-feedback">
                    {% for error in form.password.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
                {% else %}
                {{ form.password(class="form-control form-control-lg") }}
                {% endif %}
            </div>
            <div class="form-group">
                {{ form.confirm_password.label(class="form-control-label") }}
                {% if form.confirm_password.errors %}
                {{ form.confirm_password(class="form-control form-control-lg is-invalid") }}
                <div class="invalid-feedback">
                    {% for error in form.confirm_password.errors %}
                    <span>{{ error }}</span>
                    {% endfor %}
                </div>
                {% else %}
                {{ form.confirm_password(class="form-control form-control-lg") }}
                {% endif %}
            </div>
        </fieldset>
        <div class="form-group">
            {{ form.submit(class="btn btn-outline-info") }}
                </div>
            </form>
        </div>
        <div class="border-top pt-3">
            <small class="text-muted">
            Already Have an Account? <a class="ml-2" href="{{ url_for('sign_up_page') }}">Sign in Now</a>
            </small>
        </div>

For validation:

.. code-block::

    class RegistrationForm(FlaskForm):
        name = StringField('Name',
                           validators=[DataRequired(),Length(max=50)])
        surname = StringField('Surname',
                           validators=[DataRequired(),Length(max=50)])

        gender = SelectField('gender', choices=[('Male','Male'), ('Female','Female')], default=2, validators=[DataRequired()])

        age = StringField('Age',
                           validators=[DataRequired(),required(),Length(min=1, max=3)])

        email = StringField('Email',
                            validators=[DataRequired(), Email(),Length(max=50)])

        password = PasswordField('Password', validators=[DataRequired(),Length(min=6,max=9)])

        confirm_password = PasswordField('Confirm Password',
                                         validators=[DataRequired(), EqualTo('password')])


        submit = SubmitField('Sign Up')

I  also added the new user into database if all inputs are available and proper.

.. code-block::

        def insertNewUser(self,form):
            userId = 0
            with dbapi2.connect(self.url) as connection:
               cursor = connection.cursor()
               query = "select email from users where email = '%s';" %(form.email.data)
               cursor.execute(query)
               info = cursor.fetchone()

            if info is None:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    query = "INSERT INTO Users (name,surname,gender,age,email,password,isAdmin) VALUES ('%s','%s','%s','%s','%s', '%s',0);" %(form.name.data,form.surname.data,form.gender.data,form.age.data,form.email.data,form.password.data)
                    cursor.execute(query)
                    cursor.close()

                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    query = "SELECT UserID  FROM Users WHERE email='%s';" %(form.email.data)
                    cursor.execute(query)
                    info = cursor.fetchone()
                    cursor.close()
                    userId = info[0]


                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    query = "INSERT INTO UserContent (userid,FavAuthor,FavBook,FavPublisher) VALUES ('%s','','','');" %(userId)
                    cursor.execute(query)
                    cursor.close()

            return userId




SignIn page:

.. code-block::

    @app.route('/SignIn',methods=['GET','POST'])
    def sign_in_page():
        db.UserId= 0
        form = LoginForm()
        if form.validate_on_submit():
            db.UserId = db.checkLogin(form.email.data,form.password.data)
            if db.UserId > 0:
                flash('Başarılı bir şekilde giriş yaptınız!', 'success')
                return redirect(url_for('profile_page'))

        return render_template('login.html',Status =db.UserId,title = "SıgnIn Page", form=form)


I checked the email and password if both of them are valid, I provided the sign in function for user.

.. code-block::

       def checkLogin(self,email,password):
           UserID = 0
           info = []
           with dbapi2.connect(self.url) as connection:
               cursor = connection.cursor()
               query = "SELECT UserID,password FROM Users WHERE email='%s';" %(email)
               cursor.execute(query)
               info = cursor.fetchone()
               cursor.close()

           if(info is not None):
               if(password == self.crt.secret2password(info[1]).decode("utf-8")):
                   UserID = info[0]

           return UserID

I checked the inputs for validation:

.. code-block::

    class LoginForm(FlaskForm):
        email = StringField('Email',
                            validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember = BooleanField('Remember Me')
        submit = SubmitField('Sign In')

I designed the profile page for user to see own profile informations and edit profilebutton
to edit her/his own information.

Profile Page:

.. code-block::

    @app.route('/Profile',methods=['GET','POST'])
    def profile_page():
        addNewContent = 0
        profile=db.show_profile(db.UserId)
        if (len(profile) == 5):
            addNewContent = 1
        print("------new cont:",addNewContent)
        if request.method == "POST":
            if request.form["btn"] == "edit_profile" :
                return redirect(url_for('edit_profile_page'))
            elif request.form["btn"] == "edit_userContent":
                return redirect(url_for('edit_user_content'))
            if request.form["btn"] == "add_content":
                return redirect(url_for('add_user_content'))

        return render_template('profile.html', Status=db.UserId, title = "Profile Page", profile=profile,addContent = addNewContent)


Show the profile to the user. For doing this, I impelemented the Read Features that Database includes.

.. code-block::

     def show_profile(self,UserId):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "SELECT users.name,users.surname,users.gender,users.age,users.email,usercontent.commentsnum,usercontent.favauthor,usercontent.favbook,usercontent.favpublisher,usercontent.likedcommentnum FROM Users,usercontent WHERE Users.UserID=usercontent.userid and Users.UserID={}".format(UserId)
           cursor.execute(query)
           profile = cursor.fetchone()
           cursor.close()
        if (profile is None):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                query = "SELECT users.name,users.surname,users.gender,users.age,users.email FROM Users WHERE UserID={}".format(UserId)
                cursor.execute(query)
                profile = cursor.fetchone()
                cursor.close()
        return profile

For sessioning, every user can delete their own profile and deleted from database on their own except the admin.
In profile html i checked the userid to recognize the user is admin or not.

.. code-block::

    {% if Status != 1 %}
    <div class="form-group">
            <form method="POST"  action="/Profile">


            <input type="hidden" name="edit_profile" >

                <button class="button is-danger" action="submit" id="edit_profile" name="btn" value="edit_profile">Edit Profile</button>


        </form>

          </div>
    {% endif %}

Edit Profile Page:

.. code-block::

    @app.route('/EditProfile',methods=['GET','POST'])
    def edit_profile_page():
        profile = db.show_profile(db.UserId)
        print(profile)
        form = editProfile()
        if request.method == "POST":
            if form.validate_on_submit():
                db.edit_profile(form.name.data, form.surname.data, form.age.data, form.gender.data, db.UserId)
                return redirect(url_for('profile_page'))
            if request.form["btn"] == "cancel" :
                return redirect(url_for('profile_page'))
            elif request.form["btn"] == "delete":
                db.delete_profile(db.UserId)
                db.UserId = 0
                return redirect(url_for('sign_up_page'))

        return render_template('edit_profile.html', Status=db.UserId, title="Edit Profile Page", profile=profile,form=form)


Editing profile by using Update function in postgresql:

.. code-block::

     def edit_profile(self,name,surname, age, gender, Userid):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "UPDATE Users SET name='{}',surname='{}',age={},gender='{}' WHERE UserID={};".format(name, surname, age, gender, Userid)
           cursor.execute(query)
           cursor.close()

For validation i checked the inputs of user in edit profile page.

.. code-block::

    class editProfile(FlaskForm):
        name = StringField('Name',
                           validators=[DataRequired(),Length(max=50)])
        surname = StringField('Surname',
                           validators=[DataRequired(),Length(max=50)])

        gender = SelectField('gender', choices=[('Male','Male'), ('Female','Female')], default=2, validators=[DataRequired()])

        age = StringField('Age',
                           validators=[DataRequired(),required(),Length(min=1, max=3)])



        submit = SubmitField('Edit')

Delete profile function.

.. code-block::

     def delete_profile(self, Userid):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "DELETE FROM BookComment WHERE UserID={};".format(Userid)
           cursor.execute(query)
           query = "DELETE FROM UserContent WHERE UserID={};".format(Userid)
           cursor.execute(query)
           query = "DELETE FROM Users WHERE UserID={};".format(Userid)
           cursor.execute(query)
           cursor.close()



BookComment Table
-----------------

.. code-block::

    CREATE TABLE IF NOT EXISTS BookComment(
                      BookCommentID SERIAL PRIMARY KEY ,
                      UserRating INTEGER NOT NULL,
                      UserComment VARCHAR(500) NOT NULL,
                      CommentDate DATE NOT NULL,
                      DislikeNum INTEGER NOT NULL,
                      LikeNum INTEGER DEFAULT 0 NOT NULL
                     );
    ALTER TABLE BookComment ADD COLUMN UserID INTEGER REFERENCES Users (UserID) ON DELETE CASCADE;
    ALTER TABLE BookComment ADD COLUMN BookID INTEGER REFERENCES Books (BookID) ON DELETE CASCADE;
    ALTER TABLE BookComment ALTER COLUMN DislikeNum SET DEFAULT 0;
    ALTER TABLE BookComment ALTER COLUMN DislikeNum SET NOT NULL;

=============   ========== ======================  ===========  ========== =======  ======  ======
BookCommentID   UserRating UserComment             CommentDate  DislikeNum LikeNum  UserID  BookID
=============   ========== ======================  ===========  ========== =======  ======  ======
1               5           Very good book!        08/25/2018   4          128      5        6
2               3           Almost perfect!        09/11/2017   14         85       6        14
=============   ========== ======================  ===========  ========== =======  ======  ======


I create the comment table for books to Users see the book's votes and comments and they have an idea
of book that never knows or to inform other users about that book.

In Detail page users can read the comments, add a new comment tot the books and rate the books.

.. code-block::

    def getReview(self,bookId):
        info = None
        sum = 0
        avg = 0
        rates = {1:[0,0],2:[0,0],3:[0,0],4:[0,0],5:[0,0]}
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "SELECT BookComment.userrating,BookComment.usercomment,users.name,BookComment.commentdate,BookComment.LikeNum,BookComment.DislikeNum,users.UserId from BookComment,users WHERE BookComment.userid = users.userid and  bookid =  %d" %(bookId)
           cursor.execute(query)
           info = cursor.fetchall()
           cursor.close()

        #print("date ex: %s"%(d))
        for i in info:
          sum += i[0]
          rates[i[0]][0] += 1

        voteNum = len(info)
        for i in range(1,6):
            if(voteNum):
                rates[i][1] = int((rates[i][0] / voteNum)*100)
            else:
                rates[i][1] = 0

        if voteNum: avg = (sum / voteNum)

        return (avg,int(avg),voteNum,rates,info)

    def insertRate(self,userId,bookId,form,today):
        info = None

        with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                query = "UPDATE UserContent SET CommentsNum = CommentsNum+1 WHERE UserID=%s"%(userId)
                cursor.execute(query)
                cursor.close()

        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "INSERT INTO BookComment (UserID,BookID,UserRating,UserComment,commentdate) VALUES (%s, %s ,%s,'%s','%s');" %(userId,bookId,form['optradio'],form['comment'],today)
           cursor.execute(query)
           cursor.close()
           return True

        return False

The users also delete their comments:

.. code-block::

     def delete_comment(self,bookId):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM bookcomment WHERE userid={} and bookid={};".format(self.UserId,bookId)
            cursor.execute(query)
            cursor.close()

I added to the comments like and dislike number features to rated the comments by other users.

.. code-block::

     def updateLike(self,userId,type):
         if(type == "like"):
             with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                query = "UPDATE UserContent SET LikedCommentNum = LikedCommentNum+1 WHERE UserID=%s"%(userId)
                cursor.execute(query)
                cursor.close()

         with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            if(type == "like"):
                query = "UPDATE BookComment SET LikeNum = LikeNum+1 WHERE UserID=%s"%(userId)
            else:
                query = "UPDATE BookComment SET DislikeNum = DislikeNum+1 WHERE UserID=%s"%(userId)
            cursor.execute(query)
            cursor.close()

For session only users can add, delete and rate the books. The non-registered users can only see the comments.

.. code-block::

     {% if Status > 0 %}
        <label class="radio-inline" name="btn" value="ratingBtn">
            <button class="button is-link" action='submit' name="btn" value="ratingBtn">Share</button>
        </label>
     {% endif %}



UserContent Table
-----------------

.. code-block::

    CREATE TABLE IF NOT EXISTS UserContent(
                      UserContentID SERIAL PRIMARY KEY ,
                      UserID INTEGER REFERENCES Users (UserID)ON DELETE CASCADE,
                      CommentsNum INTEGER NOT NULL,
                      FavAuthor VARCHAR(20) NOT NULL,
                      FavBook VARCHAR(20) NOT NULL,
                      FavPublisher VARCHAR(20) NOT NULL,
                      LikedCommentNum INTEGER DEFAULT 0 NOT NULL
                     );
     ALTER TABLE UserContent ALTER COLUMN CommentsNum SET DEFAULT 0;
     ALTER TABLE UserContent ALTER COLUMN CommentsNum SET NOT NULL;

=============   ======  ============  ============  ========== ============  ===============
UserContentID   UserID  CommentsNum   FavAuthor     FavBook    FavPublisher  LikedCommentNum
=============   ======  ============  ============  ========== ============  ===============
1               5       14            ALex Nash     Limitless  Betha         74
2               124     25            Tara Bagvell  The End    Triplex       24
=============   ======  ============  ============  ========== ============  ===============

I create the user content table for users to add favorite authors, favorite publisher and favorite
books on their own profile page. They can also delete their contents, edit their contents and see their
comments that how many user liked that comment.

.. code-block::

    @app.route('/AddingUserContent',methods=['GET','POST'])
    def add_user_content():
        form = AddUserContent()
        if request.method == "POST":
            if form.validate_on_submit():
                db.NewContent(form)
                return redirect(url_for('profile_page'))
            elif request.form["btn"] == "cancel":
                return redirect(url_for('profile_page'))
        return render_template('add_content.html', Status=db.UserId, title="Add Content",form=form)

    @app.route('/EditUserContent',methods=['GET','POST'])
    def edit_user_content():
        profile = db.show_profile(db.UserId)
        print(profile)
        form = AddUserContent()
        if request.method == "POST":
            if form.validate_on_submit():
                print("buradayımmmmm------------------------")
                print("Edit part---->",form.author.data)
                db.edit_user_content(form)
                return redirect(url_for('profile_page'))
            elif request.form["btn"] == "delete":
                db.delete_user_content()
                return redirect(url_for('profile_page'))
            elif request.form["btn"] == "cancel" :
                print("-------->print:",request.form)
                return redirect(url_for('profile_page'))

        return render_template('edit_user_content.html', Status=db.UserId, title="Edit Profile Page", profile=profile,form=form)

Add,edit and delete functions:

.. code-block::

    def NewContent(self,form):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO UserContent (FavAuthor,FavBook,FavPublisher,UserID) VALUES ('%s','%s','%s',%d);" % (
            form.book.data, form.publisher.data, form.author.data,self.UserId)
            cursor.execute(query)
            cursor.close()

    def edit_user_content(self,form):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "UPDATE USERCONTENT SET favauthor='{}',favbook='{}',favpublisher='{}'WHERE UserID={};".format(form.author.data,form.book.data,form.publisher.data,self.UserId)
           cursor.execute(query)
           cursor.close()

    def delete_user_content(self):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "DELETE FROM UserContent WHERE UserID={};".format(self.UserId)
           cursor.execute(query)
           cursor.close()


For validation i checked the contents inputs.

.. code-block::

    class AddUserContent(FlaskForm):
        book = StringField('FavBook',
                           validators=[DataRequired()])
        publisher = StringField('FavPublisher',
                           validators=[DataRequired()])

        author = StringField('Favauthor',
                            validators=[DataRequired()])

        submit = SubmitField('submit')





