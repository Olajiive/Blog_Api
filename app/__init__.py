from flask import Flask
from flask_restx import Api
from app.auth.views import auth_namespace
from app.resources.views import post_namespace
from .utils import db
from flask_migrate import Migrate
from .config.config import config_dict
from .models.post import Post
from .models.user import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed




def create_app(config=config_dict["dev"]):
    app=Flask(__name__)

    app.config.from_object(config)
    db.init_app(app)

    jwt=JWTManager(app)
    migrate = Migrate(app, db)

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWTgt;** token to authorize"
        }
    }
    api= Api(app,
             title ="A Blog API",
             description="A simple blog REST API service", 
             authorizations=authorizations,
             security="Bearer Auth")

    api.add_namespace(post_namespace)
    api.add_namespace(auth_namespace, path='/auth')
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def not_found(error):
        return {"error": "Not Allowed"}, 404
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "user":User,
            "order":Post
        }
    return app
