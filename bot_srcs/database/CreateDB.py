from database.Models import db, create_tables


def initialization(db_name):
    db.init(db_name)
    create_tables()
