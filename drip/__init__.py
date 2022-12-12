from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
# Set up the password reset token serializer.
# This is used to generate and verify the password reset link.
app.config['SECRET_KEY']= '88d981b544da6ddbfbb1b967'
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["10 per minute", "50 per hour"]
)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ano:1964#British@localhost/drip'
app.config['SECRET_KEY']= '88d981b544da6ddbfbb1b967'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'georgewandhe@gmail.com'
app.config['MAIL_PASSWORD'] = '1964#British'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

login_manager.login_view="login_page"
login_manager.login_message_category="info"


from drip import routes







