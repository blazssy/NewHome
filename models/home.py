from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import db

class Homes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bedrooms = db.Column(db.Integer, nullable=False)
    square_footage = db.Column(db.Integer, nullable=False)
    area = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    year_built = db.Column(db.Integer, nullable=False)
    garage_size = db.Column(db.Integer, nullable=False)
    neighbourhood_quality = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Home {self.id}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
