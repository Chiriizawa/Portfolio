from flask import Flask, session
from datetime import timedelta
from sample_project.blueprint_folder.route import blueprint



def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'ray'
    
    app.permanent_session_lifetime = timedelta(hours=24)

# Make the session permanent by default
    @app.before_request
    def make_session_permanent():
        session.permanent = True
    
    app.register_blueprint(blueprint, url_prefix='/')


    return app