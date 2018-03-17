from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'


app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['SECRET_KEY'] = "kb161dfd61dgdg6ddfdd"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://capelcwvgbouzn:83904471a49b9745c1f67dae685630e6318ea452423a610d0e737b86ef448be6@ec2-54-163-246-193.compute-1.amazonaws.com:5432/d5cae0ljph75ar"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.config['UPLOAD_FOLDER'] = "./app/static/uploads"

allowed_extensions = app.config['ALLOWED_EXTENSIONS']



db = SQLAlchemy(app)
app.config.from_object(__name__)
from app import views

