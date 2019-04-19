import os

from mysql.connector import OperationalError
from mysql.connector.pooling import MySQLConnectionPool, MySQLConnection

conf = {
    "user": os.getenv("DB_USERNAME") or "aldermann",
    "password": os.getenv("DB_PASSWORD") or "123",
    "host": os.getenv("DB_URL") or "127.0.0.1",
    "database": os.getenv("DB_NAME") or "cspheartsync"
}

pool = MySQLConnectionPool(4, "heartsync", **conf)


def init():
    cnx = pool.get_connection()
    cursor = cnx.cursor()

    cursor.execute("""create table if not exists `user` (
                           `messenger_id` bigint(15) not NULL ,
                           `full_name` varchar (64) character set utf8 not NULL default 'John Doe',
                           `gender` enum('male', 'female') not NULL default 'male',
                           `avatar` varchar(256) not NULL,
                           `favourite` enum('male', 'female', 'any') not NULL default 'any',
                           `partner` bigint(15) ,
                           `enqueue_time` bigint(15) ,
                           `bot_context` varchar(64) default 'home',
                           primary key (`messenger_id`)
                       );
                       """)

    # cursor.execute("""create table if not exists `log` (
    #                        'log_id' int(8) not NULL auto_increment,
    #                        'message' varchar(512) not NULL,
    #                        primary key (`log_id`)
    #                    );
    #                    """)


def fetch_data(cur):
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def get_connection():
    """
    :return: a connection
    :rtype: MySQLConnection
    """
    return pool.get_connection()


def execute_query(cursor, cnx, query, data):
    try:
        # print("executing query", query)
        cursor.execute(query, data)
    except OperationalError:
        print("restarting connection")
        cnx.reconnect()
        cursor.execute(query, data)


init()
