DATA MODELING WITH POSTGRES
===========================

The project consists in creating a Postgres database with tables in order to optimize queries on song play analysis for a company called Sparkify. Furthermore, it entails creating a database schema and ETL pipeline. 

The repository for this project contains 3 important files (besides this one and the data folder, which contains the relevant JSON files, one for the user activity on the app and another with the metadata on the songs in the app):


sql_queries.py
-------------
This file is where all the SQL statements are.
## Drop Tables
These allow us to drop the created tables when necessary; 

## Create Tables
These are needed to create the tables in the database. Below you can find a definition of the tables.

**songplays**(***songplay_id*** serial, start_time varchar NOT NULL, user_id varchar NOT NULL, level varchar, song_id varchar, artist_id varchar, session_id varchar, location varchar, user_agent varchar) - information about the songs played in the app; This is the Fact table and songplay_id is the Primary Key 
**users**(***user_id*** varchar, first_name varchar, last_name varchar, gender varchar, level varchar) - information about the user's in the app; This is one of the Dimension tables and user_id is the Primary Key.
**songs**(***song_id*** varchar, title varchar, artist_id varchar NOT NULL, year varchar, duration varchar) - specific information about the songs, such as the tile, the artist, year of realease and the duration of the song; This is one of the Dimension tables and song_id is the Primary Key.
**artist**(***artist_id*** varchar, artist_name varchar, artist_location varchar, artist_latitude varchar, artist_longitude varchar) - specific information about the song's authors; This is one of the Dimension tables and artist_id is the Primary Key.
**time**(***start_time*** varchar, hour varchar, day varchar, week varchar, month varchar, year varchar, weekday varchar) - information about when the songs were played; This is one of the Dimension tables and start_time is the Primary Key.

## Insert Records
Allows us to insert the data into the above created records. 

## Find Songs - SELECT statement
This SELECT statement allows us to get both the song_id and the artist_id, which are needed when inserting data into the songplays table, since the log file does not have that information. Therefore, we will get that information by querying the songs and artists tables to find matches based on song title, artist name, and song duration time. 

**All these statements are then accessed in the create_tables.py file in order to perform all the desired actions**


create_tables.py 
----------------
Running this file allows us to both create the database we will be working on (sparkifydb) and the necessary tables (**songplays, users, songs, artists, time**) and also drop those same tables when needed. It does this by acessing the SQL statements defined in the sql_queries.py


etl.py
------
This is where the data in the JSON files in inserted into the created tables. The song_data is loaded into two different variables (song_data and artist_data) which are used to insert data into their respective tables (songs, artists). The log_data is also loaded into two different variables (time_data and user_df) which are also used to insert data into time and users tables, respectively.


The  are 2 remaining files. The file etl.ipynb was used as a guide to develop the final etl.py. The file test.ipnyb was used to test whether or not the data was correctly inserted into the respective tables.


SCHEMA
------

