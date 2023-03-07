from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)
movies_namespace = api.namespace('movies')
directors_namespace = api.namespace('directors')
genres_namespace = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

movie_schema = MovieSchema()
director_schema = DirectorSchema()
genre_schema = GenreSchema()

movies_schema = MovieSchema(many=True)
directors_schema = DirectorSchema(many=True)
genres_schema = GenreSchema(many=True)

@app.route('/')
@movies_namespace.route('/')
class MoviesViews(Resource):
    def get(self):
        movies = Movie.query
        if request.args.get('genre_id'):
            movies = movies.filter(Movie.genre_id == request.args.get('genre_id'))
        elif request.args.get('director_id'):
            movies = movies.filter(Movie.genre_id == request.args.get('director_id'))
        return movies_schema.dump(movies.all()), 200

@movies_namespace.route('/<int: pk>')
class MoviesViews(Resource):
    def get(self, pk):
        movie = Movie.query.get(pk)
        return movie_schema.dump(movie), 200


if __name__ == '__main__':
    app.run(debug=True)
