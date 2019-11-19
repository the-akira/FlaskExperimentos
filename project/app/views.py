from app import app
from flask import render_template, request, redirect, jsonify, make_response, send_from_directory, abort, flash
from datetime import datetime
from werkzeug.utils import secure_filename
import os

# Criação de Filtro
@app.template_filter('clean_date')
def clean_date(dt):
	return dt.strftime('%d %b %Y')

# Criando uma rota 
@app.route('/')
def index():
	return render_template('public/index.html')

@app.route('/jinja')
def jinja():
	nome = 'Gabriel'

	idade = 28

	langs = ['Python', 'Javascript', 'C', 'C++', 'Bash']

	personagens = {
		'DBZ': 'Goku',
		'Naruto': 'Kakashi',
		'Death Note': 'Raito Yagami',
		'Akira': 'Tetsuo'
	}

	cores = ('red', 'green', 'blue')

	legal = True

	class GitRemote:
		def __init__(self, name, description, url):
			self.name = name
			self.description = description
			self.url = url 

		def pull(self):
			return f'Pulling repo {self.name}'

		def clone(self):
			return f'Cloning into {self.url}'

	remote = GitRemote(name='Flask Jinja', description='Template Design Tutorial', url='https://github.com/julian-nash/jinja.git')

	def repeat(x, qty):
		return x * qty

	date = datetime.utcnow()

	html = "<h1>Titulo Grande</h1>"

	malicioso = "<script>alert('Voce foi hackeado!')</script>"

	return render_template(
		'public/jinja.html', 
		nome=nome,
		idade=idade,
		langs=langs,
		personagens=personagens,
		cores=cores,
		legal=legal,
		GitRemote=GitRemote,
		repeat=repeat,
		remote=remote,
		date=date,
		html=html,
		malicioso=malicioso
	)

# Criando uma nova rota about
@app.route('/about')
def about():
	return render_template('public/about.html')

@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
	if request.method == 'POST':
		req = request.form

		username = req['username']
		email = req.get('email')
		password = request.form['password']

		print(username,email,password)
		
		return redirect(request.url)

	return render_template('public/sign_up.html')

users = {
	'gabriel': {
		'name': 'Gabriel Felippe',
		'bio': 'Interessado em Computação',
		'twitter': '@akirascientist'
	},
	'akira': {
		'name': 'akira',
		'bio': 'the unknown',
		'twitter': '@akira'
	}
}

@app.route('/profile/<username>')
def profile(username):

	user = None

	if username in users:
		user = users[username]

	return render_template('public/profile.html', username=username, user=user)

@app.route('/multiple/<foo>/<bar>/<baz>')
def multi(foo, bar, baz):
	return f'foo is {foo}, bar is {bar}, baz is {baz}'

@app.route('/json', methods=['POST'])     
def json():
	if request.is_json:

		req = request.get_json()
		response = {
			"message": "JSON received",
			"name": req.get("name")
		}
		res = make_response(jsonify(response), 200)

		return res
	else:

		res = make_response(jsonify({"message": "No JSON received"}), 400)

		return 'No JSON received', 400

@app.route('/guestbook')
def guestbook():
	return render_template('public/guestbook.html')

@app.route('/guestbook/create-entry', methods=['POST'])
def create_entry():
	req = request.get_json()

	print(req)

	res = make_response(jsonify(req), 200)

	return res

@app.route('/query')
def query():
	args = request.args 

	for k, v in args.items():
		print(f'{k}:{v}')

	return 'Query received', 200

app.config['IMAGE_UPLOADS'] = '/home/talantyr/Documentos/Projetos/Python Experimentos/Web Development/Flask/project/app/static/img/uploads'
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ['PNG','JPG','JPEG','GIF']
app.config['MAX_IMAGE_FILESIZE'] = 0.5 * 1024 * 1024

def allowed_image(filename):
	if not '.' in filename:
		return False
	ext = filename.rsplit('.',1)[1]
	if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
		return True 
	else:
		return False

def allowed_image_file_size(filesize):
	if int(filesize) <=  app.config['MAX_IMAGE_FILESIZE']:
		return True 
	else:
		return False

@app.route('/upload-image', methods=['GET','POST'])
def upload_image():
	if request.method == 'POST':
		if request.files:
			if not allowed_image_file_size(request.cookies.get('filesize')):
				print('File exceeded maximum size limit')
				return redirect(request.url)
			image = request.files['image']
			if image.filename == "":
				print('Image must have a filename')
				return redirect(request.url)
			if not allowed_image(image.filename):
				print('That image extensions is not allowed')
				return redirect(request.url)
			else:
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
			print("image saved")
			return redirect(request.url)
	return render_template('public/upload_image.html')

"""
string:
int:
float:
path:
uuid:
"""
app.config['CLIENT_IMAGES'] = '/home/talantyr/Documentos/Projetos/Python Experimentos/Web Development/Flask/project/app/static/client/img'
app.config['CLIENT_CSV'] = '/home/talantyr/Documentos/Projetos/Python Experimentos/Web Development/Flask/project/app/static/client/csv'
app.config['CLIENT_REPORTS'] = '/home/talantyr/Documentos/Projetos/Python Experimentos/Web Development/Flask/project/app/static/client/reports'
@app.route('/get-image/<image_name>')
def get_image(image_name):
	try:
		return send_from_directory(app.config['CLIENT_IMAGES'], filename=image_name, as_attachment=False)
	except FileNotFoundError:
		abort(404)

@app.route('/get-csv/<filename>')
def get_csv(filename):
	try:
		return send_from_directory(app.config['CLIENT_CSV'], filename=filename, as_attachment=True)
	except FileNotFoundError:
		abort(404)

@app.route('/get-report/<path:path>')
def get_report(path):
	try:
		return send_from_directory(app.config['CLIENT_REPORTS'], filename=path, as_attachment=True)
	except FileNotFoundError:
		abort(404)

@app.route('/cookies')
def cookies():
	res = make_response('Cookies', 200)
	cookies = request.cookies 
	sabor = cookies.get('sabor')
	print(sabor)
	res.set_cookie('sabor', value='pizza', max_age=10, expires=None, path=request.path, domain=None, secure=False, httponly=False, samesite=False)
	return res

@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		req = request.form 
		username = req.get('username')
		email = req.get('email')
		password = req.get('password')

		if not len(password) >= 10:
			flash('Password must bet at least 10 characters in length','warning')
			return redirect(request.url)

		flash('Account created','success')

		return redirect(request.url)
	return render_template('public/signup.html')

