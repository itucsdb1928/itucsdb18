import psycopg2 as dbapi2
import psycopg2.extras
from datetime import date
from cyripto import Crypto


class Database:
    def __init__(self):
        # This one going to be environment variable in heroku
        self.url = "postgres://iedbwmwpyqzhkn:03e3f46bbea9aa0ece8e4e0f02873d2406203138589f1e51f5a42df6458e0cf5@ec2-107-22-234-103.compute-1.amazonaws.com:5432/d8g4sg1e98t5p7"
        self.crt = Crypto()
        self.UserId = 0
        self.book_name = None
        self.book_detail = None
    
    def get_home_page(self):
       with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "SELECT Books.Title,Books.content,Books.BookReview FROM Books,Author,Publisher  WHERE Books.PublisherID=Publisher.PublisherID AND Books.AuthorID=Author.AuthorID ORDER BY bookid"
           cursor.execute(query)
           home = cursor.fetchall()
           cursor.close()
           
       return home

    # def update_rewiev(self,Bookid):
    #     with self.con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    #         query = ""
    #         cursor.execute(query)


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

    def delete_book(self, bookid):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM BookComment WHERE BookID={};".format(bookid)
            cursor.execute(query)
            query = "DELETE FROM Books WHERE BookID={};".format(bookid)
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
           query = "SELECT * FROM Users WHERE UserID={}".format(UserId)
           cursor.execute(query)
           profile = cursor.fetchall()
           cursor.close()

        return profile

    def edit_profile(self,name,surname, age, gender, email, Userid):
        with dbapi2.connect(self.url) as connection:
           cursor = connection.cursor()
           query = "UPDATE Users SET name='{}',surname='{}',age={},gender='{}',email='{}'WHERE UserID={};".format(name, surname, age, gender, email, Userid)
           cursor.execute(query)
           cursor.close()

    def delete_profile(self, Userid):
        with dbapi2.connect(url) as connection:
           cursor = connection.cursor()
           query = "DELETE FROM BookComment WHERE UserID={};".format(Userid)
           cursor.execute(query)
           query = "DELETE FROM Users WHERE UserID={};".format(Userid)
           cursor.execute(query)
           cursor.close()

    #def getNumberOfbookReview(self,book_name):
    #    with dbapi2.connect(self.url) as connection:
    #        cursor = connection.cursor()
    #        query = "SELECT Books.BookID From Books Where Books.Title='{}';".format(book_name)
    #        cursor.execute(query)
    #        BookCommentid=cursor.fetchone()
    #        cursor.close()
    #       return BookCommentid[0]

    #def update_review(self,BookCommentid):
    #    with dbapi2.connect(self.url) as connection:
    #        cursor = connection.cursor()
    #        query = "UPDATE BookComment SET review=review+1 WHERE BookCommentID={};".format(BookCommentid)
    #        cursor.execute(query)
    #        cursor.close()

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

                return info[0]

        return 0

    def insertRate(self,userId,bookId,form,today):
        info = None
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
                query = "UPDATE UserContent SET LikedCommnetNum = LikedCommnetNum+1 WHERE UserID=%s"%(userId)
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