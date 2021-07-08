from flask import Flask, render_template, flash, session, redirect, url_for 
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'kmykey'

class SimpleForm(FlaskForm):
    name = StringField('Qual o seu nome?')
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET','POST'])
def index():
    form = SimpleForm()

    if form.validate_on_submit():
        session['name'] = form.name.data 
        flash(f'Você alterou o seu nome para: {session["name"]}')

        return redirect(url_for('index'))

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)