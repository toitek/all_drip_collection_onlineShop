from drip import db, login_manager
from flask_login import UserMixin
from drip import bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    ip_address = db.Column(db.String(20), nullable=False)
    sales = db.relationship('Sale', backref='user', lazy=True)

    def get_id(self):
           return (self.user_id)


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

""" class Seller(db.Model):
    seller_id = db.Column(db.Integer, primary_key=True)
    username = db.column(db.Integer(), db.ForeignKey('user_id'))
    product = db.relationship('Product', backref='product_seller', lazy=True) """

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    old_price = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    sales = db.relationship('Sale', backref='product', lazy=True)

    def __repr__(self):
        return f'Product {self.name}'

"""class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Cart {self.cart_id}'"""
    
class Sale(db.Model):
    sales_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_sold = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Sales {self.sales_id}'
    



