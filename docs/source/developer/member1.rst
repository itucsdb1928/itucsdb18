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


Search book fuction:

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
