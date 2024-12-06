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
