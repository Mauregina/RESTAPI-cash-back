from flask_restful import Resource, reqparse
from models.customer import CustomerModel

class Customers(Resource):
    def get(self):
        return {'customers': [customer.json() for customer in CustomerModel.query.all()]}

class Customer(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument('name', type=str, required=True, help="The filed 'name' might be informed.")

    def get(self, document):
        customer = CustomerModel.find_customer(document)

        if customer:
            return customer.json()
        return {'message': 'Customer not found'}, 404       

    def post(self, document):
        if not CustomerModel.find_customer(document):        
            dados = Customer.attributes.parse_args()
            customer_obj = CustomerModel(document, **dados)

            try:
                customer_obj.save_customer()
                return {'message': 'Customer created successfully'}, 201
            except:
                return {'message': 'An internal error occurred trying to save site.'}, 500

        return {"message": "Customer '{}' already exists.".format(document)}, 400 # bad request        
