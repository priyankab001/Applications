import csv
import json
from io import StringIO
from flask import Flask, render_template, request, make_response

app = Flask(__name__)
app.debug = True

def csv2json(data):
	reader = csv.DictReader
	reader = csv.DictReader(data)
	out = json.dumps([ row for row in reader ])
	print("JSON parsed!") 
	return out
	print("JSON saved!")


@app.route('/csv2json', methods=["POST"])
def convert():
	f = request.files['data_file']
	if not f:
		return "No file"
	file_contents = StringIO(f.stream.read())
	result = csv2json(file_contents)
	response = make_response(result)
	response.headers["Content-Disposition"] = "attachment; filename=Converted.json"
	return response


@app.route('/')
def main():
	render_template
	return render_template('convert.html')

if __name__ == '__main__':
	app.run(debug=True)