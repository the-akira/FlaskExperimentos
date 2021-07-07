# Importando Flask
from flask import Flask 

# Iniciando a aplicação Flask
app = Flask(__name__) 

# Criando uma rota
@app.route('/')
def index():
    return 'Hello World'

# Rodando o app
if __name__ == '__main__':
    app.run(debug=True)