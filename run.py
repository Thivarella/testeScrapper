import os
from flask import Flask
from app import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port)
