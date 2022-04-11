from inspect import Attribute
from flask_restful import Resource, reqparse
from models.sale import SaleModel

class Sales(Resource):
    def get(self):
        return {'sales': [sale.json() for sale in SaleModel.query.all()]}

class Sale(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument('total', type=str, required=True, help="The field 'total' might be informed.")  
    attributes.add_argument('type', type=str, required=True, help="The field 'type' might be informed.") 
    attributes.add_argument('value', type=str, required=True, help="The field 'value' might be informed.") 
    attributes.add_argument('qty', type=int, required=True, help="The field 'qty' might be informed.")  

    def post(self):
        dados = Sale.attributes.parse_args()
        sale_obj = SaleModel(**dados)

        try:
            sale_obj.save_sale()
            return sale_obj.json(), 201
        except:
            return {'message': 'An internal error occurred trying to save hotel.'}, 500

    