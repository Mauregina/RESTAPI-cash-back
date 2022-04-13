from flask_restful import Resource, reqparse
from models.cashback import CashbackModel
from models.sale import SaleModel
from models.product import ProductModel
from models.customer import CustomerModel
from models.cashback import CashbackModel

class Sales(Resource):
    def get(self):
        return {'sales': [sale.json() for sale in SaleModel.query.all()]}

class Sale(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument('sold_at', type=str, required=True, help="The field 'sold_at' must be informed.") 
    attributes.add_argument('customer', type=dict, required=True, help="The field 'customer' must be informed.")
    attributes.add_argument('total', type=float, required=True, help="The field 'total' must be informed.")  
    attributes.add_argument('products', type=dict, action='append', required=True, help="The field 'products' must be informed.")

    def post(self):
        dados = Sale.attributes.parse_args()
        sold_dt = dados.get('sold_at')
        total = dados.get('total')
        customer_dict = dados.get('customer')
        products_lst = dados.get('products')
     
        document = customer_dict.get('document')
        if not CustomerModel.valid_document(document):
            return {'message': "The 'document' must be valid"}, 400 # bad request 

        name = customer_dict.get('name')
        if not CustomerModel.valid_name(name):
            return {'message': "The 'name' must be valid"}, 400 # bad request                 

        if not SaleModel.valid_date(sold_dt):
            return {'message': "The 'sold_at' must be valid"}, 400 # bad request     
        
        for product in products_lst:
            type = product.get('type')
            if not ProductModel.valid_type(type):
                return {'message': "The 'product type' must be 'A', 'B' or 'C'"}, 400 # bad request

            value = product.get('value')
            if not ProductModel.valid_value(value):
                return {'message': "The 'value' must be valid"}, 400 # bad request 

            qty = product.get('qty')
            if not ProductModel.valid_qty(qty):
                return {'message': "The 'qty' must be valid"}, 400 # bad request                     

        if not ProductModel.valid_sum_total_product(total, products_lst):
            return {'message': "The 'total' must be equal to the sum of products"}, 400 # bad request            

        try:
            customer = CustomerModel.find_customer(document)
            if customer:
                customer_id = customer.customer_id
            else:  
                customer_obj = CustomerModel(**customer_dict)
                customer_obj.save_customer()
                customer_id = customer_obj.customer_id

            sale_obj = SaleModel(customer_id, sold_dt, total)
            sale_obj.save_sale()
            sale_id = sale_obj.sale_id

            for product in products_lst:  
                product_obj = ProductModel(sale_id, **product)
                product_obj.save_product()                          

            cashback_obj = CashbackModel(total, sale_id)
            cashback_obj.save_cashback()

            api_response = CashbackModel.send_cashback_maistodos(document, cashback_obj.cashback_value)

            if api_response:
                cashback_obj.cashback_sent = True
                cashback_obj.api_response = str(api_response)
                cashback_obj.save_cashback()
 
        except ValueError:
            return {'message': 'An internal error occurred trying to register cash back. {}'.format(ValueError)}, 500

        return {'message': 'Cashback registered successfully!'}, 201 # created

