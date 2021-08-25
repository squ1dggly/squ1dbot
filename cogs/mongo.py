from pymongo import MongoClient

mongo_url = 'mongodb://squ1d:<password>@squ1dbot-shard-00-00.kk3hm.mongodb.net:27017,squ1dbot-shard-00-01.kk3hm.mongodb.net:27017,squ1dbot-shard-00-02.kk3hm.mongodb.net:27017/test?replicaSet=atlas-felmbb-shard-0&ssl=true&authSource=admin'

class Mongo():
    def __init__(self):
        self.cluster = MongoClient(mongo_url)
        self.bot_cluster = self.cluster["bot"]
        self.server_configs_collection = self.bot_cluster["server_configs"]

    def append_to_server_configs(self, data):
        self.server_configs_collection.insert_one(data)

    def update_server_configs(self, query, new_data):
        self.server_configs_collection.update_one(query, new_data)

    def count_documents_in_server_configs(self, query):
        return self.server_configs_collection.count_documents(query)

    def get_guild_user(self, guild_id):
        return self.server_configs_collection.find({"_id": guild_id})