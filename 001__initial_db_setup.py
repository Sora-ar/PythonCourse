import sqlite3

conn = sqlite3.connect('task3_db.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS banks(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY,
                bank_sender_name TEXT NOT NULL,
                account_sender_id INTEGER NOT NULL,
                bank_receiver_name TEXT NOT NULL,
                account_receiver_id INTEGER NOT NULL,
                sent_currency TEXT NOT NULL,
                sent_amount REAL NOT NULL,
                datetime TEXT
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                birth_day TEXT CHECK (birth_day LIKE '%.%.%'),
                accounts TEXT NOT NULL CHECK (accounts LIKE '%,%'),
                UNIQUE (name, surname)
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS accounts(
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('credit', 'debit')),
                account_number INTEGER NOT NULL UNIQUE,
                bank_id INTEGER NOT NULL,
                currency TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT CHECK (status IN ('gold', 'silver', 'platinum'))
                )''')

conn.commit()
cursor.close()
conn.close()
