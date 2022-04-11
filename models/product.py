from sql_alchemy import banco

class ProductModel(banco.Model):
    __tablename__ = 'products'

    product_id = banco.Column(banco.Integer, primary_key=True)
    type = banco.Column(banco.String(1))
    value = banco.Column(banco.Float(precision=2))
    qty = banco.Column(banco.Integer)
    sale_id = banco.Column(banco.Integer, banco.ForeignKey('sales.sale_id'))

    def __init__(self, sale_id, type, value, qty):
        self.sale_id = sale_id
        self.type =type
        self.value = value
        self.qty = qty

    def json(self):
        return {
            'product_id': self.product_id,
            'sale_id': self.sale_id,
            'type': self.type,
            'value': self.value,
            'qty': self.qty           
        }

    def save_product(self):
        banco.session.add(self)
        banco.session.commit()

