import flask

app = flask.Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'HEAD', 'POST', 'PUT'])
def catch_all(path):
    values = {'path': path,
              'method': flask.request.method,
              'values': flask.request.args,
              'headers': dict(flask.request.headers)}
    return flask.json.jsonify(values)

if __name__ == '__main__':
    app.run()