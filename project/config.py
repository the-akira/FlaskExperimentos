class Config(object):
	DEBUG = False 
	TESTING = False
	SECRET_KEY = 'a90fb31x2la1092!5@#!'
	DB_NAME = 'production-db'
	DB_USERNAME = 'root'
	DB_PASSWORD = 'example'

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	DEBUG = True 

	DB_NAME = 'development-db'
	DB_USERNAME = 'root'
	DB_PASSWORD = 'example'

class TestingConfig(Config):
	TESTING = True 

	DB_NAME = 'development-db'
	DB_USERNAME = 'root'
	DB_PASSWORD = 'example'