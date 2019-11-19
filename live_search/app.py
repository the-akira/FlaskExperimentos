from flask import Flask, request, render_template
import json

app = Flask(__name__)

LANGUAGES = [
	'Python',
	'PHP',
	'C',
	'C++',
	'Javascript',
	'LISP',
	'FORTRAN',
	'C#',
	'Java',
	'Haskell',
	'Assembly',
	'Elixir',
	'Go',
	'COBOL',
	'Ruby',
	'Clojure',
	'Erlang',
	'Julia',
	'Objective-C',
	'Pascal',
	'Bash',
	'OCaml'
]

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
	text = request.args['search_text']
	result = [c for c in LANGUAGES if str(text).lower() in c.lower()]
	return json.dumps({"results":result}) 

if __name__ == "__main__":
    app.run(debug=True)