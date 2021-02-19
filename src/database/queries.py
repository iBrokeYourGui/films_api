"""
SELECT QUERIES
"""
from sqlalchemy import and_

from src import db
from src.database import models

films = db.session.query(models.Film).order_by(models.Film.rating.desc()).all()
harry_potter_and_ch_s = db.session.query(models.Film).filter(
    models.Film.title == 'Harry Potter and Chamber of Secrets'
).first()
harry_potter_priz_az = db.session.query(models.Film).filter_by(
    title='Harry Potter and the Prizoner of Azkaban'
).first()
# можно в место and_ навешивать последовательно фильтры
and_statement_harry_potter = db.session.query(models.Film).filter(
    and_(
        models.Film.title != 'Harry Potter and Chamber of Secrets',
        models.Film.rating >= 7.5
    )
).all()
# Еще есть ilike но он чувствительный к регистру
deathy_hallows = db.session.query(models.Film).filter(
    models.Film.title.ilike('%deathly hallows%')
).all()
# тильда (~) означает not для in
# слайсами в конце строки мы можем задавать limit выводимых значений
harry_potter_sorted_by_length = db.session.query(models.Film).filter(
    ~models.Film.length.in_([146, 161]))[:3]
"""
QUERYING WITH JOINS
"""
films_with_actors = db.session.query(models.Film).join(models.Film.actors).all()
print(films_with_actors)