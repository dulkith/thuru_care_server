import flask

app = flask.Flask(__name__, static_url_path ="/static")

app.run(host="0.0.0.0", port=5000)
