from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload

from src.services.film_service import FilmService
from src import db
from src.database.models import Film
from src.resources.auth import token_required
from src.schemas.films import FilmSchema


class FilmListApi(Resource):
    film_schema = FilmSchema()

    # @token_required
    def get(self, uuid=None):
        if not uuid:
            # .options - для разрашения n+1 проблемы
            # joinedload - будет делать 1 запрос к базе
            # selectinload - будет делать 2 запрос к базе
            # без опций - для каждой записи подзапрос будет отрабатывать как одельный запрос

            # films = db.session.query(Film).options(joinedload(Film.actors)).all()
            films = FilmService.fetch_all_films(db.session).options(joinedload(Film.actors)).all()

            return self.film_schema.dump(films, many=True), 200
            # return [f.to_dict() for f in films], 200
        # film = db.session.query(Film).filter_by(uuid=uuid).first()
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return '', 404
        return self.film_schema.dump(film), 200
        # return film.to_dict(), 200

    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 201

        # film_json = request.json
        # if not film_json:
        #     return {'message': 'Wrong data'}, 400
        # try:
        #     film = Film(
        #         title = film_json['title'],
        #         release_date = datetime.datetime.strptime(film_json['release_date'], '%B %d %Y'),
        #         description = film_json.get('description'),
        #         distributed_by = film_json.get('distributed_by'),
        #         length = film_json.get('length'),
        #         rating = film_json.get('rating')
        #     )
        #     db.session.add(film)
        #     db.session.commit()
        # except (ValueError, KeyError):
        #     return {'message': 'Wrong data'}, 400
        # return {'message': 'Crete successfully'}, 201

    def put(self, uuid):
        # film = db.session.query(Film).filter_by(uuid=uuid).first()
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return {'message': ''}, 404
        try:
            film = self.film_schema.load(request.json, instance=film, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(film)
        db.session.commit()
        return self.film_schema.dump(film), 200

        # film_json = request.json
        # if not film_json:
        #     return {'message': 'Wrong data'}, 400
        # try:
        #     db.session.query(Film).filter_by(uuid=uuid).update(
        #         dict(
        #             title=film_json['title'],
        #             release_date=datetime.datetime.strptime(film_json['release_date'], '%B %d %Y'),
        #             description=film_json.get('description'),
        #             distributed_by=film_json.get('distributed_by'),
        #             length=film_json.get('length'),
        #             rating=film_json.get('rating')
        #         )
        #     )
        #     db.session.commit()
        # except (ValueError, KeyError):
        #     return {'message': 'Wrong data'}, 400
        # return {'message': 'Update successfully'}, 200

    def patch(self, uuid):
        """Частичное изменение ресурса"""
        # todo добавить валидацию данных
        pass
        # film = db.session.query(Film).filter_by(uuid=uuid).first()
        # if not film:
        #     return '', 404
        # film_json = request.json
        # title = film_json.get('title')
        # # Если на вход пришля пустая дата то возвращаем None
        # release_date = datetime.datetime.strptime(film_json('release_date'), '%B %d %Y') \
        #     if film_json.get('release_date') else None
        # description = film_json.get('description')
        # distributed_by = film_json.get('distributed_by')
        # length = film_json.get('length')
        # rating = film_json.get('rating')
        #
        # # проверыем каждый поступивший параметр и заменфем его
        # if title:
        #     film.title = title
        # elif release_date:
        #     film.release_date = release_date
        # elif description:
        #     film.description = description
        # elif distributed_by:
        #     film.distributed_by = distributed_by
        # elif length:
        #     film.length = length
        # elif rating:
        #     film.rating = rating
        #
        # db.session.add(film)
        # db.session.commit()
        # return {'message': 'Update successfully'}, 200

    def delete(self, uuid):
        """Удаление ресурса"""
        # film = db.session.query(Film).filter_by(uuid=uuid).first()
        film = FilmService.fetch_film_by_uuid(db.session, uuid)
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return '', 204
