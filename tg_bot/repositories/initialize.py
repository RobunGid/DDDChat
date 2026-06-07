import sqlite3

from repositories.sql import CREATE_MAPPING_TABLE_SQL_QUERY

from settings.config import get_settings


def create_tables():
    settings = get_settings()

    with sqlite3.connect(database=settings.database_name) as connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_MAPPING_TABLE_SQL_QUERY)
