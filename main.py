#app/-init_.py

from flask import Flask

def create_app():
    app = Flask(__name__)
    from .routes import main
    app.register_blueprint(main)
    return app

#---- app/routes.py-----
from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

#----main.py----
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

#---requirements.txt---
Flask==2.3.3
gunicorn==21.2.0


