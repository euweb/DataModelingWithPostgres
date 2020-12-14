import psycopg2
import os
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # read the database host from the environment variable DB_HOST or 
    # use localhost as default value if not present
    db_host = os.getenv('DB_HOST', 'localhost')
    # connect to default database
    conn = psycopg2.connect("host=%s dbname=studentdb user=student password=student" % db_host)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=%s dbname=sparkifydb user=student password=student" % db_host)
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    
    try:
        print('connecting to the database')
        cur, conn = create_database()
        print('dropping tables')
        drop_tables(cur, conn)
        print('creating tables')
        create_tables(cur, conn)
        print('finished')
    except psycopg2.Error as e: 
        print(e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()