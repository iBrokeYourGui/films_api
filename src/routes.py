"""
    Здесь только то что служит для регистрации новых маршрутов
"""

from src import api
from src.resources.agregations import AggregationApi
from src.resources.films import FilmListApi
from src.resources.actors import ActorListApi
from src.resources.smoke import Smoke
from src.resources.auth import AuthRegister, AuthLogin

api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/films/<uuid>', strict_slashes=False)
api.add_resource(AggregationApi, '/agregations', strict_slashes=False)
api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
