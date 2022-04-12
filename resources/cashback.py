from flask_restful import Resource, reqparse
from models.cashback import CashbackModel

class Cashback(Resource):
    def get(self):
        return {'cashback': [cashback.json() for cashback in CashbackModel.query.all()]}
        