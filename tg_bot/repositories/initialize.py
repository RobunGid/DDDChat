import sqlite3

from repositories.queries import CREATE_MAPPING_TABLE_SQL_QUERY

from settings.config import get_config


def create_tables():
    config = get_config()

    with sqlite3.connect(database=config.database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_MAPPING_TABLE_SQL_QUERY)
