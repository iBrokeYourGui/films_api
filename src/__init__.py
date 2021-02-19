from flask_swagger_ui import get_swaggerui_blueprint

import config
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy, get_debug_queries

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

# Настройки свагера
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Flask tutorial'
    }
)
# привязываем ургу свагера к нашему приложению
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

app.debug = True


def sql_debug(response):
    """
        Считаем время выполнения запросов
        для отловки проблемы n+1 запросов
    """
    queries = list(get_debug_queries())
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration

    print('=' * 80)
    print(f' SQL Queryes {len(queries)} in {round(total_duration * 1000, 2)}ms')
    print('=' * 80)

    return response


app.after_request(sql_debug)

# @app.route("/", methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')
#
#
# @app.route("/greetings", methods=['POST'])
# def greetings():
#     name = request.form.get('name')
#     # проверка на заполнения параметра name на форме. Защита от 500 ошибки при передвчи пустых дагнных через curn
#     if not name:
#         return 'Please enter value\n', 400
#     return render_template('greetings.html', name=name)


from . import routes
from .database import models
