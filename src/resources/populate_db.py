"""
    Механизм наполнения базы с разных сайтов
    с использованием потоков

    Получиь топ фильмов
    Пройтись по каддому фильму из рейтинга и вытащьть по нему информацию
    Залить в базу
"""
import requests
import bs4
import datetime
from flask_restful import Resource

from src import db
from src.services.film_service import FilmService


def convert_time(time: str) -> float:
    hour, minute = time.split('h')
    minutes = (60 * int(hour)) + int(minute.strip('min'))
    return minutes


class PopulateDB(Resource):
    url = 'https://www.imdb.com/'

    def post(self):
        t0 = datetime.datetime.now()
        films_urls = self.get_films_urls()
        films = self.parse_films(films_urls)
        created_films = self.populate_db_with_films(films)
        dt = datetime.datetime.now() - t0
        print(f'Done in {dt.total_seconds():.2f} sec.')
        return {'message': f'Database were populated with {created_films} films'}, 201

    def get_films_urls(self):
        print('Getting film urls', flush=True)
        url = self.url + 'chart/top/'
        resp = requests.get(url)
        resp.raise_for_status()

        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        movie_containers = soup.find_all('td', class_='posterColumn')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:10]
        return movie_links

    def parse_films(self, film_urls):
        films_to_create = []
        for url in film_urls:
            url = self.url + url
            print(f'Getting a detailed info about the film - {url}')
            film_content = requests.get(url)
            film_content.raise_for_status()

            html = film_content.text
            soup = bs4.BeautifulSoup(html, features="html.parser")
            title, _ = soup.find('div', class_='originalTitle').text.split('(')
            rating = float(soup.find('div', class_='ratingValue').strong.text)
            description = soup.find('div', class_='summary_text').text.strip()
            title_bar = soup.find('div', class_='titleBar').text.strip()
            title_content = title_bar.split('\n')
            release_date, _ = title_content[-1].split('(')
            try:
                release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
            except ValueError:
                try:
                    release_date = datetime.datetime.strptime(release_date.strip(), '%B %Y')
                except ValueError:
                    release_date = datetime.datetime.strptime(release_date.strip(), '%Y')
            length = convert_time(soup.find('div', class_='subtext').time.text.strip())
            print(f'Received information about - {title}', flush=True)
            films_to_create.append(
                {
                    'title': title,
                    'rating': rating,
                    'description': description,
                    'release_date': release_date,
                    'length': length,
                    'distributed_by': 'Warner Bros. Pictures',
                }
            )
        return films_to_create

    @staticmethod
    def populate_db_with_films(films):
        return FilmService.bulk_create_films(db.session, films)
