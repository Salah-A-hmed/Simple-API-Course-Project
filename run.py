from app import create_app
from flask_swagger_ui import get_swaggerui_blueprint
import os
app = create_app()

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'SIMPLE API COURSE PROJECT'
    }
)
app.register_blueprint(swaggerui_blueprint, url_pregfix = SWAGGER_URL)

if __name__ == '__main__':
    app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'static')
    app.run(debug=True)
