from sql_alchemy import banco

class SaleModel(banco.Model):
    __tablename__ = 'sales'

    sale_id = banco.Column(banco.Integer, primary_key=True)
    total = banco.Column(banco.Float(precision=2))
    type = banco.Column(banco.String(1))
    value = banco.Column(banco.Float(precision=2))
    qty = banco.Column(banco.Integer)
    #document = banco.Column(banco.Integer, banco.ForeignKey('customers.document'))

    def __init__(self, total, type, value, qty):
        self.total = total
        self.type =type
        self.value = value
        self.qty = qty

    def json(self):
        return {
            'sale_id': self.sale_id,
            'total': self.total,
            'type': self.type,
            'value': self.value,
            'qty': self.qty           
        }

    def save_sale(self):
        banco.session.add(self)
        banco.session.commit()

