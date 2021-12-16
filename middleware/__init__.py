from configs import settings
from middleware.mongo_pool import MongoDBPool



dbconfig_mongo = {
    'host':settings.MONGO_CONFIG['host'],
    'port': 27017,
    'user': settings.MONGO_CONFIG['user'],
    'password':settings.MONGO_CONFIG['password'],
    'database':settings.MONGO_CONFIG['database']  
}

global ypmongo_pool

ypmongo_pool = MongoDBPool(dbconfig_mongo)
ypmongo_pool.create_client()



