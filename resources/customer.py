from flask_restful import Resource, reqparse
from models.customer import CustomerModel

class Customers(Resource):
    def get(self):
        return {'customers': [customer.json() for customer in CustomerModel.query.all()]}
        