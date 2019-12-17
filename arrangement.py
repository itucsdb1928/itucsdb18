import psycopg2 as dbapi2

from cyripto import Crypto


class Database:
    def __init__(self):
        # This one going to be environment variable in heroku
        self.url = "postgres://klnslbgroolcmt:6e4c28e765ba63b0f5bb9acaa3403e47e4cff7b7b3b48bb8eee78291f47b711a@ec2-174-129-255-46.compute-1.amazonaws.com:5432/d9ej37pubfqund"
        self.crt = Crypto()
        self.UserId = 0
        self.book_name = None
        self.book_detail = None
        self.author_details=None
        self.publisher_details=None
        self.publishers=self.all_publishers()
        self.authors=self.all_authors()
    
    def all_publishers(self):

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "SELECT DISTINCT Publisher.name,Publisher.PublisherID FROM Publisher;"
            cursor.execute(query)
            publishers = cursor.fetchall()
            cursor.close()

        return publishers

    def all_authors(self):

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "SELECT DISTINCT Author.name,Author.surname,Author.AuthorID FROM Author;"
            cursor.execute(query)
            authors = cursor.fetchall()
            cursor.close()

        return authors

    def get_home_page(self):
       with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "SELECT Books.Title,Books.content,Books.BookReview,Books.PostDate FROM Books,Author,Publisher  WHERE Books.PublisherID=Publisher.PublisherID AND Books.AuthorID=Author.AuthorID ORDER BY Books.BookReview DESC"
           cursor.execute(query)
           home = cursor.fetchall()
           cursor.close()
           
       return home



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


    def show_publisher_detail(self,publisherName):

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "SELECT DISTINCT Publisher.adress,Publisher.numberOfbooks,Publisher.establishmentDate,Publisher.companyName,Publisher.publisherid FROM Publisher,Books WHERE Publisher.publisherid=Books.publisherid AND Publisher.name='%s' ;" % (publisherName)
            cursor.execute(query)
            publisherDetails=cursor.fetchone()
            cursor.close()
            return publisherDetails

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

    def delete_author(self, authorid):

        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Author WHERE AuthorID={};".format(authorid)
            cursor.execute(query)
            cursor.close()

    def delete_book(self, bookid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BookComment WHERE BookID={};".format(bookid)
            cursor.execute(query)
            query = "DELETE FROM Books WHERE BookID={};".format(bookid)
            cursor.execute(query)
            cursor.close()

    def add_new_book(self,title, postdate, PageNum, content, authorid, publisherid):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Books (Title, PostDate,PageNum,Content,AuthorID, PublisherID ) VALUES ('{}', '{}', {}, '{}',{},{} );".format(title, postdate, PageNum, content, authorid, publisherid)

            cursor.execute(query)
            cursor.close()


    def Search(self,name):
       with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "SELECT Books.Title,Books.content FROM Books,Author,Publisher  WHERE Books.PublisherID=Publisher.PublisherID AND Books.AuthorID=Author.AuthorID AND Books.Title LIKE '%%%s%%' "%(name)
           cursor.execute(query)
           search = cursor.fetchall()
           cursor.close()

       return search

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

    def edit_profile(self,name,surname, age, gender, email, Userid):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "UPDATE Users SET name='{}',surname='{}',age={},gender='{}',email='{}'WHERE UserID={};".format(name, surname, age, gender, email, Userid)
           cursor.execute(query)
           cursor.close()

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

    def edit_user_content(self,fav_author,fav_book,fav_publisher):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "UPDATE USERCONTENT SET favauthor='{}',favbook='{}',favpublisher='{}'WHERE UserID={};".format(fav_author,fav_book,fav_publisher,self.UserId)
           cursor.execute(query)
           cursor.close()

    def delete_user_content(self):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "DELETE FROM UserContent WHERE UserID={};".format(self.UserId)
           cursor.execute(query)
           cursor.close()

    def NewContent(self,form):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO UserContent (FavAuthor,FavBook,FavPublisher,UserID) VALUES ('%s','%s','%s',%d);" % (
            form.book.data, form.publisher.data, form.author.data,self.UserId)
            cursor.execute(query)
            cursor.close()

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
                query = "INSERT INTO UserContent (userid) VALUES ('%s');" %(userId)
                cursor.execute(query)
                cursor.close()

        return userId

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

    def checkUser(self,userId,bookId):
        info = None

        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "SELECT userid FROM BookComment where userid = '%d' and bookid = %d" %(userId,bookId)
           cursor.execute(query)
           info = cursor.fetchone()
           cursor.close()
        if info is None:
           return True
        
        return False


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

    def updateBookContent(self,bookId,newComment):
        info = None
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "UPDATE books SET content = '%s' WHERE bookid = %d" %(newComment,bookId)
           cursor.execute(query)
           cursor.close()

    
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

    def delete_comment(self,bookId):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM bookcomment WHERE userid={} and bookid={};".format(self.UserId,bookId)
            cursor.execute(query)
            cursor.close()