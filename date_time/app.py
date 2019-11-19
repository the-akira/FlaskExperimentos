from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms.fields import DateField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
Bootstrap(app)

class MyForm(Form):
    date = DateField(id='datepick')

@app.route('/')
def index():
    form = MyForm()
    return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)