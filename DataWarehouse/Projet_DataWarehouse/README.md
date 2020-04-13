DATA WAREHOUSE
===========================

The project consists in building an ETL pipeline that extracts Sparkify's data from S3, stages it in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

The repository for this project contains 4 important files:

dwh.cfg
-------
In this file we add redshift database details and IAM role info.

sql_queries.py
-------------
This file is where all the SQL statements are. The first step is to read the details in dwh.cfg, which will allow us to connect to cluster created in AWS.

## Drop Tables
These allow us to drop the created tables when necessary; 

## Create Tables
These are needed to create the tables in the database. Below you can find a definition of the tables.

**staging_events**(event_id identity, artist varchar, auto varchar, first_name varchar, gender varchar, item_in_session integer, last_name varchar, length float, level varchar, location varchar, method varchar, page varchar, registration bigint, session_id integer, song varchar, status integer, ts bigint, user_agent varchar, user_id varchar) 
**staging_songs**(num_songs integer, artist_id varchar, artist_latitude float, artist_longitude float, artist_location varchar, artist_name varchar, song_id varchar, title varchar, duration float, year integer) 

These first two tables are staging tables. Staging area is a place where you hold temporary tables on data warehouse server. Staging tables are connected to work area or fact tables. We basically need staging area to hold the data, and perform data cleansing and merging, before loading the data into warehouse

**songplays**(***songplay_id*** identity, start_time timestamp NOT NULL, user_id varchar NOT NULL, level varchar, song_id varchar NOT NULL, artist_id varchar NOT NULL, session_id integer NOT NULL, location varchar, user_agent varchar) - information about the songs played in the app; This is the Fact table and songplay_id is the Primary Key.
**users**(***user_id*** varchar, first_name varchar, last_name varchar, gender varchar, level varchar) - information about the user's in the app; This is one of the Dimension tables and user_id is the Primary Key.
**songs**(***song_id*** varchar, title varchar, artist_id varchar NOT NULL, year integer, duration float) - specific information about the songs, such as the tile, the artist, year of realease and the duration of the song; This is one of the Dimension tables and song_id is the Primary Key.
**artist**(***artist_id*** varchar, name varchar, location varchar, latitude float, longitude float) - specific information about the song's authors; This is one of the Dimension tables and artist_id is the Primary Key.
**time**(***start_time*** timestamp, hour integer, day integer, week integer, month integer, year integer, weekday integer) - information about when the songs were played; This is one of the Dimension tables and start_time is the Primary Key.

## COPY Statements
These allow us to copy the tables from the staging area into the desired cluster. For this it is important to make sure that the ARN under IAM_ROLE in the dwh.cfg file is substituted with the correct value.

## Insert Records
Allows us to insert the data into the final tables (songplays, users, songs, artists and time, using the staging tables for this goal). 


**All these statements are then accessed in the create_tables.py file in order to perform all the desired actions**


create_tables.py 
----------------
Running this file allows us to both create the necessary tables (**songplays, users, songs, artists, time**) and drop those same tables when needed. It also connects to the created cluster. It does this by acessing the SQL statements defined in the sql_queries.py


etl.py
------
hese allow us to load data from S3 to staging tables on Redshift and then from staging tables to analytics tables on Redshiftcopy the tables from the staging area into the desired cluster.
For this we use the COPY statements in sql_queries.py 



