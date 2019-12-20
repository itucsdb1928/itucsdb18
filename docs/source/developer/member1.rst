Parts Implemented by Mehmet Ali Han Tutuk
=========================================

My Tables in Database
---------------------
Books Table
-----------
.. code-block::

    CREATE TABLE IF NOT EXISTS Books(
                      BookID SERIAL PRIMARY KEY ,
                      Title VARCHAR(20) NOT NULL,
                      PostDate  DATE DEFAULT CURRENT_DATE NOT NULL,
                      PageNum INTEGER NOT NULL,
                      PublisherID INTEGER  REFERENCES Publisher (PublisherID) ON DELETE CASCADE,
                      AuthorID INTEGER  REFERENCES Author (AuthorID) ON DELETE CASCADE,
                      Content VARCHAR(500) NOT NULL,
                      BookReview INTEGER DEFAULT 0 NOT NULL
                     );

======  =========  ============  ========  =============  =========  ====================  ===========
BookID  Title      PostDate      PageNum   PublisherID    AuthorID   Content               BookReview
======  =========  ============  ========  =============  =========  ====================  ===========
1       OZ         01/05/2015    356        12            8          Lorem Ipsum Dolor.    5
2       Fund       02/07/2010    455        10            12         Nice Books Ever.      15
======  =========  ============  ========  =============  =========  ====================  ===========

I implemented the 4 main database standardization skills on the tables such as Create, Read, Update and Delete.

I showed some book attributes on the homepage and i added some extra useful tools such as search box and added
the see detail button.Additionally, i implemented the session such as add a new book, add  new author and add a
new publisher buttons which are not seen by the user,only admin access these buttons.

.. code-block::

    @app.route('/')
    @app.route('/Home',methods=['GET','POST'])
    def homepage():
        My_list = []
        if request.method == "POST":
            if request.form["btn"] == "search":
                db.book_name=request.form["search_book"]
                My_list=db.Search(db.book_name)
            elif request.form["btn"] == "detail":
                db.book_name=request.form["Book_name"]
                db.book_detail=db.get_detail_page(db.book_name)
                return redirect(url_for('detail_page'))
            elif request.form["btn"] == "add_book":
                return redirect(url_for('add_book'))
            elif request.form["btn"] == "add_author":
                return redirect(url_for('add_author'))
            elif request.form["btn"] == "add_publisher":
                return redirect(url_for('add_publisher'))
        else:
            My_list=db.get_home_page()
        return render_template('home.html',Status =db.UserId,title = "Home Page",titles=My_list,user=db.UserId)


Read Function in Homepage:

