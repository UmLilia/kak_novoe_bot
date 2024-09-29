import sqlite3

db = sqlite3.connect('/data/db.sqlite3', check_same_thread=False)
sql = db.cursor()


def new_user(user):
    sql.execute(
        ('INSERT INTO api_users (id, username, first_name, last_name)'
         ' VALUES (?, ?, ?, ?)'),
        (user.id, user.username, user.first_name, user.last_name)
    )
    db.commit()


def check_user(user):
    if check_status('api_users', user.id) is not True:
        new_user(user)
    else:
        None


def check_status(table, id):
    sql.execute(f"SELECT id FROM '{table}' WHERE id = '{id}'")
    return True if sql.fetchone() is not None else False


def api_put(table, id, key, text):
    sql.execute(f"UPDATE '{table}' SET '{key}' = '{text}' WHERE id = '{id}'")
    db.commit()


def api_post(table, id, key, text):
    sql.execute(
        f"INSERT INTO '{table}' (id, username_id, '{key}') VALUES (?, ?, ?)",
        (id, id, text))
    db.commit()


def write_data(table, id, key, message):
    if check_status(table, id) is True:
        api_put(table, id, key, message)
    else:
        api_post(table, id, key, message)


def get_data(table, id):
    sql.execute(f"SELECT * FROM '{table}' WHERE id = '{id}'")
    data = sql.fetchall()
    return data
