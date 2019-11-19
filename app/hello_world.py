from flask import Flask # Importando Flask

app = Flask(__name__) # Iniciando a aplicação Flask

# Criando uma rota
@app.route('/')
def index():
	return 'Hello World'

if __name__ == '__main__':
	app.run(debug=True)