import os

import algorithmz
from flask import Flask, render_template, json, request, redirect, url_for, jsonify
from werkzeug.wsgi import LimitedStream
import uuid


app = Flask(__name__)

class StreamConsumingMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        stream = LimitedStream(environ['wsgi.input'],
                               int(environ['CONTENT_LENGTH'] or 0))
        environ['wsgi.input'] = stream
        app_iter = self.app(environ, start_response)
        try:
            stream.exhaust()
            for event in app_iter:
                yield event
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)

@app.route("/")
@app.route("/index")
def main():
    return render_template('index.html')

@app.route("/timeTabling")
def timeTabling():
    return render_template('timeTabling.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})

@app.route("/timeTabling/result", methods=['POST'])
def findSchedule():

    # Initialize the errors variable to empty string. We will have the error messages
    # in that variable, if any.
    errors = ''
    check = request.form.get('file')
    try:
            used = "ha"
            if request.form.get('file') is None:
                _filePath = ''
                return render_template('timeTabling.html')
            else:
                _filePath = '/home/febiagil/Workspaces/workspace_python/tubes_ai/uploads/' + request.form.get('file')
                algorithmz.bacaTestcase(_filePath)
                if (request.form.get('algooptions') == "simulatedannealing"):
                    algorithmz.execSA()
                    used = "Simulated Annealing"
                if (request.form.get('algooptions') == "hillclimbing"):
                    algorithmz.execHC()
                    used = "Hill Climbing"
                if (request.form.get('algooptions') == "geneticalgorithm"):
                    algorithmz.execSA()
                    used = "Genetic Algorithm"


                result_in_json = algorithmz.convert_to_json()
                effectiveness = algorithmz.calculateEffectiveness()
                conflict = algorithmz.countConflicts()
                listKonflik = algorithmz.listKonflik

                return render_template('result.html', data=result_in_json, effectiveness=effectiveness, conflict=conflict, listKonflik = listKonflik, used=used )
    except Exception as e:
        return render_template('404.html',error = str(e), check=check)



if __name__ == "__main__":
    app.run(debug=True)
