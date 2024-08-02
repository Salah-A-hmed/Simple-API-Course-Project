from flask import Flask
from .database import db
from .routes.V1.Authors import authors_bp as authors_v1_bp
from .routes.V1.Books import books_bp as books_v1_bp
from .routes.V1.Borrow_Records import Borrow_Records_bp as Borrow_Records_v1_bp
from .routes.V1.Users import users_bp as users_v1_bp

from .routes.V2.Authors import authors_bp as authors_v2_bp
from .routes.V2.Books import books_bp as books_v2_bp
from .routes.V2.Borrow_Records import Borrow_Records_bp as Borrow_Records_v2_bp
from .routes.V2.Users import users_bp as users_v2_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)

    app.static_folder = '/static'

    CORS(app , resources={r"/*":{"origins":"http://127.0.0.1:8090/"}})

    app.register_blueprint(authors_v1_bp, url_prefix='/api/v1/authors')
    app.register_blueprint(books_v1_bp, url_prefix='/api/v1/books')
    app.register_blueprint(Borrow_Records_v1_bp, url_prefix='/api/v1/borrowrecords')
    app.register_blueprint(users_v1_bp, url_prefix='/api/v1/users')

    app.register_blueprint(authors_v2_bp, url_prefix='/api/v2/authors')
    app.register_blueprint(books_v2_bp, url_prefix='/api/v2/books')
    app.register_blueprint(Borrow_Records_v2_bp, url_prefix='/api/v2/borrowrecords')
    app.register_blueprint(users_v2_bp, url_prefix='/api/v2/users')
    
    return app