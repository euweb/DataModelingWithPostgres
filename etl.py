import glob
import os

import pandas as pd
import psycopg2

from sql_queries import (artist_table_insert, song_select, song_table_insert,
                         songplay_table_insert, time_table_insert,
                         user_table_insert)


def process_song_file(cur, filepath):
    """
    Description: This function is responsible for extracting artist and song data from
    the given json file and for saving it to the database.

    Arguments:
        cur: the cursor object.
        filepath: log data or song data file path.
 
    Returns:
        None
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert artist record
    df['artist_latitude'] = df['artist_latitude'].fillna(-1)
    df['artist_longitude'] = df['artist_longitude'].fillna(-1)
    artist_data = df[['artist_id', 'artist_name', 'artist_location',
                      'artist_latitude', 'artist_longitude']].values
    artist_data = artist_data.tolist()[0]

    cur.execute(artist_table_insert, artist_data)

    # insert song record
    song_data = df[['song_id', 'title',
                    'artist_id', 'year', 'duration']].values
    song_data = song_data.tolist()[0]

    cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    """
    Description: This function is responsible for extracting songplay and user data from
    the given json file and for saving it to the database. Entries for the time table are generated and
    appropriate artist and song ids are retrieved and evaluated. 

    Arguments:
        cur: the cursor object.
        filepath: log data or song data file path.
 
    Returns:
        None
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page.eq('NextSong')]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time = pd.Series(t).dt
    time_data = (df['ts'], time.hour, time.day, time.week,
                 time.month, time.year, time.dayofweek)
    column_labels = ('start_time', 'hour', 'day',
                     'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(list(time_data), list(column_labels)).T

    for _, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName',
                  'gender', 'level']].copy().drop_duplicates()

    # insert user records
    for _, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for _, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            
            songid, artistid = results
            
            # insert songplay record
            songplay_data = (row.ts, row.userId, row.level, songid,
                         artistid, row.sessionId, row.location, row.userAgent)

            cur.execute(songplay_table_insert, songplay_data)

        #else:
        #    print("unknown song: {} ({})".format(row.song, row.artist))
        


def process_data(cur, conn, filepath, func):
    """
    Description: This function is responsible for listing the files in a directory,
    and then executing the ingest process for each file according to the function
    that performs the transformation to save it to the database.

    Arguments:
        cur: the cursor object.
        conn: connection to the database.
        filepath: log data or song data file path.
        func: function that transforms the data and inserts it into the database.

    Returns:
        None
    """

    # get all files matching extension from directory
    all_files = []
    for root, _, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Establishes connection with the sparkify database and gets
    cursor to it.  

    - Drops all the tables.  

    - Creates all tables needed. 

    - Finally, closes the connection. 
    """
    db_host = os.getenv('DB_HOST', 'localhost')
    conn = psycopg2.connect(
        "host=%s dbname=sparkifydb user=student password=student" % db_host)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
