from flask_restx import Resource, Namespace
from flask import request
from dao.model.director import DirectorSchema
from implemented import director_service
from conteiner import auth_service



director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200
    @auth_service.auth_required
    def post(self):
        r = request.json
        return director_service.create(r)


@director_ns.route('/<int:rid>')
class DirectorView(Resource):

    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @auth_service.auth_required
    def put(self, rid):
        r = request.json
        return director_service.update(r)

    @auth_service.auth_required
    def delete(self, rid):
        r = request.json
        return director_service.delete(r)
