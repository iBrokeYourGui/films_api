from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from src.database.models import Film


class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        # Задаем поля модели которые хотим игнорировать
        exclude = ['id']
        load_instance = True
        # прописываем связь между таблицами
        include_fk = True
    # exclude - для того чтобы избежать рекурсий (зацикливаний)
    actors = Nested('ActorSchema', many=True, exclude=('films', ))
