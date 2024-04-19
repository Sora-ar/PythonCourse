import sqlite3

with sqlite3.connect('employees.db') as conn:
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS employees(
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        division TEXT NOT NULL,
                        salary INTEGER
                        )''')
    data = [('Bob', 'professor', 1234), ('Lulu', 'boss', 2345), ('Den', 'tutor', 120)]
    cursor.executemany("INSERT INTO  employees(name, division, salary) VALUES (?, ?, ?)", data)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.commit()
