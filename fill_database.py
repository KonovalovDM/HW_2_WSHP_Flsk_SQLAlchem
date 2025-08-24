from app import app, db
from models import Book, Genre
from datetime import datetime, timedelta

with app.app_context():
    # Очищаем существующие данные
    db.session.query(Book).delete()
    db.session.query(Genre).delete()
    db.session.commit()

    # Создаем жанры
    genres = [
        Genre(name='Фантастика'),
        Genre(name='Детектив'),
        Genre(name='Роман'),
        Genre(name='Фэнтези'),
        Genre(name='Научная литература'),
        Genre(name='Биография'),
        Genre(name='Исторический'),
        Genre(name='Триллер'),
        Genre(name='Ужасы'),
        Genre(name='Приключения')
    ]

    for genre in genres:
        db.session.add(genre)
    db.session.commit()

    # Список книг с разными жанрами и статусами
    books_data = [
        {'title': 'Мастер и Маргарита', 'genre': 'Роман', 'is_read': True},
        {'title': 'Преступление и наказание', 'genre': 'Роман', 'is_read': False},
        {'title': '1984', 'genre': 'Фантастика', 'is_read': True},
        {'title': 'Убийство в Восточном экспрессе', 'genre': 'Детектив', 'is_read': False},
        {'title': 'Властелин колец', 'genre': 'Фэнтези', 'is_read': True},
        {'title': 'Гарри Поттер и философский камень', 'genre': 'Фэнтези', 'is_read': True},
        {'title': 'Краткая история времени', 'genre': 'Научная литература', 'is_read': False},
        {'title': 'Шерлок Холмс', 'genre': 'Детектив', 'is_read': True},
        {'title': 'Война и мир', 'genre': 'Исторический', 'is_read': False},
        {'title': 'Тихий Дон', 'genre': 'Роман', 'is_read': False},
        {'title': 'Дюна', 'genre': 'Фантастика', 'is_read': True},
        {'title': 'Игра престолов', 'genre': 'Фэнтези', 'is_read': False},
        {'title': 'Молчание ягнят', 'genre': 'Триллер', 'is_read': True},
        {'title': 'Оно', 'genre': 'Ужасы', 'is_read': False},
        {'title': 'Три мушкетера', 'genre': 'Приключения', 'is_read': True},
        {'title': 'Автостопом по галактике', 'genre': 'Фантастика', 'is_read': True},
        {'title': 'Десять негритят', 'genre': 'Детектив', 'is_read': False}
    ]

    # Добавляем книги с разными датами создания
    for i, book_info in enumerate(books_data):
        genre = Genre.query.filter_by(name=book_info['genre']).first()
        if genre:
            book = Book(
                title=book_info['title'],
                genre_id=genre.id,
                is_read=book_info['is_read'],
                created_at=datetime.utcnow() - timedelta(hours=i * 2)  # Разные даты
            )
            db.session.add(book)

    db.session.commit()
    print("База данных успешно заполнена! Добавлено 17 книг.")