from database.Models import db, create_tables


def initialization(db_name):
    """
    Функции первичного создания БД, инициализация таблиц.

    :param db_name: название создаваемой БД ("name.db")
    :type: str
    """
    db.init(db_name)
    create_tables()
