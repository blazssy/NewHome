from flask import Flask, render_template, request, redirect, jsonify
from models.home import Homes
from utils.db import db
from flask import flash, redirect, url_for


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

@flask_app.route('/house')
def house():
    houses = Homes.query.all()  # Get all house entries
    if not houses:
        print("No houses found.")  # Debugging: Print statement to check if there are no houses
    else:
        for house in houses:
            print(house)  # Debugging: Print each house object

    return render_template('house.html', houses=houses)


@flask_app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_house(id):
    houses = Homes.query.get_or_404(id)

    if request.method == 'POST':
        try:
            house.bedrooms = int(request.form.get('bedrooms', house.bedrooms))
            house.square_footage = int(request.form.get('square_footage', house.square_footage))
            house.area = request.form.get('area', house.area).strip()
            house.price = int(request.form.get('price', house.price))
            house.bathrooms = int(request.form.get('bathrooms', house.bathrooms))
            house.year_built = int(request.form.get('year_built', house.year_built))
            house.garage_size = int(request.form.get('garage_size', house.garage_size))
            house.neighbourhood_quality = request.form.get('neighbourhood_quality', house.neighbourhood_quality).strip()

            db.session.commit()
            flash("House details updated successfully!", "success")
            return redirect(url_for('home'))  # Change 'index' to 'home' if your root route is named 'home'.
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating. Please try again.", "error")

    return render_template('update.html', house=houses)

@flask_app.route('/manipulate')
def manipulate():
    houses = Homes.query.all()  # Get all house entries
    return render_template('doto.html', house=houses)


@flask_app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    house = Homes.query.get(id)
    if house:
        db.session.delete(house)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404

@flask_app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    house = Homes.query.get_or_404(id)
    if request.method == 'POST':
        house.bedrooms = request.form['bedrooms']
        house.square_footage = request.form['square_footage']
        house.area = request.form['area']
        house.price = request.form['price']
        house.bathrooms = request.form['bathrooms']
        house.garage_size = request.form['garage_size']
        house.neighbourhood_quality = request.form['neighbourhood_quality']
        house.year_built = request.form['year_built']

        db.session.commit()
        return redirect(url_for('manipulate'))
    return render_template('update.html', house=house)

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
