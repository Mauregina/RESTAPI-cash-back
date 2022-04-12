from sql_alchemy import banco

class CashbackModel(banco.Model):
    __tablename__ = 'cachbacks'

    cashback_id = banco.Column(banco.Integer, primary_key=True)
    cashback_value = banco.Column(banco.Float(precision=2))
    sale_id = banco.Column(banco.Integer, banco.ForeignKey('sales.sale_id'))   
    cashback_sent = banco.Column(banco.Boolean)

    def __init__(self, cashback_value, sale_id):
        self.cashback_value = cashback_value
        self.sale_id = sale_id
        self.cashback_sent = False

    def json(self):
        return {
            'cashback_id': self.cashback_id,
            'cashback_value': self.cashback_value,
            'sale_id': self.sale_id,
            'cashback_sent': self.cashback_sent          
        }       

    def send_cashback_maistodos(self):
        pass    

    def save_cashback(self):
        banco.session.add(self)
        banco.session.commit()
