from flask import Flask

app = None

def init_app():
	global app
	app = Flask(__name__.split('.')[0])
	return app
