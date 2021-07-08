from flask import Flask, render_template, session, redirect, url_for 
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField, RadioField, SelectField, TextField, TextAreaField, SubmitField)
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    name = StringField('Quem é você?', validators=[DataRequired()])
    saúde = BooleanField('Você está bem de saúde?')
    humor = RadioField('Por favor, escolha o seu humor:', choices=[('Feliz','Feliz'),('Alegre','Alegre')])
    comida = SelectField('Escolha seu alimento favorito:',choices=[('Arroz','Arroz'),('Batata','Batata'),('Banana','Banana')])
    feedback = TextAreaField()
    submit = SubmitField('enviar')

@app.route('/', methods=['GET','POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['name'] = form.name.data 
        session['saúde'] = form.saúde.data 
        session['humor'] = form.humor.data 
        session['comida'] = form.comida.data 
        session['feedback'] = form.feedback.data 

        return redirect(url_for('obrigado'))

    return render_template('index.html', form=form)

@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html')

if __name__ == '__main__':
    app.run(debug=True)