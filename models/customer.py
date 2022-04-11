from sql_alchemy import banco
import re

class CustomerModel(banco.Model):
    __tablename__ = 'customers'

    customer_id = banco.Column(banco.Integer, primary_key=True)
    document = banco.Column(banco.String(11))
    name = banco.Column(banco.String(100))

    def __init__(self, document, name):
        self.document = document
        self.name = name
        
    def json(self):
        return {
            'customer_id': self.customer_id,
            'document': self.document,
            'name': self.name
        }

    @classmethod
    def valid_document(cls, document: str)->bool:
        if len(document) != 11 or len(set(document)) == 1:
            return False  

        numbers = [int(digit) for digit in document]

        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    @classmethod
    def find_customer(cls, document):
        customer = cls.query.filter_by(document=document).first()

        if customer:
            return customer
        return None    

    def save_customer(self):
        banco.session.add(self)
        banco.session.flush()
        #banco.session.commit()
