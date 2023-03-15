import logging
import sqlite3
from sqlite3 import Error

from database.helper_db import open_connection

logger = logging.getLogger(__name__)


def create_chat_db(
        db_file_path: str,
    ):
    """create a SQLite database and relevant tables for storing chat data

    Args:
        db_file_path (str): path to the database file
    """
    conn = open_connection(db_file_path=db_file_path)
    create_chat_table(connection=conn)
    conn.close()


def create_chat_table(
        connection: sqlite3.Connection,
    ):
    """create a table to store GPT chat data

    Args:
        conn (sqlite3.Connection): connection to the database
    """
    sql_create_chat_table = """ CREATE TABLE IF NOT EXISTS chat (
                                        id integer PRIMARY KEY,
                                        author text NOT NULL,
                                        role text NOT NULL,
                                        message text NOT NULL,
                                        timestamp datetime NOT NULL
                                    ); """

    try:
        c = connection.cursor()
        c.execute(sql_create_chat_table)
        logger.info("Chat table created successfully (if not already existing)")
    except Error as e:
        logger.error(f"Chat table not created successfully: {e}")


def add_message_to_chat_db(
        username: str,
        message: str,
        role: str,
        connection: sqlite3.Connection,
    ):
    """add a user message to the chat database

    Args:
        message (str): user message
        username (str): username of the user this conversation is with
        role (str): role who created the message text, either "user" or "assistant" for the model
        connection (sqlite3.Connection): connection to the chat database
    """
    sql_query = "INSERT INTO chat(author,message,role,timestamp) VALUES(?,?,?,datetime('now'))"

    try:
        cur = connection.cursor()
        cur.execute(sql_query, (username, message, role))
        connection.commit()
        logger.info(f"Message for {username}:{role} added to chat db.")
    except Error as e:
        logger.error(f"Message for {username}:{role} not added to chat db: {e}.")


def get_chat_history(
        username: str,
        connection: sqlite3.Connection,
        timeframe: float = 2
    ) -> list:
    """get the chat history of a user

    Args:
        username (str): username of the user this conversation is with
        connection (sqlite3.Connection): connection to the chat database
        timeframe (str): timeframe to get the chat history for in hours. Defaults to 2 hours.

    Returns:
        list: list of tuples containing the chat history
    """
    logger.info(f"Retrieving message hist for {username} from chat db.")
    sql_query = (
        f"""SELECT role, message
            FROM chat
            WHERE author = '{username}' AND timestamp > datetime('now', '-{timeframe} hours')
            ORDER BY timestamp ASC;
        """
    )

    try:
        c = connection.cursor()
        c.execute(sql_query)
        chat_history = [row for row in c]
        logger.info(f"Chat history for {username} retrieved: {len(chat_history)} relevant messages found.")
    except (Error, Exception) as e:
        logger.error(f"Chat history for {username} not retrieved: {e}")
        chat_history = []

    return chat_history
