import sqlite3
import os

p = os.path.join(os.path.dirname(__file__))
    
dbPath = f'{p}/../meedikal.db'

getDb = lambda: sqlite3.connect(dbPath, check_same_thread=False)

if __name__ == '__main__':
    
    schemaPath = f'{p}/meedikal.sql'

    if os.path.exists(dbPath):
        os.remove(dbPath)

    schema = open(schemaPath, 'r').read()

    getDb().cursor().executescript(schema)