import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE staging_events (
        event_id integer IDENTITY(0, 1),
        artist varchar(max),
        auth varchar(30),
        first_name varchar(30),
        gender varchar(20),
        item_in_session integer,
        last_name varchar(30),
        length float,
        level varchar(30),
        location varchar(max),
        method varchar(20),
        page varchar(20),
        registration bigint,
        session_id integer,
        song varchar(max),
        status integer,
        ts bigint, 
        user_agent varchar(max),
        user_id varchar(20))
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs (
        num_songs integer,
        artist_id varchar(30),
        artist_latitude float,
        artist_longitude float,
        artist_location varchar(max),
        artist_name varchar(max),
        song_id varchar(30),
        title varchar(max),
        duration float,
        year integer)
""")

songplay_table_create = ("""
    CREATE TABLE songplays(
    songplay_id integer IDENTITY(0,1) PRIMARY KEY,
    start_time timestamp NOT NULL,
    user_id varchar(30) NOT NULL,
    level varchar(30),
    song_id varchar(30) NOT NULL,
    artist_id varchar(30) NOT NULL,
    session_id integer NOT NULL,
    location varchar(max),
    user_agent varchar(max))""")

user_table_create = ("""
    CREATE TABLE users(
    user_id varchar(30) PRIMARY KEY,
    first_name varchar(30),
    last_name varchar(30),
    gender varchar(20),
    level varchar(30))""")

song_table_create = ("""
    CREATE TABLE songs(
    song_id varchar(30) PRIMARY KEY,
    title varchar(max),
    artist_id varchar(30) NOT NULL,
    year integer,
    duration float)""")

artist_table_create = ("""
    CREATE TABLE artists(
    artist_id varchar(30) PRIMARY KEY,
    name varchar(max),
    location varchar(max),
    latitude float,
    longitude float)""")

time_table_create = ("""
    CREATE TABLE time(
    start_time timestamp PRIMARY KEY,
    hour integer,
    day integer,
    week integer,
    month integer,
    year integer,
    weekday integer)""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {} 
    iam_role {}
    json {}
    region 'us-west-2'
    """).format(config.get('S3', 'LOG_DATA'), config.get('IAM_ROLE', 'ARN'),  config.get('S3', 'LOG_JSONPATH'))
                       
staging_songs_copy = ("""
    copy staging_songs from {} 
    iam_role {}
    format as json 'auto'
    region 'us-west-2'
    """).format(config.get('S3', 'SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays(
    start_time,
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent)
    SELECT
    timestamp 'epoch' + stev.ts/1000 * interval '1 second' AS start_time,
    stev.user_id AS user_id,
    stev.level AS level,
    stsongs.song_id AS song_id,
    stsongs.artist_id AS artist_id,
    stev.session_id AS session_id,
    stev.location AS location,
    stev.user_agent AS user_agent
    FROM staging_events stev
    JOIN staging_songs stsongs
    ON stev.artist=stsongs.artist_name AND stev.length=stsongs.duration AND stev.song=stsongs.title
    WHERE stev.page = 'NextSong'
""")

user_table_insert = ("""
    INSERT INTO users(
    user_id,
    first_name,
    last_name,
    gender,
    level)
    SELECT DISTINCT
    stev.user_id AS user_id,
    stev.first_name AS first_name,
    stev.last_name AS last_name,
    stev.gender AS gender,
    stev.level AS level
    FROM staging_events stev
""")

song_table_insert = ("""
    INSERT INTO songs(
    song_id,
    title,
    artist_id,
    year,
    duration)
    SELECT DISTINCT
    song_id,
    title,
    artist_id,
    year,
    duration
    FROM staging_songs
""")

artist_table_insert = ("""
    INSERT INTO artists(
    artist_id,
    name,
    location,
    latitude,
    longitude)
    SELECT DISTINCT
    artist_id,
    artist_name AS name,
    artist_location AS location,
    artist_latitude AS latitude,
    artist_longitude AS longitude
    FROM staging_songs
""")

time_table_insert = ("""
    INSERT INTO time(
    start_time,
    hour,
    day,
    week,
    month,
    year,
    weekday)
    SELECT
    sp.start_time,
    extract(hour from sp.start_time),
    extract(day from sp.start_time),
    extract(week from sp.start_time),
    extract(month from sp.start_time),
    extract(year from sp.start_time),
    extract(weekday from sp.start_time)
    FROM songplays sp   
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
