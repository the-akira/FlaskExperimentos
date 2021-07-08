from flask import Flask, render_template 
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    name = StringField('Qual o seu nome?')
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET','POST'])
def index():
    name = False 
    form = InfoForm()

    if form.validate_on_submit():
        name = form.name.data 
        form.name.data = ''
    return render_template('index.html',form=form, name=name)

if __name__ == '__main__':
    app.run(debug=True)