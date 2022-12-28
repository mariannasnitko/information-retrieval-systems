import os
import re

from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    term = ''
    if request.method == "POST":
        term = request.form['projectFilepath']
    if term == '':
        return 'Введіть слово для пошуку'

    p = subprocess.Popen('python3 searchengine.py --search_bbc {term}'.format(term=term),
                         stdout=subprocess.PIPE, shell=True)
    out = str(p.communicate())
    left_str = out[3:len(out)]
    right = left_str[0: len(left_str) - 10]
    result = right.replace('\\', '')

    return 'Results for query "{term}": '.format(term=term) + result


if __name__ == '__main__':
    app.run(debug=True)
