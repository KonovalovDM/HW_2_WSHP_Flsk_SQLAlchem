from flask import Flask, render_template, request, redirect, url_for, jsonify
from extensions import db
from flask_migrate import Migrate
from models import Book, Genre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    books = Book.query.order_by(Book.created_at.desc()).limit(15).all()
    return render_template('index.html', books=books)

@app.route('/genre/<int:genre_id>')
def genre_view(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books = Book.query.filter_by(genre_id=genre_id).all()
    return render_template('genre.html', genre=genre, books=books)

@app.route('/update_is_read/<int:book_id>', methods=['POST'])
def update_is_read(book_id):
    book = Book.query.get_or_404(book_id)
    is_read = request.json.get('is_read')
    if is_read is not None:
        book.is_read = is_read
        db.session.commit()
        return jsonify({'success': True, 'is_read': book.is_read})
    return jsonify({'success': False}), 400


if __name__ == '__main__':
    app.run(debug=True)