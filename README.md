# DataModelingWithPostgres

This project allows Sparkify employees to get analytics from the usage of their app. Since the data is stored in JSON files there is no easy way to query their data.
For this purpose a relational database and its schema should be created and an ETL pipeline should be developed to import the JSON files into the database.

## Description

We use a star schema which is optimized for queries on the song play analysis. For the data consistency we define constraints such as foreign keys or not null values. We use python programming language to implement the automated database creation and the running of ETL process / pipeline. There are two types of JSON files containing song data (artist and song data) and song play data (song plays and user information). We use jupyter lab for development of our ETL pipeline and transfer later the code to the python source file.

We use Docker to create the necessary infrastructure for database, jupyter lab and a tool for managing database content. 

## Database schema and ER Diagram

```sql
CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY, 
    first_name varchar NOT NULL,
    last_name varchar NOT NULL, 
    gender varchar(1) NOT NULL,
    level varchar NOT NULL
)

CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY,
    title varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    year int,
    duration numeric,
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id)
)

CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY,
    name varchar NOT NULL,
    location varchar, 
    latitude float, 
    longitude float
)

CREATE TABLE IF NOT EXISTS time (
    start_time timestamp PRIMARY KEY, 
    hour int, 
    day int,
    week int, 
    month int,
    year int, 
    weekday int
)

CREATE TABLE IF NOT EXISTS songplays(
    songplay_id SERIAL PRIMARY KEY, 
    start_time timestamp NOT NULL, 
    user_id int NOT NULL, 
    level varchar NOT NULL, 
    song_id varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    session_id int, 
    location varchar, 
    user_agent varchar,
    FOREIGN KEY (start_time) REFERENCES time (start_time),
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (song_id) REFERENCES songs (song_id)
)
```

![ER Diagram](https://github.com/euweb/DataModelingWithPostgres/blob/main/DataModelingWithPostgres.png?raw=true)
 
## Running using Docker

1. clone this repository
2. run `docker-compose up`
3. start jupyter lab:
    - search in the terminal for connection url like `http://127.0.0.1:8888/?token=f4a438dfe17abe6a80b098d08249b55700f79613ecc7a7da`
    - run _InstallDependencies.ipynb_ notebook to install required dependencies
    - run `python create_tables.py`
    - run `python etl.py`
4. start Adminer:
    - url `http://localhost:8080/`
        - data base: _PostgreSQL_
        - host: _db_
        - user: _student_
        - passwort: _student_
        - database: sparkifydb
    - navigate to tables

## Running without Docker

If postgres and python are installed localy, you can run this project without docker

1. clone this repository
2. create database _studentdb_ and give user _student_ identified by _student_ password access to it
3. run `python create_tables.py`
4. run `python etl.py`

## File list

| Name                      	| Description                                                    	|
|---------------------------	|----------------------------------------------------------------	|
| data                      	| Folder containing JSON files                                   	|
| create_tables.py          	| (re)creates tables in the database                             	|
| Dashboard.ipyng           	| contains simple example of querieng the database               	|
| docker-compose.yml        	| composer file to start docker container                        	|
| etl.ipyng                 	| notebook to develop the etl pipeline                           	|
| etl.py                    	| etl pipeline                                                   	|
| InstallDependencies.ipyng 	| notebook to install nesessary python modules                   	|
| README.md                 	| this documenation                                              	|
| sql_queries.py            	| python file with sql queries for create tables and ets scripts 	|
| test.ipyng                	| notebook dumping first 5 rows of each sql tables               	|

