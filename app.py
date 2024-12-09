from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


# Subscription Plan Enum
from enum import Enum
app = Flask(__name__)

app.config['SECRET_KEY'] = 'oursecretkey'
bcrypt = Bcrypt(app)

# Configure database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    return app


# Initialize the LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to 'login' view if unauthorized
login_manager.login_message = "Please log in to access this page."


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose another.', 'danger')
            return redirect(url_for('register'))

        # Hash the password and create a new user
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Replace `User` with your user model


class SubscriptionPlan(Enum):
    BASIC = "Basic"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"


# User model with subscription plan
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # Ensure this column is defined
    subscription = db.Column(db.String(50), default='Basic')


# IoT Data model


class ScientificData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    measurement = db.Column(db.Float, nullable=False)
    # Indicates if the data is processed
    processed = db.Column(db.Boolean, default=False)


@app.route('/api/register_device', methods=['POST'])
def register_device():
    data = request.get_json()
    device_id = data.get('device_id')
    secret_key = data.get('secret_key')

    if not device_id or not secret_key:
        return jsonify({'message': 'Missing device_id or secret_key'}), 400

    if Device.query.filter_by(device_id=device_id).first():
        return jsonify({'message': 'Device already exists'}), 400

    new_device = Device(device_id=device_id, secret_key=secret_key)
    db.session.add(new_device)
    db.session.commit()
    return jsonify({'message': 'Device registered successfully'}), 201


@app.route('/api/data', methods=['POST'])
def collect_data():
    data = request.get_json()
    device_id = data.get('device_id')
    measurement = data.get('measurement')

    if not device_id or not measurement:
        return jsonify({'message': 'Invalid payload'}), 400

    new_data = ScientificData(
        device_id=device_id, timestamp=datetime.utcnow(), measurement=measurement)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Data collected successfully'}), 201


@app.route('/api/data/<plan>', methods=['GET'])
@login_required
def get_data(plan):
    if plan == "basic":
        if current_user.subscription != SubscriptionPlan.BASIC:
            return jsonify({'message': 'Access denied for Basic Plan'}), 403
        data = ScientificData.query.all()  # Raw data only
    elif plan == "pro":
        if current_user.subscription != SubscriptionPlan.PRO:
            return jsonify({'message': 'Access denied for Pro Plan'}), 403
        data = ScientificData.query.filter_by(
            processed=True).all()  # Processed data
    elif plan == "enterprise":
        if current_user.subscription != SubscriptionPlan.ENTERPRISE:
            return jsonify({'message': 'Access denied for Enterprise Plan'}), 403
        data = ScientificData.query.all()  # All data

    return jsonify([
        {'device_id': d.device_id, 'timestamp': d.timestamp.isoformat(),
         'measurement': d.measurement}
        for d in data
    ])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/subscriptions")
def subscriptions():
    return render_template("subscriptions.html")


@app.route('/subscribe/<plan>', methods=['GET', 'POST'])
@login_required
def subscribe(plan):
    # Validate the plan
    valid_plans = ['basic', 'pro', 'enterprise']
    if plan not in valid_plans:
        flash('Invalid subscription plan selected.', 'danger')
        return redirect(url_for('subscriptions'))

    # Update the user's subscription plan
    # Store the plan (Basic, Pro, Enterprise)
    current_user.subscription = plan.capitalize()
    db.session.commit()

    flash(
        f'Successfully subscribed to the {plan.capitalize()} plan!', 'success')
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)
