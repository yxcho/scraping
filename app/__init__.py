from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy_session import flask_scoped_session

# Define the WSGI application object
app = Flask(__name__, instance_relative_config=False)

# Configurations
app.config.from_object('system_config.Config')

# bind restful api with flask
api = Api(app)

# from .request import requests
# app.register_blueprint(requests)


url  = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(url)
session_factory = sessionmaker(bind=engine)
Session = flask_scoped_session(session_factory, app)



# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
db.init_app(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app import routes

app.template_folder = './templates'
app.app_context().push()

# Import a module / component using its blueprint handler variable (mod_auth)
# from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
# app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()