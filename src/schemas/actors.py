from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from src.database.models import Actor


class ActorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
        exclude = ['id']
        load_instance = True
        # прописываем связь между таблицами
        include_fk = True

    films = Nested('FilmSchema', many=True, exclude=('actors', ))