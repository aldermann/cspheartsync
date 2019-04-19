import const.context_name as context_name
import db.mongo as mongo
import pymongo
from model.API import FBAPI


class MongoUser:
    messenger_id = None
    avatar = None
    full_name = "John Doe"
    gender = "male"
    favourite = "any"
    bot_context = context_name.home
    partner = None
    enqueue_time = None

    _API = None

    def __init__(self, user_messenger_id, do_fetch=True):
        self._API = FBAPI()
        self.messenger_id = user_messenger_id
        if not do_fetch:
            return

        data = mongo.db["user"].find_one({
            "messenger_id": user_messenger_id
        })
        if data is not None:
            for key in data:
                self.__dict__[key] = data[key]

    def _fetch_user_data_from_facebook(self):
        data = self._API.get_user_data(self.messenger_id)
        self.full_name = data["first_name"] + " " + data["last_name"]
        self.avatar = data["profile_pic"]
        self.gender = data["gender"]

    def save(self):
        data = {
            "full_name": self.full_name,
            "gender": self.gender,
            "avatar": self.avatar,
            "partner": self.partner,
            "bot_context": self.bot_context,
            "favourite": self.favourite,
            "enqueue_time": self.enqueue_time
        }
        mongo.db["user"].update_one({
            'messenger_id': self.messenger_id
        }, {
            "$set": data
        })

    def _insert_user(self):
        data = {
            "messenger_id": self.messenger_id,
            "full_name": self.full_name,
            "gender": self.gender,
            "avatar": self.avatar,
            "bot_context": context_name.home
        }
        mongo.db["user"].insert_one(data)

    @staticmethod
    def check_exist(messenger_id):
        return mongo.db["user"].count({
            "messenger_id": messenger_id
        })

    @staticmethod
    def _lookup(gender, favourite):
        query = {
            "$and": [
                {
                    "bot_context": context_name.queuing
                },
                {
                    "$or": [
                        {
                            "favourite": "any"
                        },
                        {
                            "favourite": gender
                        }
                    ]
                }
            ]
        }

        if favourite != "any":
            query["$and"].append({"gender": favourite})
        print (mongo.db["user"].find(query)[0])
        data = mongo.db["user"].find(query).sort("enqueue_time",pymongo.ASCENDING)[0]
        if data is None:
            return data
        return data["messenger_id"]
