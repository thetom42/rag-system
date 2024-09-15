import os
from flask import Flask
from rag_system.app.routes import init_routes
from rag_system.config import UPLOAD_FOLDER

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')

    init_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
