from pymongo import MongoClient

class MongoDBPool():
    def __init__(self, dbconfig):
        self._host = dbconfig['host']
        self._port = dbconfig['port']
        self._user = dbconfig['user']        
        self._password = dbconfig['password']
        self._database = dbconfig['database']
        self.mongo_uri = "mongodb+srv://"+self._user+":"+self._password+"@"+self._host+"/"+self._database

    def create_client(self):
        self.client = MongoClient(self.mongo_uri)
        print('MOngo client created') 

    def get_client(self):
        return self.client 

    def get_db_connection(self):
        return self.client[self._database]    