# %%
import sqlite3
from datetime import date

conn = sqlite3.connect('baza.db')
conn.execute("PRAGMA foreign_keys = 1")  # relations won't work without that
c = conn.cursor()


def creating_tables():
    """creating 3 tables with we will use in this database
    table students have 5 values:
    student_id: id from discord
    st_name, st_last_name,st_phone: personal information
    st_status: status if we still have lessons with this student or not

    table tutor have 3 values:
    tutor_id: tutor discord id
    tutor_name,tutor_last_name: presonal information

    table lessons have 5 values:
    lesson_id: id of lesson
    tutor_id: id of tutors who's have lesson
    student_id: id of student who's have lesson
    start_time: time and day when lesson started
    course_duration: how long lesson was"""
    c.execute('''
                CREATE TABLE students(
                student_id INTEGER PRIMARY KEY, 
                st_name TEXT, 
                st_last_name TEXT, 
                st_phone TEXT,
                st_discord TEXT, 
                st_status TEXT)
                ''')

    c.execute('''
                CREATE TABLE tutors(
                tutor_id  INTEGER PRIMARY KEY, 
                tutor_name TEXT, 
                tutor_last_name TEXT,
                tutor_discord TEXT)
                ''')

    c.execute("""
                CREATE TABLE lessons(
                lesson_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                tutor_id INTEGER , 
                student_id INTEGER ,
                start_day TIME, 
                course_duration REAL,
                FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE ,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE )
                """)
    conn.commit()


def add_student(st_name, st_last_name, st_phone, st_discord, st_status=""):
    tab = [st_discord.split('#')[1], st_name, st_last_name, st_phone, st_discord, st_status]

    c.execute(f"""
                    INSERT INTO students(student_id,st_name, st_last_name, st_phone, st_discord, st_status) 
                    VALUES (?,?,?,?,?,?)""", tab)
    conn.commit()


def add_tutor(name, last_name, tutor_discord):
    tab = [tutor_discord.split('#')[1], name, last_name, tutor_discord]
    c.execute(f'''INSERT INTO tutors(tutor_id,tutor_name, tutor_last_name, tutor_discord) VALUES 
                (?,?,?,?)''', tab)
    conn.commit()


def add_lesson(tutor_id, student_id, curse_duration=1.0, start_day=date.today()):
    tab = [tutor_id, student_id, curse_duration, start_day]
    c.execute(f"""
                INSERT INTO  lessons(tutor_id, student_id, course_duration, start_day)
                VALUES  (?,?,?,?)
                """, tab)
    conn.commit()


def show_students():
    c.execute(f"""
        SELECT * FROM students
        """)
    info = c.fetchall()
    conn.commit()
    return info


def show_my_students(tutor_id):
    c.execute(f"""
            SELECT st_name, st_last_name, st_phone, st_discord, st_status
            FROM lessons
            INNER JOIN students 
                ON students.student_id = lessons.student_id
            WHERE tutor_id = ?
            GROUP BY st_discord
            """, [tutor_id])

    info = c.fetchall()
    conn.commit()
    return info


def show_tutors():
    c.execute(f"""
        SELECT * FROM tutors
        """)
    info = c.fetchall()
    conn.commit()
    return info


def show_lessons(month):
    c.execute(f"""
        SELECT lesson_id, start_day, course_duration, st_name, st_last_name 
        FROM lessons
        INNER JOIN students 
                ON students.student_id = lessons.student_id
        WHERE start_day LIKE ?
        """, ["%-" + month + "-%"])
    info = c.fetchall()
    conn.commit()
    return info


def show_my_lesson(tutor_id, month=date.today().strftime("%m")):
    c.execute(f"""
            SELECT lesson_id, start_day, course_duration, st_name, st_last_name
            FROM lessons
            INNER JOIN students 
                ON students.student_id = lessons.student_id
            WHERE tutor_id = ? AND start_day LIKE ?
            ORDER BY start_day
            """, [tutor_id, "%-" + month + "-%"])

    info = c.fetchall()
    conn.commit()
    return info


def count_hours(tutor_id, month=date.today().strftime("%m")):
    c.execute(f"""
                SELECT st_discord,st_name, st_last_name, SUM(course_duration)
                FROM lessons
                INNER JOIN students 
                    ON students.student_id = lessons.student_id
                WHERE tutor_id = ? AND start_day LIKE ?
                GROUP BY st_discord
                """, [tutor_id, "%-" + month + "-%"])
    info = c.fetchall()
    conn.commit()
    return info


def change_lesson(tutor_id, student_id, lesson_id, date, time):
    c.execute('''
                UPDATE lessons
                SET student_id = ?,
                    start_day = ?,
                    course_duration = ?
                WHERE
                    tutor_id = ? AND lesson_id = ? AND student_id = ?
                
    ''', ([student_id, date, time, tutor_id, lesson_id, student_id]))
    conn.commit()


def change_student(st_discord, name, last_name, phone_nub, status):
    c.execute('''
            UPDATE students
            SET st_name = ?,
                st_last_name = ?,
                st_phone = ?,
                st_status = ?
            WHERE 
                student_id = ?
            ''', ([name, last_name, phone_nub, status, st_discord.split('#')[1]]))
    conn.commit()


def change_tutor(tutor_discord, name, last_name):
    c.execute('''
            UPDATE tutors
            SET tutor_name = ?,
                tutor_last_name = ?
            WHERE
                tutor_id = ?
            ''', ([tutor_discord.split('#')[1], name, last_name]))
    conn.commit()


def delete_student(st_discord):
    c.execute('''
            DELETE FROM students
            WHERE student_id = ? 
            ''', ([st_discord.split('#')[1]]))
    conn.commit()


def delete_tutor(tutor_discord):
    c.execute('''
            DELETE FROM tutors
            WHERE tutor_id = ?   
            ''', (tutor_discord.split('#')[1]))
    conn.commit()


if __name__ == '__main__':
    add_lesson("937", "6214", 2.4)