.. code-block::

    def get_home_page(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "SELECT Books.Title,Books.content,Books.BookReview,Books.PostDate FROM Books,Author,Publisher  WHERE Books.PublisherID=Publisher.PublisherID AND Books.AuthorID=Author.AuthorID ORDER BY Books.BookReview DESC"
            cursor.execute(query)
            home = cursor.fetchall()
            cursor.close()

        return home


Add a new bookpage and backround database code:

.. code-block::

    @app.route('/Add_Book',methods=['GET','POST'])
    def add_book():
    if request.method == "POST":
        if request.form["btn"] == "cancel":
            return redirect(url_for('homepage'))
        elif request.form["btn"] == "add_book":
            title=request.form["title"]
            postdate=request.form["postdate"]
            PageNum=request.form["PageNum"]
            content=request.form["content"]
            authorid=request.form["Authorid"]
            publisherid=request.form["Publisherid"]
            db.add_new_book(title, postdate, PageNum, content, authorid, publisherid)

            return redirect(url_for('homepage'))


    return render_template('add_book.html', Status=db.UserId, title="New Book Page",publisher=db.all_publishers(),author=db.all_authors())

Insert new book to the database:

.. code-block::

    def add_new_book(self,title, postdate, PageNum, content, authorid, publisherid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Books (Title, PostDate,PageNum,Content,AuthorID, PublisherID ) VALUES ('{}', '{}', {}, '{}',{},{} );".format(title, postdate, PageNum, content, authorid, publisherid)

            cursor.execute(query)
            cursor.close()


Search book function:

.. code-block::

    def Search(self,name):
       with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "SELECT Books.Title,Books.content FROM Books,Author,Publisher  WHERE Books.PublisherID=Publisher.PublisherID AND Books.AuthorID=Author.AuthorID AND Books.Title LIKE '%%%s%%' "%(name)
           cursor.execute(query)
           search = cursor.fetchall()
           cursor.close()

       return search



I showed some book attributes on the detail page and in detail page user can add  a comment to the book.
There is a delete book button that only seen by Admin.
.. code-block::

    @app.route('/Detail',methods=['GET','POST'])
    def detail_page():
    bookId = db.book_detail[5]
    today = date.today()
    bookRateInfo = db.getReview(bookId)
    detailStat = db.UserId
    commentCheck = db.checkUser(db.UserId,bookId)

    if(commentCheck == False):
        detailStat = -1

    if request.method == "POST":
        if request.form["btn"] == "ratingBtn" :
            userWiev = request.form
            print(userWiev)
            today = today.strftime("%m/%d/%Y")
            result = db.insertRate(db.UserId,bookId,userWiev,today)
            if(result):
                return redirect(url_for('detail_page'))
        elif request.form["btn"] == "updateBtn" :
            newContent = request.form['comment']
            db.updateBookContent(bookId,newContent)
            return redirect(url_for('homepage'))
        elif request.form["btn"] == "delete_book":
            db.delete_book(bookId)
            return redirect(url_for('homepage'))
        elif request.form["btn"] == "1":
            print("ım here",request.form["custId"])
            db.updateLike(request.form["custId"],"like")
            return redirect(url_for('detail_page'))
        elif request.form["btn"] == "-1":
            db.updateLike(request.form["custId"],"dislike")
            return redirect(url_for('detail_page'))
        elif request.form["btn"] == "delete_comment":
            db.delete_comment(bookId)
            return redirect(url_for('detail_page'))
        elif request.form["btn"] == "detail_p_a":
            if request.form['radiobutton']=='author':
                db.author_details=db.show_author_detail(db.book_detail[0],db.book_detail[1])
                return redirect(url_for('author_detail_page'))
            else:
                db.publisher_details=db.show_publisher_detail(db.book_detail[2])
                return redirect(url_for('publisher_detail_page'))


    return render_template('detail.html',Status=detailStat,user=db.UserId,title = " %s Detail Page"%(db.book_name),details=db.book_detail,
                           name=db.book_name,rateInfo = bookRateInfo,today=today)


Read Function in DetailPage and update bookreview:

.. code-block::

    def get_detail_page(self,book_name):
       with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "UPDATE Books SET BookReview = BookReview+1 WHERE Books.Title='%s'"%(book_name)
            cursor.execute(query)
            cursor.close()
       with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "SELECT Author.name,Author.surname,Publisher.name,Books.PageNum,Books.content,Books.BookID FROM Books,Author,Publisher  WHERE Books.PublisherID=Publisher.PublisherID AND Books.AuthorID=Author.AuthorID AND Books.Title='%s'"%(book_name)
           cursor.execute(query)
           detail = cursor.fetchone()
           cursor.close()
       return detail

Delete function in DetailPage:

.. code-block::

     def delete_book(self, bookid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BookComment WHERE BookID={};".format(bookid)
            cursor.execute(query)
            query = "DELETE FROM Books WHERE BookID={};".format(bookid)
            cursor.execute(query)
            cursor.close()


Update book content functions:

.. code-block::

    def updateBookContent(self,bookId,newComment):
        info = None
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "UPDATE books SET content = '%s' WHERE bookid = %d" %(newComment,bookId)
           cursor.execute(query)
           cursor.close()


Author Table
------------

.. code-block::

    CREATE TABLE IF NOT EXISTS Author(
                      AuthorID SERIAL PRIMARY KEY ,
                      name VARCHAR(30) NOT NULL,
                      surname VARCHAR(30) NOT NULL,
                      birthDate DATE NOT NULL,
                      numberOfbooks INTEGER NOT NULL,
                      country VARCHAR(40) NOT NULL
                     );

========  =========  ============  ==========  =============  =========
AuthorID  name       surname       birthDate   numberOfbooks  country
========  =========  ============  ==========  =============  =========
1         Alex       Smith         01/02/1984  12             England
2         John       Purcell       03/16/1954  25             Scotland
========  =========  ============  ==========  =============  =========

I implemented the 4 main database standardization skills on the tables such as Create, Read, Update and Delete.

I showed the author details in the author details page which is accessed with the button on the detail page.
In this page, every user can see all attributes of the authorbut only admin see the edit author button which
update contents of author table and delete author button which deletes all author information include it's references books.

Author Detail Page,Add author page and edit author page:

.. code-block::

    @app.route('/Author_Profile',methods=['GET','POST'])
    def author_detail_page():
    nameAuthor=db.book_detail[0]
    surnameAuthor=db.book_detail[1]
    if request.method == "POST":
        if request.form["btn"] == "update_author":
            return redirect(url_for("edit_author_page"))


    return render_template('detail_author.html',Status =db.UserId, title="Author Detail Page",author=db.author_details, name=nameAuthor,surname=surnameAuthor,user=db.UserId)

    @app.route('/EditAuthor',methods=['GET','POST'])
    def edit_author_page():
    form = editAuthor()
    if request.method == "POST":
        if form.validate_on_submit():
            db.edit_author(form.name.data, form.surname.data,form.date.data,form.numOfBooks.data,form.country.data, db.author_details[5])
            return redirect(url_for('homepage'))
        elif request.form["btn"] == "cancel":
            return redirect(url_for('author_detail_page'))
        elif request.form["btn"] == "delete_author":
            db.delete_author(db.author_details[5])
            return redirect(url_for('homepage'))

    return render_template('edit_author.html', Status=db.UserId, title="Edit Author Page",author=db.author_details,user=db.UserId,form=form)

    @app.route('/Add_Author',methods=['GET','POST'])
    def add_author():
    Country = "Universe"
    if request.method == "POST":
        if request.form["btn"] == "cancel":
            return redirect(url_for('homepage'))
        elif request.form["btn"] == "add_author":
            name = request.form["name"]
            surname = request.form["surname"]
            birthdate = request.form["birthdate"]
            numberofbooks = request.form["numberofbooks"]
            Country = request.form["country"]
            db.add_new_author(name,surname, birthdate, numberofbooks, Country)

            return redirect(url_for('homepage'))


    return render_template('add_author.html', Status=db.UserId, title="New Author Page",country=Country)

Read,create,delete and udate author functions:

.. code-block::

    def show_author_detail(self,authorName,authorSurname):

        with dbapi2.connect(self.url) as connection:
             cursor = connection.cursor()
             query = "SELECT DISTINCT Author.name,Author.surname,Author.Birthdate,Author.Numberofbooks,Author.Country,Author.Authorid FROM Author,Books WHERE Author.Authorid=Books.authorid AND Author.name='%s' AND Author.Surname='%s';" % (authorName,authorSurname)
             cursor.execute(query)
             authorDetails=cursor.fetchone()
             cursor.close()
             return authorDetails

    def edit_author(self,name,surname, birthdate, numberofbooks, country,authorid):
         with dbapi2.connect(self.url) as connection:
             cursor = connection.cursor()
             query = "UPDATE Author SET name='{}',surname='{}',birthdate='{}',numberofbooks={},country='{}' WHERE authorid={};".format(name,surname, birthdate, numberofbooks, country,authorid)
             cursor.execute(query)
             cursor.close()

    def delete_author(self, authorid):

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Author WHERE AuthorID={};".format(authorid)
            cursor.execute(query)
            cursor.close()

    def add_new_author(self,name,surname, birthdate, numberofbooks, Country):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Author (name,surname,birthdate,numberOfbooks ,country) VALUES ('{}', '{}', '{}', {},'{}');".format(name ,surname, birthdate, numberofbooks, Country)
            cursor.execute(query)
            cursor.close()


Publisher Table
---------------

.. code-block::

    CREATE TABLE IF NOT EXISTS Publisher(
                      PublisherID SERIAL PRIMARY KEY ,
                      name VARCHAR(40) NOT NULL,
                      adress VARCHAR(50) NOT NULL,
                      numberOfbooks INTEGER NOT NULL,
                      establishmentDate DATE NOT NULL,
                      companyName VARCHAR(50) NOT NULL
                     );

============ =========  ================  =============  =================  ===========
PublisherID  name       adress            numberOfbooks  establishmentDate  companyName
============ =========  ================  =============  =================  ===========
1            Alpha      Main street       145            06/11/2001         Mono INC.
2            Betha      Temproray street  258            03/24/1988         PUDY INC.
============ =========  ================  =============  =================  ===========

I implemented the 4 main database standardization skills on the tables such as Create, Read, Update and Delete.

I showed the publisher details in the publisher details page which is accessed with the button on the detail page.
On this page, every user can see all attributes of the publisher but only admin see the delete publisher button
which deletes all publisher information include it's references books.


Publisher Detail Page, Add Publisher Page and Edit Publisher Page:

.. code-block::

    @app.route('/Publisher_Profile',methods=['GET','POST'])
    def publisher_detail_page():
        if request.method == "POST":
            if request.form["btn"] == "update_publisher":
                return redirect(url_for("edit_publisher_page"))
        return render_template('detail_publisher.html',Status =db.UserId, title="Edit Publisher Page",publisher=db.publisher_details, name=db.book_detail[2],user=db.UserId)


    @app.route('/EditPublisher',methods=['GET','POST'])
    def edit_publisher_page():
        print(db.publisher_details[4])
        form = editPublisher()
        if request.method == "POST":
            if form.validate_on_submit():
                db.edit_publisher(form.name.data, form.address.data, form.numOfBooks.data, form.date.data, form.companyName.data, db.publisher_details[4])
                return redirect(url_for('homepage'))
            elif request.form["btn"] == "cancel":
                return redirect(url_for('publisher_detail_page'))
            elif request.form["btn"] == "delete_publisher":
                db.delete_publisher(db.publisher_details[4])
                return redirect(url_for('homepage'))

        return render_template('edit_publisher.html', Status=db.UserId, title="Edit Publisher Page",publisher=db.publisher_details, name=db.book_detail[2],user=db.UserId,form=form)

    @app.route('/Add_Publisher',methods=['GET','POST'])
    def add_publisher():
        if request.method == "POST":
            if request.form["btn"] == "cancel":
                return redirect(url_for('homepage'))
            elif request.form["btn"] == "add_publisher":
                name = request.form["name"]
                adress = request.form["adress"]
                numberOfbooks = request.form["numberofbooks"]
                establishmentdate = request.form["establismentdate"]
                companyName = request.form["companyname"]
                db.add_new_publisher(name,adress,numberOfbooks, establishmentdate, companyName)

                return redirect(url_for('homepage'))


        return render_template('add_publisher.html', Status=db.UserId, title="New Publisher Page")


Read,create,delete and udate publisher functions:

.. code-block::

     def show_publisher_detail(self,publisherName):

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "SELECT DISTINCT Publisher.adress,Publisher.numberOfbooks,Publisher.establishmentDate,Publisher.companyName,Publisher.publisherid FROM Publisher,Books WHERE Publisher.publisherid=Books.publisherid AND Publisher.name='%s' ;" % (publisherName)
            cursor.execute(query)
            publisherDetails=cursor.fetchone()
            cursor.close()
            return publisherDetails

    def edit_publisher(self,name,adress,numberOfbooks, establishmentdate, companyName,publisherid):
         with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "UPDATE Publisher SET name='{}',adress='{}',numberofbooks={},establishmentdate='{}',companyname='{}' WHERE PublisherID={};".format(name,adress,numberOfbooks, establishmentdate, companyName,publisherid)
           cursor.execute(query)
           cursor.close()

    def delete_publisher(self,publisherid):

         with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "DELETE FROM Publisher WHERE PublisherID={};".format(publisherid)
           cursor.execute(query)
           cursor.close()

    def add_new_publisher(self,name,adress,numberOfbooks, establishmentdate, companyName):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Publisher (name,adress,numberOfbooks ,establishmentDate ,companyName ) VALUES ('{}', '{}', {}, '{}','{}');".format(name,adress,numberOfbooks, establishmentdate, companyName)
            cursor.execute(query)
            cursor.close()


