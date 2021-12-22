import os

APP_ENV = 'development'
API_PREFIX = '/api'
DEBUG = True
TESTING = True

MONGO_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'user':'dbadmin2',
    'password':'demo1234',
    'database': 'usersdata'    
}
BASE_DIR = os.path.join( os.getcwd())