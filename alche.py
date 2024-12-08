from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://root:''@localhost/post'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(150))
    author = db.Column(db.String(50))

    def __init__(self,title, description, author):
        self.title = title
        self.description = description
        self.author = author



@app.route('/get', methods = ['GET'])
def get_post():
    return jsonify({"Hello":"World"})

if __name__ == "__main__":
    app.run(debug=True)