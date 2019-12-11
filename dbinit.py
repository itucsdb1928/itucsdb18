import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """
    CREATE TABLE Author( 
                      AuthorID SERIAL PRIMARY KEY , 
                      name VARCHAR(30), 
                      surname VARCHAR(30),
                      birthDate DATE , 
                      numberOfbooks INTEGER,
                      country VARCHAR(40)
                     );
    CREATE TABLE BookRewiev( 
                      BookRewievID SERIAL PRIMARY KEY ,
                      review INTEGER DEFAULT 0,
                      UserRating INTEGER,
                      UserComment VARCHAR(500),
                      CommentDate DATE 
                     );
                     
    CREATE TABLE Publisher( 
                      PublisherID SERIAL PRIMARY KEY , 
                      name VARCHAR(40), 
                      adress VARCHAR(50),
                      numberOfbooks INTEGER , 
                      establishmentDate DATE ,
                      companyName VARCHAR(50)
                     );
                     
    CREATE TABLE Books( 
                      BookID SERIAL PRIMARY KEY , 
                      Title VARCHAR(20),
                      PostDate  DATE,
                      PageNum INTEGER,
                      BookRewiev INTEGER REFERENCES BookRewiev (BookRewievID) , 
                      PublisherID INTEGER REFERENCES Publisher (PublisherID), 
                      AuthorID INTEGER REFERENCES Author (AuthorID) ,
                      Content VARCHAR(500)
                     );  
                    
                                          
    CREATE TABLE UserContent( 
                      UserContentID SERIAL PRIMARY KEY , 
                      VoteNum INTEGER,        
                      CommentsNum INTEGER,
                      FavAuthor VARCHAR(20),
                      FavBook VARCHAR(20),
                      FavPublisher VARCHAR(20)
                     );
                     
    CREATE TABLE Users( 
                      UserID SERIAL PRIMARY KEY, 
                      name VARCHAR (50)  NOT NULL, 
                      surname VARCHAR (50)  NOT NULL, 
                      gender VARCHAR (6) NULL, 
                      age VARCHAR (3) NULL,
                      content INTEGER REFERENCES UserContent (UserContentID),
                      email VARCHAR (50) UNIQUE NOT NULL,
                      password VARCHAR (20)  NOT NULL,
                      isAdmin INTEGER
                     );

    ALTER TABLE BookRewiev ADD COLUMN UserID INTEGER REFERENCES Users (UserID);
    ALTER TABLE BookRewiev ADD COLUMN BookID INTEGER REFERENCES Books (BookID);       
    
    INSERT INTO Users (name,surname, email,password,isAdmin) 
    VALUES ('admin','admin','admin@gmail.com', 'admin',1);
    INSERT INTO Users (name, surname, gender, age, email, password)
    VALUES ('Barclay', 'Miell', 'Male', 52, 'bmiell3@sfgate.com', 'jp7PDwLdq');
    INSERT INTO Users (name, surname, gender, age, email, password)
    VALUES ('Stephenie', 'Mackie', 'Female', 39, 'smackie4@ebay.co.uk', 'oHjvgA');
    INSERT INTO Users (name, surname, gender, age, email, password)
    VALUES ('Hewett', 'Grushin', 'Male', 24, 'hgrushin5@state.gov', '05JJUHZzbm');
    INSERT INTO Users (name, surname, gender, age, email, password)
    VALUES ('L;urette', 'O''Cassidy', 'Female', 51, 'locassidy6@4shared.com', 'JNskYpdg');
    INSERT INTO Users (name, surname, gender, age, email, password)
    VALUES ('Vidovic', 'Avesque', 'Male', 34, 'vavesque7@amazon.com', '3Em8lAq60');

   
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Asoka', '96064 Norway Maple Hill', 31, '1/21/1977', 'Cassin LLC');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Overhold', '03 Oneill Alley', 70, '10/10/1961', 'Ankunding, Macejkovic and Hansen');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Veribet', '99353 Bashford Drive', 27, '8/2/1967', 'Boyle, McCullough and Macejkovic');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Guipy', '7654 Fisk Pass', 42, '9/17/1979', 'Mann Group');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Apqru', '8 Tony Court', 48, '1/5/2002', 'Kris Group');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Zamit', '20 Becker Plaza', 22, '10/24/1970', 'Jerde Group');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Pannier', '3152 Dayton Alley', 72, '11/1/2005', 'Hettinger, Price and Schuster');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Ventosanzap', '589 Fallview Lane', 83, '11/11/2005', 'Jones, Gorczany and Zemlak');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Latlux', '064 Pine View Crossing', 26, '11/23/1996', 'Feeney, Jast and Zboncak');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Bigtax', '41 Sachs Way', 79, '7/13/1976', 'Renner-Osinski');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Namfix', '034 Dorton Center', 27, '11/22/1992', 'McKenzie-Donnelly');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Duobam', '6697 Armistice Parkway', 78, '6/9/2008', 'Hessel, Hirthe and Schinner');
INSERT INTO Publisher (name, adress, numberOfbooks, establishmentDate, companyName) VALUES ('Alpha', '212 Nevada Junction', 49, '3/10/1971', 'Mraz LLC');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Maryann', 'Golsby', '10/25/1913', 4, 'Poland');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Linnie', 'Lincke', '2/6/1942', 12, 'China');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Gearalt', 'Bangiard', '11/24/1929', 23, 'Indonesia');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Bron', 'Froment', '8/23/1918', 1, 'Japan');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Burr', 'Woodroff', '8/9/1957', 10, 'Togo');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Britteny', 'Suett', '4/29/1948', 21, 'Thailand');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Pavel', 'Vickar', '1/2/1923', 14, 'Malaysia');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Elfrieda', 'Goligly', '10/28/1946', 25, 'Afghanistan');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Launce', 'Lodemann', '3/27/1957', 18, 'Suriname');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Clayborn', 'Souley', '10/15/1934', 19, 'China');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Petra', 'Simonian', '2/7/1959', 7, 'Norway');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Donetta', 'Webbe', '12/19/1915', 3, 'China');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Evanne', 'Stratford', '12/10/1931', 8, 'Indonesia');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Moll', 'Palley', '11/25/1939', 18, 'Colombia');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Ramon', 'Arzu', '1/16/1932', 21, 'Bulgaria');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Carlie', 'Sikorski', '9/26/1919', 17, 'Serbia');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Enid', 'Boddis', '10/22/1918', 21, 'China');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Toiboid', 'Tassel', '9/4/1977', 23, 'Sweden');
INSERT INTO Author (name, surname, birthDate, numberOfbooks, country) VALUES ('Piotr', 'Cheetam', '10/5/1973', 22, 'Norway');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Y-find', 206, 13, 19, 'In hac habitasse platea dictumst.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Job', 631, 12, 18, 'Suspendisse potenti.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Voltsillam', 825, 11, 17, 'In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Stronghold', 171, 10, 16, 'Donec posuere metus vitae ipsum.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Alrhagap', 214, 9, 15, 'Suspendisse potenti.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Qwoesam', 553, 8, 14, 'Nam dui.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Hatity', 235, 7, 13, 'Curabitur at ipsum ac tellus semper interdum.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Zoolab', 224, 6, 12, 'Morbi a ipsum.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Ronstring', 455, 5, 11, 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Bitchip', 841, 4, 10, 'Proin interdum mauris non ligula pellentesque ultrices.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Otcom', 731, 3, 9, 'Aenean sit amet justo.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Daltfresh', 716, 2, 8, 'Curabitur convallis.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Sonair', 637, 1, 7, 'Etiam faucibus cursus urna.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Kanlam', 814, 13, 6, 'Etiam faucibus cursus urna.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Transcof', 240,12, 5, 'Sed ante.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Karqwe', 459, 10, 3, 'Nulla mollis molestie lorem.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Subin', 225, 9, 2, 'Maecenas ut massa quis augue luctus tincidunt.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Rank', 589, 8, 1, 'Fusce consequat.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Bitwolf', 575, 7, 19, 'Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Lotstring', 525, 6, 18, 'Quisque id justo sit amet sapien dignissim vestibulum.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Domainer', 801, 5, 17, 'Phasellus in felis.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Stringtough', 331, 4, 16, 'Suspendisse potenti.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Quo Lux', 780, 2, 14, 'In congue.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Konklux', 227, 1, 13, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nulla dapibus dolor vel est.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Span', 219, 13, 12, 'Aliquam non mauris.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Cookley', 833, 12, 11, 'Aliquam erat volutpat.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Betaqr', 223, 10, 9, 'Proin eu mi.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Gembucket', 548, 8, 7, 'Duis consequat dui nec nisi volutpat eleifend.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Doamr', 732, 7, 6, 'Morbi non quam nec dui luctus rutrum.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Biodex', 845, 5, 4, 'Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Wrapsafe', 691, 4, 3, 'Fusce consequat.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES (Harmit', 641, 3, 2, 'Morbi non quam nec dui luctus rutrum.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Tempsoft', 655, 2, 1, 'Donec quis orci eget orci vehicula condimentum.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Viva', 382,1, 19, 'Nullam molestie nibh in lectus.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Bryom', 177, 13, 18, 'Nulla tempus.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Flowdesk', 579, 12, 17, 'Proin leo odio, porttitor id, consequat in, consequat ut, nulla.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Tresom', 218, 11, 16, 'In hac habitasse platea dictumst.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Sonsing', 649, 10, 15, 'Duis mattis egestas metus.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Scanniery', 738, 9, 14, 'Curabitur in libero ut massa volutpat convallis.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Zontrax', 327, 8, 13, 'Nulla facilisi.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Treeflex', 221, 7, 12, 'Cras non velit nec nisi vulputate nonummy.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Sonair', 361, 6, 11, 'Integer a nibh.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Flooweyt', 709, 3, 8, 'Nullam molestie nibh in lectus.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Planetq', 819, 2, 7, 'Integer a nibh.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Cardguard', 577, 1, 6, 'In hac habitasse platea dictumst.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Konklab', 492, 13, 5, 'Aliquam sit amet diam in magna bibendum imperdiet.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Bamity', 603, 12, 4, 'Integer tincidunt ante vel ipsum.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Bytecard', 856, 11, 3, 'Nunc rhoncus dui vel sem.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Fixflex', 305, 9, 1, 'Mauris lacinia sapien quis libero.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Zaam-Dox', 641, 8, 19, 'Integer non velit.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Prodder', 399, 7, 18, 'Nulla suscipit ligula in lacus.');
INSERT INTO Books (Title, PageNum, PublisherID, AuthorID, Content) VALUES ('Ronstring', 251, 6, 17, 'Duis at velit eu est congue elementum.');


INSERT INTO bookrewiev (UserID,BookID,UserRating,UserComment,commentdate) VALUES (1, 1 ,2,'kotu','1/21/2019');
INSERT INTO bookrewiev (UserID,BookID,UserRating,UserComment,commentdate) VALUES (2, 1 ,3,'idare eder','9/19/2019');
INSERT INTO bookrewiev (UserID,BookID,UserRating,UserComment,commentdate) VALUES (1, 2 ,4,'idare eder','11/15/2019');
INSERT INTO bookrewiev (UserID,BookID,UserRating,UserComment,commentdate) VALUES (2, 2 ,5,'cok ii','11/30/2019');


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
