import logging
import sqlite3
from sqlite3 import Error


def open_connection(
        db_file_path: str,
        logger: logging.Logger
    ) -> sqlite3.Connection:
    """open a database connection to a SQLite database

    Args:
        db_file_path (str): path to the database file
        logger (logging.Logger): logger instance

    Returns:
        sqlite3.Connection: connection to the database
    """
    try:
        conn = sqlite3.connect(db_file_path)
        logger.debug(f"Connection to SQLite DB successful: {db_file_path}")
    except Error as e:
        logger.error(f"Connection to SQLite DB not successful: {db_file_path} - {e}")
        raise e

    return conn
