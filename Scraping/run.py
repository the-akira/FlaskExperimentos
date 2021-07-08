from app import app 

# Instalar redis-server
# Executar rq worker
# Navegar até http://localhost:5000/add-task
if __name__ == '__main__':
    app.run(debug=True)