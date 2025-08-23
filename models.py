from extensions import db
from datetime import datetime

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='genre', lazy=True)

    def __repr__(self):
        return f'<Genre {self.name}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'