# DOMETL (Python ETL Tool)
Dometl is a Python ETL package.

## Process

CSV -> Staging Table
by using the copy command

```
COPY st_game FROM '/path/to/csv/ZIP_CODES.txt' WITH (FORMAT csv);

psql -U postgres -h 127.0.0.1 -d nba -c "COPY st_game FROM 'C:\Users\Dominik\Documents\Projects\dometl\datasets\game_data\daily\20221105_g.csv' WITH (FORMAT csv)"
```

# Run a script (Stored Procedure) 
```
psql -U postgres -h 127.0.0.1 -d nba -f setup\db_setup\table_creation.sql
```
