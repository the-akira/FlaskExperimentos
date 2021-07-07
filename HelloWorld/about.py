# Importando Flask
from flask import Flask 

# Iniciando a aplicação Flask
app = Flask(__name__) 

# Criando uma rota 
@app.route('/')
def index():
    return 'Hello World'

# Criando uma nova rota about
@app.route('/about')
def about():
    return '<h1>Sobre</h1>'

# export FLASK_APP=about.py
# flask run
if __name__ == '__main__':
    app.run(debug=True)