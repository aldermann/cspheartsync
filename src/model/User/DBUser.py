import const.context_name as context_name
import db.mysql as db
from model.API import FBAPI


class DBUser:
    messenger_id = None
    avatar = None
    full_name = "John Doe"
    gender = "male"
    favourite = "any"
    bot_context = context_name.home
    partner = None

    _API = None

    def __init__(self, user_messenger_id, do_fetch=True):
        self._API = FBAPI()
        self.messenger_id = user_messenger_id
        if not do_fetch:
            return
        cnx = db.get_connection()
        cursor = cnx.cursor()
        db.execute_query(cursor, cnx, "select * from user where messenger_id = %(messenger_id)s", {
            "messenger_id": user_messenger_id
        })
        data = db.fetch_data(cursor)
        if len(data) > 0:
            for key in data[0]:
                self.__dict__[key] = data[0][key]
        cursor.close()
        cnx.close()

    def _fetch_user_data_from_facebook(self):
        data = self._API.get_user_data(self.messenger_id)
        self.full_name = data["first_name"] + " " + data["last_name"]
        self.avatar = data["profile_pic"]
        self.gender = data["gender"]

    def save(self):
        cnx = db.get_connection()
        cursor = cnx.cursor()
        query = """update user
                          set 
                            full_name = %(full_name)s,
                            gender = %(gender)s,
                            avatar = %(avatar)s,
                            partner = %(partner)s,
                            bot_context = %(bot_context)s,
                            favourite = %(favourite)s
                          where
                            messenger_id = %(messenger_id)s                             
                    """
        data = {
            "full_name": self.full_name,
            "gender": self.gender,
            "avatar": self.avatar,
            "partner": self.partner,
            "bot_context": self.bot_context,
            "favourite": self.favourite,
            "messenger_id": self.messenger_id
        }
        db.execute_query(cursor, cnx, query, data)
        cnx.commit()
        cursor.close()
        cnx.close()

    def _insert_user(self):
        cnx = db.get_connection()
        cursor = cnx.cursor()
        query = """
                    insert into user 
                          (messenger_id, full_name, gender, avatar, favourite, partner, bot_context) 
                    values (%(messenger_id)s, %(full_name)s, %(gender)s, %(avatar)s, 'any', NULL, %(context)s);
                """
        data = {
            "messenger_id": self.messenger_id,
            "full_name": self.full_name,
            "gender": self.gender,
            "avatar": self.avatar,
            "context": context_name.home
        }
        db.execute_query(cursor, cnx, query, data)
        cnx.commit()
        cursor.close()
        cnx.close()

    @staticmethod
    def check_exist(messenger_id):
        cnx = db.get_connection()
        cursor = cnx.cursor()
        db.execute_query(cursor, cnx, "select messenger_id from user where messenger_id = %(messenger_id)s", {
            "messenger_id": messenger_id
        })
        res = len(cursor.fetchall()) > 0
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def _lookup(gender, favourite):
        cnx = db.get_connection()
        cursor = cnx.cursor()
        query = """
        select messenger_id from user 
            where bot_context = %(context)s 
            and (favourite = 'any' or favourite = %(gender)s)
        """
        if favourite != "any":
            query += "and gender = %(favourite)s"
        data = {
            "context": context_name.queuing,
            "gender": gender,
            "favourite": favourite
        }
        db.execute_query(cursor, cnx, query, data)
        data = db.fetch_data(cursor)
        cursor.close()
        cnx.close()
        if len(data) == 0:
            return None
        return data[0]["messenger_id"]
