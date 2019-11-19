from flask import Flask, request 
from task import *

# Comando para rodar o worker: rq worker

app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

@app.route('/task')
def add_task():
	if request.args.get('n'):
		job = q.enqueue(background_task, request.args.get('n'))

		q_len = len(q)

		return f'Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in the queue'

	return 'No value for n'

if __name__ == '__main__':
	app.run(debug=True)