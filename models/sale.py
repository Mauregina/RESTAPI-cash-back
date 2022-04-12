import datetime
from sql_alchemy import banco

class SaleModel(banco.Model):
    __tablename__ = 'sales'

    sale_id = banco.Column(banco.Integer, primary_key=True)
    sold_at = banco.Column(banco.String(20))
    total = banco.Column(banco.Float(precision=2))
    customer_id = banco.Column(banco.Integer, banco.ForeignKey('customers.customer_id'))
    products = banco.relationship('ProductModel')
    customer = banco.relationship('CustomerModel')

    def __init__(self, customer_id, sold_at, total):
        self.customer_id = customer_id
        self.sold_at = sold_at
        self.total = total

    def json(self):
        return {
            'sale_id': self.sale_id,
            'sold_at': self.sold_at,
            'customer_id': self.customer.json(),
            'total': self.total,
            'products': [product.json() for product in self.products]          
        }

    @classmethod
    def valid_date(cls, date: str)->bool:
        date_format = '%Y-%m-%d %H:%M:%S'    
        try:
            date_obj = datetime.datetime.strptime(date, date_format)
            return True
        except:    
            return False

    def save_sale(self):
        banco.session.add(self)
        banco.session.flush()
