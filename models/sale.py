from sql_alchemy import banco

class SaleModel(banco.Model):
    __tablename__ = 'sales'

    sale_id = banco.Column(banco.Integer, primary_key=True)
    sold_at = banco.Column(banco.String(20))
    total = banco.Column(banco.Float(precision=2))
    products = banco.relationship('ProductModel')

    #document = banco.Column(banco.Integer, banco.ForeignKey('customers.document'))

    def __init__(self, sold_at, total):
        self.sold_at = sold_at
        self.total = total

    def json(self):
        return {
            'sale_id': self.sale_id,
            'sold_at': self.sold_at,
            'total': self.total,
            'products': [product.json() for product in self.products]          
        }

    def save_sale(self):
        banco.session.add(self)
        banco.session.flush()
        banco.session.commit()

