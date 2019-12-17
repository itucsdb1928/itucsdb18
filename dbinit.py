import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """
    
  CREATE TABLE IF NOT EXISTS Author( 
                      AuthorID SERIAL PRIMARY KEY , 
                      name VARCHAR(30) NOT NULL,
                      surname VARCHAR(30) NOT NULL,
                      birthDate DATE NOT NULL, 
                      numberOfbooks INTEGER NOT NULL,
                      country VARCHAR(40) NOT NULL
                     );
    CREATE TABLE IF NOT EXISTS BookComment( 
                      BookCommentID SERIAL PRIMARY KEY ,
                      UserRating INTEGER NOT NULL,
                      UserComment VARCHAR(500) NOT NULL,
                      CommentDate DATE NOT NULL,
                      DislikeNum INTEGER NOT NULL,
                      LikeNum INTEGER DEFAULT 0 NOT NULL
                     );
                     
    CREATE TABLE IF NOT EXISTS Publisher( 
                      PublisherID SERIAL PRIMARY KEY , 
                      name VARCHAR(40) NOT NULL, 
                      adress VARCHAR(50) NOT NULL,
                      numberOfbooks INTEGER NOT NULL, 
                      establishmentDate DATE NOT NULL,
                      companyName VARCHAR(50) NOT NULL
                     );
                     
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

    CREATE TABLE IF NOT EXISTS UserContent( 
                      UserContentID SERIAL PRIMARY KEY ,
                      UserID INTEGER REFERENCES Users (UserID)ON DELETE CASCADE,
                      CommentsNum INTEGER NOT NULL,
                      FavAuthor VARCHAR(20) NOT NULL,
                      FavBook VARCHAR(20) NOT NULL,
                      FavPublisher VARCHAR(20) NOT NULL,
                      LikedCommentNum INTEGER DEFAULT 0 NOT NULL
                     );
                     
    ALTER TABLE BookComment ADD COLUMN UserID INTEGER REFERENCES Users (UserID) ON DELETE CASCADE;
    ALTER TABLE BookComment ADD COLUMN BookID INTEGER REFERENCES Books (BookID) ON DELETE CASCADE;
    ALTER TABLE BookComment ALTER COLUMN DislikeNum SET DEFAULT 0; 
    ALTER TABLE BookComment ALTER COLUMN DislikeNum SET NOT NULL;
    ALTER TABLE UserContent ALTER COLUMN CommentsNum SET DEFAULT 0;
    ALTER TABLE UserContent ALTER COLUMN CommentsNum SET NOT NULL;
    
    """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
