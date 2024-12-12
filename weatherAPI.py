
# Installation
# install flask
# pip install flask
 #pip install pymysql
# install Flask-SQLAlchemy
# pip install flask_sqlalchemy
 
# install Flask-Marshmallow
# pip install flask_marshmallow

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()

# Initializing the Flask app, SQLAlchemy, and Marshmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/weather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Data model to store weather details
class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))  # ISO 8601 - YYYYMMDD
    time = db.Column(db.String(8))  # ISO 8601 - hh:mm:ss
    timezone_offset = db.Column(db.String(6))  # ISO 8601 e.g. UTC-10:00
    coordinates = db.Column(db.String(50))  # Decimal degrees
    temperature_water = db.Column(db.Float)  # C°
    temperature_air = db.Column(db.Float)  # C°
    humidity = db.Column(db.Float)  # g/kg
    wind_speed = db.Column(db.Float)  # km/h
    wind_direction = db.Column(db.Float)  # Decimal degrees
    precipitation = db.Column(db.Float)  # mm
    haze = db.Column(db.Float)  # %
    notes = db.Column(db.Text)  # Additional notes

    def __init__(
        self, date, time, timezone_offset, coordinates,
        temperature_water, temperature_air, humidity, wind_speed,
        wind_direction, precipitation, haze, notes
    ):
        self.date = date
        self.time = time
        self.timezone_offset = timezone_offset
        self.coordinates = coordinates
        self.temperature_water = temperature_water
        self.temperature_air = temperature_air
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.precipitation = precipitation
        self.haze = haze
        self.notes = notes

# Marshmallow schema for serialization
class WeatherRecordSchema(ma.Schema):
    class Meta:
        fields = (
            "id", "date", "time", "timezone_offset", "coordinates",
            "temperature_water", "temperature_air", "humidity", "wind_speed",
            "wind_direction", "precipitation", "haze", "notes"
        )

weather_record_schema = WeatherRecordSchema()
weather_records_schema = WeatherRecordSchema(many=True)

# Route to add a new weather record
@app.route('/weather', methods=['POST'])
def add_weather_record():
    data = request.json

    new_record = WeatherRecord(
        date=data['date'],
        time=data['time'],
        timezone_offset=data['timezone_offset'],
        coordinates=data['coordinates'],
        temperature_water=data['temperature_water'],
        temperature_air=data['temperature_air'],
        humidity=data['humidity'],
        wind_speed=data['wind_speed'],
        wind_direction=data['wind_direction'],
        precipitation=data['precipitation'],
        haze=data['haze'],
        notes=data['notes']
    )

    db.session.add(new_record)
    db.session.commit()

    return weather_record_schema.jsonify(new_record)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Weather API. Use /weather to interact."})

# Route to get all weather records
@app.route('/weather', methods=['GET'])
def get_weather_records():
    all_records = WeatherRecord.query.all()
    result = weather_records_schema.dump(all_records)
    return jsonify(result)

# Route to get a single weather record by ID
@app.route('/weather/<id>', methods=['GET'])
def get_weather_record(id):
    record = WeatherRecord.query.get(id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return weather_record_schema.jsonify(record)

#Route to get paramatised qurys 
# Route to get filtered weather records based on query parameters
@app.route('/weather/filter', methods=['GET'])
def get_filtered_weather_records():
    # Extract query parameters
    start_date = request.args.get('start_date')  # Optional
    end_date = request.args.get('end_date')      # Optional
    min_temp_air = request.args.get('min_temp_air', type=float)  # Optional
    max_temp_air = request.args.get('max_temp_air', type=float)  # Optional
    coordinates = request.args.get('coordinates')  # Optional

    # Start building the query
    query = WeatherRecord.query

    # Apply filters conditionally
    if start_date:
        query = query.filter(WeatherRecord.date >= start_date)
    if end_date:
        query = query.filter(WeatherRecord.date <= end_date)
    if min_temp_air is not None:
        query = query.filter(WeatherRecord.temperature_air >= min_temp_air)
    if max_temp_air is not None:
        query = query.filter(WeatherRecord.temperature_air <= max_temp_air)
    if coordinates:
        query = query.filter(WeatherRecord.coordinates == coordinates)

    # Execute the query and serialize results
    filtered_records = query.all()
    result = weather_records_schema.dump(filtered_records)
    return jsonify(result)


# Route to delete a weather record by ID
@app.route('/weather/<id>', methods=['DELETE'])
def delete_weather_record(id):
    record = WeatherRecord.query.get(id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return weather_record_schema.jsonify(record)

if __name__ == "__main__":
    app.run(debug=True)

'''
from alche import app, db

# Use the app context
with app.app_context():
    db.create_all()
'''