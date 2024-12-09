from flask import Flask
from sample_project.blueprint_folder.route import blueprint



def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'ray'
    
    app.register_blueprint(blueprint, url_prefix='/')


    return app