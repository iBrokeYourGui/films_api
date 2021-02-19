import datetime
from functools import wraps

import jwt
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from src import db, app
from src.database.models import User
from src.schemas.users import UserSchema


class AuthRegister(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {"message": str(e)}
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"message": "Such user exists"}, 409
        return self.user_schema.dump(user), 201


class AuthLogin(Resource):
    def get(self):
        auth = request.authorization
        if not auth:
            return "Authentication required", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        # user = db.session.query(User).filter_by(user_name=(auth.get('username', ''))).first()
        user = User.find_user_by_username(auth.get('username', ''))
        if not user or not check_password_hash(user.password, auth.get('password', '')):
            return "no user or bad passowrd", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            }, 'SECRET_KEY'
        )
        return jsonify(
            {
                # "token": token.decode('utf-8')
                "token": token
            }
        )


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-API-KEY', '')
        if not token:
            return "have no tokein in your request", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return "no user_id in your token", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        # user = db.session.query(User).filter_by(uuid=uuid).first()
        user = User.find_user_by_uuid(uuid)
        if not user:
            return "bad user_id", 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}
        return func(self, *args, **kwargs)

    return wrapper

