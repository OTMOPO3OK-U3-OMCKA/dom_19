from flask import Flask, request
from flask_restx import Resource, Namespace
from conteiner import user_service, auth_service
from dao.model.user import SchemaUser


schema_user = SchemaUser(many=True)
user_ns = Namespace("users")

@user_ns.route("/")
class UserView(Resource):
    def get(self):
        return schema_user.dump(user_service.get_all()), 200

    def post(self):
        r = request.json
        d = user_service.create(r)
        return "", 201

@user_ns.route("/<user_name>")
class UserView(Resource):

    def put(self, user_name):
        r = request.json
        d = user_service.update(r, user_name)
        return '', 201