from inspect import Attribute

from pkg_resources import require
from flask_restful import Resource, reqparse
from models.sale import SaleModel
from models.product import ProductModel
from models.customer import CustomerModel

class Sales(Resource):
    def get(self):
        return {'sales': [sale.json() for sale in SaleModel.query.all()]}

class Sale(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument('sold_at', type=str, required=True, help="The field 'sold_at' might be informed.") 
    attributes.add_argument('customer', type=dict, required=True, help="The field 'customer' might be informed.")
    attributes.add_argument('total', type=str, required=True, help="The field 'total' might be informed.")  
    attributes.add_argument('products', type=dict, action='append', required=True, help="The field 'products' might be informed.")

    def post(self):
        dados = Sale.attributes.parse_args()
        sold_at = dados.get('sold_at')
        total = dados.get('total')
        customer_dict = dados.get('customer')
        products_lst = dados.get('products')

        try:     
            document = customer_dict.get('document')
            customer = CustomerModel.find_customer(document)
            if customer:
                customer_id = customer.customer_id
            else:
                if not CustomerModel.valid_document(document):
                    return {'message': "The 'document' must be valid"}, 400 # bad request    
                customer_obj = CustomerModel(**customer_dict)
                customer_obj.save_customer()
                customer_id = customer_obj.customer_id

            if not SaleModel.valid_date(sold_at):
                return {'message': "The 'sold_at' must be valid"}, 400 # bad request     

            sale_obj = SaleModel(customer_id, sold_at, total)
            sale_obj.save_sale()
            
            for product in products_lst:
               product_obj = ProductModel(sale_obj.sale_id, **product)
               product_obj.save_product()
        except ValueError:
            return {'message': 'An internal error occurred trying to save sale. {}'.format(ValueError)}, 500

        return {'message': 'Cashback registered successfully!'}, 201 # created


    