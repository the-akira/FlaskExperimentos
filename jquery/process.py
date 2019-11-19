from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/process', methods=['POST'])
def process():
	email = request.form['email']
	name = request.form['name']

	if name and email:
		new_name = name[::-1]

		return jsonify({'name': new_name})

	return jsonify({'error': 'Missing data!'})

if __name__ == '__main__':
	app.run(debug=True)