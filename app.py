from flask import Flask
from modules.empresa.controller import app_empresa



app = Flask(__name__)
app.register_blueprint(app_empresa)

if __name__ == '__main__':
    app.run(debug=True)
