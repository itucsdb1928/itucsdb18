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
