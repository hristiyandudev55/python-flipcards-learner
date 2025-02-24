# NOTES WHAT I DID ON 23/24 February:

1. **Migrated the database** from SQLite to PostgreSQL using _psycopg2-binary_.
* Created a migrate.load file, e.g.:
  
```
LOAD DATABASE
FROM sqlite:///Users/a516095/Documents/GitHub/flip-cards/python-flipcards-learner/flipcards.db
INTO postgresql://a516095@localhost/flipnlearn

WITH create tables,
     include drop,
     create indexes,
     reset sequences;
```
* Ran the migration using:
```
pgloader migrate.load
```
2. Tested both backend and frontend.

3. Automated tests to run on commit.

4. Created a script (./run.sh) to start the application.
