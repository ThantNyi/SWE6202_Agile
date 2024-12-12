# import flask class
from flask import Flask, request
import json

from datetime import datetime, timezone

# Sqlalchemy for ORM
from flask_sqlalchemy import SQLAlchemy

# Marshmallow for object serialization/deserialization
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Sqlalchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# install database
db = SQLAlchemy(app)

# initialise Marshmallow
ma = Marshmallow(app)

# class def for Sqlalchemy ORM
class Details(db.Model):
    location_id = db.column(db.string(20), primary_key=True)
    watertemp_C = db.column(db.float(5), nullable=False)
    airtemp_C = db.column(db.float(5), nullable=False)
    humidity_kg = db.column(db.string(5), nullable=False)
    windspeed_km = db.column(db.string(5), nullable=False)
    winddirection = db.column(db.float(5), nullable=False)
    precipitation_mm = db.column(db.string(5), nullable=False)
    haze = db.column(db.string(5), nullable=False)
    becquerel_Bq = db.column(db.string(5), nullable=False)

    def __repe__(self):
        return '<Details %r>' %self.location_id

#----class def for marsh serialization-----

class DetailsSchema(ma.SQLAlchemyAutoSchema):
    """Definition used for serialization based on the details model"""
    class Meta:
        fields = ("location_id", "watertemp_C", "airtemp_C", "humidity_kg", "windspeed_km", "winddirection", "precipitation_mm", "haze", "becquerel_Bq")

#-----instantiation of objects---------

details_schema = DetailsSchema()
details_schema = DetailsSchema(many=True)

#----------------------------------------------
@app.get('/')
def hello_world():
    return 'Hello World'