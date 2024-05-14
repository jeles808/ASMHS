import sqlite3

def init_db():
    conn = sqlite3.connect('Answers.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            Start TEXT,
            answer_1 TEXT,
            answer_2 TEXT,
            answer_3 TEXT,
            answer_4 TEXT,
            answer_5 TEXT,
            answer_6 TEXT,
            answer_7 TEXT,
            answer_8 TEXT,
            answer_9 TEXT,
            answer_10 TEXT,
            answer_11 TEXT,
            answer_12 TEXT,
            answer_13 TEXT,
            answer_14 TEXT,
            answer_15 TEXT,
            answer_16 TEXT,
            answer_17 TEXT
        )
    ''')
    conn.commit()
    conn.close()


def fetch_all_answers():
    conn = sqlite3.connect('answers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM answers")
    all_answers = cursor.fetchall()
    conn.close()
    return all_answers


def save_answers(user_id, Start, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7, answer_8,
                  answer_9, answer_10, answer_11, answer_12, answer_13, answer_14, answer_15, answer_16, answer_17):
    conn = sqlite3.connect('answers.db')
    c = conn.cursor()
    c.execute('INSERT INTO answers (user_id, Start, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7,'
              ' answer_8, answer_9, answer_10, answer_11, answer_12, answer_13, answer_14, answer_15,'
              ' answer_16, answer_17) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (user_id, Start, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6, answer_7, answer_8, answer_9,
               answer_10, answer_11, answer_12, answer_13, answer_14, answer_15, answer_16, answer_17))
    conn.commit()
    conn.close()
