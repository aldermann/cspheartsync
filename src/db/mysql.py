import os
from mysql.connector import connect

user = os.getenv("DB_USERNAME") or "aldermann"
password = os.getenv("DB_PASSWORD") or "123"
host = os.getenv("DB_URL") or "127.0.0.1"
cnx = connect(user=user, password=password, host=host, database="cspheartsync")

cursor = cnx.cursor()

cursor.execute("""create table if not exists `user` (
                       `messenger_id` bigint(15) not NULL ,
                       `full_name` varchar (64) character set utf8 not NULL default 'John Doe',
                       `gender` enum('male', 'female') not NULL default 'male',
                       `avatar` varchar(256) not NULL,
                       `favourite` enum('male', 'female', 'any') not NULL default 'any',
                       `partner` int(15) ,
                       `bot_context` varchar(64) default 'home',
                       primary key (`messenger_id`)
                   );
                   """)


def fetch_data(cur):
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def create_cursor(**kwargs):
    return cnx.cursor(**kwargs)


def commit_change():
    cnx.commit()
    print("connection committed")
