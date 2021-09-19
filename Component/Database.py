import sqlite3


def checkSetup():
    conn = sqlite3.connect('timetabler.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rooms'")
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    return True


def setup():
    conn = sqlite3.connect('timetabler.db')
    cursor = conn.cursor()

    create_rooms_table = """
        CREATE TABLE IF NOT EXISTS rooms (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          capacity INTEGER NOT NULL,
          type TEXT NOT NULL
        )
    """
    create_teachers_table = """
        CREATE TABLE IF NOT EXISTS teachers (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          dept TEXT NOT NULL,
          title TEXT NOT NULL
        )
    """
    create_courses_table = """
        CREATE TABLE IF NOT EXISTS courses (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          code TEXT NOT NULL,
          teachers TEXT NOT NULL,
          rooms TEXT NOT NULL,
          type TEXT NOT NULL,
          hours REAL NOT NULL,
          credit INTEGER NOT NULL
        )
    """
    create_semesters_table = """
        CREATE TABLE IF NOT EXISTS semesters (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          dept TEXT NOT NULL,
          students INTEGER NOT NULL,
          courses TEXT NOT NULL
        )
    """
    create_results_table = """
        CREATE TABLE IF NOT EXISTS results (
          id INTEGER PRIMARY KEY,
          content BLOB NOT NULL,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    cursor.execute(create_rooms_table)
    cursor.execute(create_teachers_table)
    cursor.execute(create_courses_table)
    cursor.execute(create_semesters_table)
    cursor.execute(create_results_table)
    conn.commit()
    conn.close()


def getConnection():
    return sqlite3.connect('timetabler.db')
