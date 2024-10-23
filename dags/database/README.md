# Database writer

The database writer is currently the last stage of the pipeline.
The database instance is an Azure PostgerSQL, the config contains the functions used to establish the connection ti the Database.
The writeData.py contains the query genrator which only generates the queries for the articles, all articles will not have all the attributes in the database, that we need a query generator which will dynamically generate the INSERT query.

The writer also ignore articles already present in the DB , so that we do not add them twice