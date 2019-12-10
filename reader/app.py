import flask
import flask_bootstrap
import glob
import json
import random
import os
import re

app = flask.Flask(__name__)
bootstrap = flask_bootstrap.Bootstrap(app)

@app.route('/')
def index():
    novelList = []
    for path in glob.glob('database/*.txt'):
        with open(path, 'rb') as f:
            novelList.append(get_meta(f))
    random.shuffle(novelList)
    return flask.render_template('index.html', novels=novelList)

@app.route('/view/<string:ncode>')
def view(ncode):
    if re.fullmatch("N\d{4}[A-Z]{2}", ncode):
        path = 'database/{}.txt'.format(ncode)
        if not os.path.exists(path):
            flask.abort(404, 'Not found dayo')
        else:
            with open(path, 'rb') as f:
                meta = get_meta(f)
                text = f.read().decode().replace('\n', '<br>')
    else:
        flask.abort(404, 'Not found dayo')

    if '{{' in text:
        error = '<p style="color:red;">テンプレートタグが使われているためこの文章は表示できません</p>'
        flask.render_template('view.html', title=meta['title'], text=error)
    else:
        return flask.render_template('view.html', title=meta['title'], text=text)

def get_meta(f):
    json_meta = b''
    while True:
        c = f.read(1)
        if c == b'\n': break
        json_meta += c
    meta = json.loads(json_meta)
    return meta

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=21080
    )
