from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for
from models.home import Homes, User
from utils.db import db

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.secret_key = 'your_secret_key'
db.init_app(flask_app)
with flask_app.app_context():
    db.create_all()

# Authentication and role management routes
@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@flask_app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')  # Default to 'user' if no role is specified
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Helper function to check if the user is an admin
def is_admin():
    return session.get('user_role') == 'admin'

# Home route
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
    houses = Homes.query.all()
    return render_template('house.html', houses=houses)

@flask_app.route('/house_chart')
def house_chart():
    houses = Homes.query.all()
    labels = [house.area for house in houses]
    prices = [house.price for house in houses]
    square_footages = [house.square_footage for house in houses]
    return render_template('house_chart.html', labels=labels, prices=prices, square_footages=square_footages)

# CRUD routes with admin access only
@flask_app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_house(id):
    if not is_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('home'))
    house = Homes.query.get_or_404(id)
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
            flash('House details updated successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating. Please try again.', 'error')
    return render_template('update.html', house=house)

@flask_app.route('/manipulate')
def manipulate():
    if not is_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('home'))
    houses = Homes.query.all()
    return render_template('doto.html', house=houses)

@flask_app.route('/delete/<int:id>', methods=['DELETE'])
def delete_house(id):
    if not is_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('home'))
    house = Homes.query.get(id)
    if house:
        db.session.delete(house)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404

@flask_app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    if not is_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('home'))
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
        flash('House details updated successfully!', 'success')
        return redirect(url_for('manipulate'))
    return render_template('update.html', house=house)

@flask_app.route('/submit', methods=['POST'])
def submit():
    if not is_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('home'))
    form_data = request.form.to_dict()
    home = Homes(**form_data)
    db.session.add(home)
    db.session.commit()
    flash('House added successfully!', 'success')
    return redirect(url_for('manipulate'))

# API routes
@flask_app.route('/api/house_data')
def house_data():
    houses = Homes.query.all()
    data = {
        'labels': [house.area for house in houses],
        'bedrooms': [house.bedrooms for house in houses],
        'square_footages': [house.square_footage for house in houses],
        'prices': [house.price for house in houses],
        'bathrooms': [house.bathrooms for house in houses],
        'garage_sizes': [house.garage_size for house in houses],
        'neighbourhood_qualities': [house.neighbourhood_quality for house in houses],
        'year_built': [house.year_built for house in houses]
    }
    return jsonify(data)

@flask_app.route('/api/filter_houses', methods=['GET'])
def filter_houses():
    bedrooms = request.args.get('bedrooms', type=int)
    area = request.args.get('area')
    max_price = request.args.get('max_price', type=int)
    bathrooms = request.args.get('bathrooms', type=int)

    query = Homes.query
    if bedrooms:
        query = query.filter(Homes.bedrooms == bedrooms)
    if area:
        query = query.filter(Homes.area == area)
    if max_price:
        query = query.filter(Homes.price <= max_price)
    if bathrooms:
        query = query.filter(Homes.bathrooms == bathrooms)

    houses = query.all()

    data = [
        {
            'id': house.id,
            'bedrooms': house.bedrooms,
            'square_footage': house.square_footage,
            'area': house.area,
            'price': house.price,
            'bathrooms': house.bathrooms,
            'year_built': house.year_built,
            'garage_size': house.garage_size,
            'neighbourhood_quality': house.neighbourhood_quality
        }
        for house in houses
    ]

    return jsonify(data)

if __name__ == '__main__':
    flask_app.run( host='127.0.0.1', port=5001, debug=True )