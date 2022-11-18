import os
import psycopg2

# connect to default database
conn = psycopg2.connect("host=127.0.0.1 dbname=nba user=postgres password=password")
conn.set_session(autocommit=True)
cur = conn.cursor()

# create sparkify database with UTF8 encoding
path_to_csv = 'C:\\Users\\Dominik\\Documents\\Projects\\dometl\\datasets\\game_data\\daily\\20221105_g.csv'
with open(path_to_csv, "r") as f:
    cur.copy_from(f, "st_game", sep=',')

# cur.execute(f"COPY st_game FROM '{path_to_csv}' WITH (FORMAT csv)")

# close connection to default database\
conn.close()    