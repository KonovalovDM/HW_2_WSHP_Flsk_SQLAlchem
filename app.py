from flask import Flask, render_template, request, jsonify
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
    try:
        books = Book.query.order_by(Book.created_at.desc()).limit(15).all()
        return render_template('index.html', books=books)
    except Exception as e:
        return str(e), 500

@app.route('/genre/<int:genre_id>')
def genre_view(genre_id):
    try:
        genre = Genre.query.get_or_404(genre_id)
        books = Book.query.filter_by(genre_id=genre_id).all()
        return render_template('genre.html', genre=genre, books=books)
    except Exception as e:
        return str(e), 500


@app.route('/update_is_read/<int:book_id>', methods=['POST'])
def update_is_read(book_id):
    try:
        print(f"Updating book {book_id}")  # лог для отладки

        book = Book.query.get_or_404(book_id)
        data = request.get_json()

        print(f"Received data: {data}")  # лог для отладки

        if not data:
            return jsonify({'success': False, 'error': 'No JSON data'}), 400

        is_read = data.get('is_read')
        if is_read is None:
            return jsonify({'success': False, 'error': 'is_read parameter required'}), 400

        print(f"Setting is_read to: {is_read}")  # лог для отладки

        book.is_read = bool(is_read)
        db.session.commit()

        print(f"Successfully updated book {book_id} to is_read={book.is_read}")
        return jsonify({'success': True, 'is_read': book.is_read})

    except Exception as e:
        db.session.rollback()
        print(f"Error updating book {book_id}: {str(e)}")  # лог для отладки
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/debug/books')
def debug_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'title': book.title,
            'is_read': book.is_read,
            'genre': book.genre.name,
            'created_at': book.created_at.isoformat()
        })
    return jsonify(result)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)