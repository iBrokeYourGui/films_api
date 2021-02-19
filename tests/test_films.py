import json
from dataclasses import dataclass
from http import HTTPStatus
from unittest.mock import patch

from src import app, db

@dataclass
class FakeFilm:
    title = 'Fake Film'
    distributed_by = 'Fake'
    release_date = '2002-12-03'
    description = 'Fake description'
    length = 100
    rating = 8.0


class TestFilms:
    uuid =[]

    def test_get_films_from_db(self):
        client = app.test_client(db.session)
        resp = client.get('/films')

        assert resp.status_code == HTTPStatus.OK

    @patch('src.services.film_service.FilmService.fetch_all_films')
    def test_get_films_mock_db(self, mock_db_call):
        client = app.test_client(db.session)
        resp = client.get('/films')

        mock_db_call.assert_called_once()
        assert resp.status_code == HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_film_with_db(self):
        client = app.test_client(db.session)
        data = {
            "title": "Fake Film",
            "distributed_by": "Fake",
            "release_date": "2002-12-03",
            "description": "Fake description",
            "length": 100,
            "rating": 8.0
        }
        resp = client.post('/films', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == HTTPStatus.CREATED
        assert resp.json['title'] == "Fake Film"
        self.uuid.append(resp.json['uuid'])

    def test_create_film_with_mock_db(self):
        """
            В данном слкучае у нас 2 метода обращаются к базе, поэтому нужно создать
            2 контектста патчей для эмуляции процесса
            в результате записей в базе не создатся
        """
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                'title': 'Test Title',
                'distributed_by': 'Test Company',
                'release_date': '2010-04-01',
                'description': '',
                'length': 100,
                'rating': 8.0
            }
            resp = client.post('/films', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        data = {
            'title': 'Update Title',
            'distributed_by': 'update',
            'release_date': '2010-04-01'
        }
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == HTTPStatus.OK
        assert resp.json['title'] == 'Update Title'

    def test_update_film_with_mock_db(self):
        with patch('src.services.film_service.FilmService.fetch_film_by_uuid') as mocked_query, \
                patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            # эмулируем ответ от сервера в виде датакласса FakeFilm
            mocked_query.return_value = FakeFilm()
            client = app.test_client()
            url = f'/films/1'
            data = {
                'title': 'Update Title',
                'distributed_by': 'update',
                'release_date': '2010-04-01'
            }
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == HTTPStatus.NO_CONTENT