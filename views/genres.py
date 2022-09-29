from flask_restx import Resource, Namespace
from flask import request
from dao.model.genre import GenreSchema
from implemented import genre_service
from conteiner import auth_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):

    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200
    @auth_service.auth_required
    def post(self):
        r = request.json
        return genre_service.create(r)


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @auth_service.auth_required
    def put(self, rid):
        r = request.json
        return genre_service.update(r)

    @auth_service.auth_required
    def delete(self, rid):
        r = request.json
        return genre_service.delete(r)
