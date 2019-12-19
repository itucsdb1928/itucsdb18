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