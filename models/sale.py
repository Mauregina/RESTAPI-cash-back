import datetime
from resources.cashback import Cashback
from sql_alchemy import banco

class SaleModel(banco.Model):
    __tablename__ = 'sales'

    sale_id = banco.Column(banco.Integer, primary_key=True)
    sold_dt = banco.Column(banco.String(20))
    total = banco.Column(banco.Float(precision=2))
    customer_id = banco.Column(banco.Integer, banco.ForeignKey('customers.customer_id'))
    products = banco.relationship('ProductModel')
    customer = banco.relationship('CustomerModel')
    cashback = banco.relationship('CashbackModel', backref='sales', uselist=False)

    def __init__(self, customer_id, sold_dt, total):
        self.customer_id = customer_id
        self.sold_dt = sold_dt
        self.total = total

    def json(self):
        return {
            'sale_id': self.sale_id,
            'sold_at': self.sold_dt,
            'customer_id': self.customer.json(),
            'total': self.total,
            'products': [product.json() for product in self.products],  
            'cashback': self.cashback.json()       
        }

    @classmethod
    def valid_date(cls, date: str)->bool:
        date_format = '%Y-%m-%d %H:%M:%S'    
        try:
            date_obj = datetime.datetime.strptime(date, date_format)
            return True
        except:    
            return False

    @classmethod
    def find_sale(cls, sale_id):
        sale = cls.query.filter_by(sale_id=sale_id).first()

        if sale:
            return sale   
        return None   

    def save_sale(self):
        banco.session.add(self)
        banco.session.flush()
