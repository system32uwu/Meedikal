import sqlite3
import os

if __name__ == '__main__':
    p = os.path.join(os.path.dirname(__file__))
    
    dbPath = f'{p}/../meedikal.db'
    schemaPath = f'{p}/meedikal.sql'

    if os.path.exists(dbPath):
        os.remove(dbPath)

    conn = sqlite3.connect(dbPath)

    schema = open(schemaPath, 'r').read()

    conn.cursor().executescript(schema)