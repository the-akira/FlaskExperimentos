from app import app
from flask import render_template

# Criando uma rota 
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

# Criando uma nova rota about
@app.route('/admin/profile')
def admin_profile():
    return render_template('admin/profile.html')