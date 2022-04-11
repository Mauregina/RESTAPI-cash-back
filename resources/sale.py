from inspect import Attribute
from flask_restful import Resource, reqparse
from models.sale import SaleModel
from models.product import ProductModel

class Sales(Resource):
    def get(self):
        return {'sales': [sale.json() for sale in SaleModel.query.all()]}

class Sale(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument('sold_at', type=str, required=True, help="The field 'sold_at' might be informed.") 
    attributes.add_argument('total', type=str, required=True, help="The field 'total' might be informed.")  
    attributes.add_argument('products', type=dict, action='append')

    def post(self):
        dados = Sale.attributes.parse_args()
        sold_at = dados.get('sold_at')
        total = dados.get('total')
        products_lst = dados.get('products')

        try:       
            sale_obj = SaleModel(sold_at, total)
            sale_obj.save_sale()
            print(sale_obj.sale_id)
            
            for product in products_lst:
                product_obj = ProductModel(sale_obj.sale_id, **product)
                product_obj.save_product()
        except:
            return {'message': 'An internal error occurred trying to save sale.'}, 500

        return {'message': 'Cashback registered successfully!'}, 201 # created


    