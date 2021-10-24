from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
import time
from datetime import datetime
from pymongo.errors import OperationFailure


class DataBase():
    def __init__(self, host, port, db_name):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]

    def insert_one(self, collection, data):
        try:
            self.db[collection].insert_one(data)
            return {"status": "success"}
        except OperationFailure:
            return {"status": "error"}

    def insert_many(self, collection, data):
        try:
            self.db[collection].insert_many(data)
            return {"status": "success"}
        except OperationFailure:
            return {"status": "error"}

    def get_by_id(self, collection, obj_id):
        model = self.db[collection].find_one({"_id": ObjectId(obj_id)})
        if not model:
            return None
        return model

    def get_by_film_id(self, collection, film_id):
        model = self.db[collection].find_one({"film_id": film_id})
        if not model:
            return None
        return model

    def get_all(self, collection):
        model = self.db[collection].find({})
        if not model:
            return []
        return list(model)

    def get_all_ids(self, collection):
        model = self.db[collection].find({}, {"film_id": 1, "_id": 0})
        if not model:
            return []
        res = list(map(lambda film: film["film_id"], list(model)))
        return res

    def filter_timestamp_gte(self, collection, timestamp):
        model = self.db[collection].find({"timestamp": {"$gte": timestamp}})
        if not model:
            return []
        return list(model)
