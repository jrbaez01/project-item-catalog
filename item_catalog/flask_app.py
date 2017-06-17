from flask import Flask

app = None

def init_app():
	global app
	app = Flask(__name__.split('.')[0])
	app.secret_key = 'super_secret_key_TODO'
	return app
