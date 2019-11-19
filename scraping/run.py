from app import app 

# redis-server
# rq worker
if __name__ == '__main__':
	app.run(debug=True)