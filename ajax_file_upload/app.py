from flask import Flask, render_template, request, jsonify, make_response 

# Iniciando a aplicação Flask
app = Flask(__name__) 

# Rotas
@app.route('/')
def index():
	return 'Hello World'

@app.route('/upload-video', methods=['GET', 'POST'])
def upload_video():
	if request.method == 'POST':
		filesize = request.cookies.get('filesize')
		file = request.files['file']
		print(f'Filesize: {filesize}')
		print(file)
		res = make_response(jsonify({'message': f"{file.filename} uploaded"}), 200)
		return res 
	return render_template('upload_video.html')

if __name__ == '__main__':
	app.run(debug=True)