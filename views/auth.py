
from flask_restx import abort, Namespace, Resource
from flask import request, jsonify
from conteiner import auth_service

auth_ns = Namespace('auth')


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        data = request.json

        username = data.get("username")
        password = data.get("password")

        if None is [username, password]:
            return '', 400

        tokens = auth_service.generate_tokens(username, password)
        return jsonify(tokens)



    def put(self):
        data = request.json
        token = data.get("refresh_token")
        tokens = auth_service.approve_refresh_token(token)
        return tokens, 200



