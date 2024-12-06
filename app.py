from flask import Flask, render_template, request, redirect
from models.home import Homes
from utils.db import db

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(flask_app)
with flask_app.app_context():
    db.create_all()

@flask_app.route('/')
def home():
    return render_template('index.html')

@flask_app.route('/about')
def about():
    return render_template('about.html')

@flask_app.route('/contact')
def contact():
    return render_template('contact.html')

@flask_app.route('/filter')
def filter():
    return render_template('filter.html')

@flask_app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()
    print(f"form_data: {form_data}")

    bedrooms = form_data.get('bedrooms')
    square_footage = form_data.get('square_footage')
    area = form_data.get('area')
    price = form_data.get('price')
    bathrooms = form_data.get('bathrooms')
    year_built = form_data.get('year_built')
    garage_size = form_data.get('garage_size')
    neighbourhood_quality = form_data.get('neighbourhood_quality')

    home = Homes(
        bedrooms=bedrooms,
        square_footage=square_footage,
        area=area,
        price=price,
        bathrooms=bathrooms,
        year_built=year_built,
        garage_size=garage_size,
        neighbourhood_quality=neighbourhood_quality
    )
    db.session.add(home)
    db.session.commit()
    print("submitted successfully")
    return redirect('/')

if __name__ == '__main__':
    flask_app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    )
