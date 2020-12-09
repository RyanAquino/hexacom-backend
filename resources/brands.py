from flask_restful import Resource, reqparse
from models.brands import BrandModel
from flask_jwt import jwt_required
from sqlalchemy import exc


class Brand(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, name):
        brand = BrandModel.find_by_name(name)

        if brand:
            return brand.json()

        return {"message": "Brand not found."}, 404

    @jwt_required()
    def post(self, name):
        if BrandModel.find_by_name(name):
            return {
                "message": "A Brand with name '{}' already exists.".format(name)
            }, 400

        brand = BrandModel(name)

        try:
            brand.save_to_db()
        except Exception:
            return {"message": "An error occured while adding the brand."}, 500

        return brand.json(), 201

    @jwt_required()
    def delete(self, name):
        brand = BrandModel.find_by_name(name)

        if brand:
            try:
                brand.delete_from_db()
            except exc.IntegrityError:
                return {
                    "message": "Brand can't be deleted. It is associated with an item in a job order. "
                }

        return {"message": "Brand deleted."}


class BrandList(Resource):
    @jwt_required()
    def get(self):
        return {"brands": [brand.json() for brand in BrandModel.query.all()]}
