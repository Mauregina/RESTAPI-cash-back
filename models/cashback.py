from sql_alchemy import banco
from requests import post

class CashbackModel(banco.Model):
    __tablename__ = 'cachbacks'

    cashback_id = banco.Column(banco.Integer, primary_key=True)
    cashback_value = banco.Column(banco.Float(precision=2))
    sale_id = banco.Column(banco.Integer, banco.ForeignKey('sales.sale_id'))   
    cashback_sent = banco.Column(banco.Boolean)
    api_response = banco.Column(banco.String(500))

    def __init__(self, cashback_value, sale_id):
        self.cashback_value = cashback_value
        self.sale_id = sale_id
        self.cashback_sent = False

    def json(self):
        return {
            'cashback_id': self.cashback_id,
            'cashback_value': self.cashback_value,
            'sale_id': self.sale_id,
            'cashback_sent': self.cashback_sent,  
            'api_response': self.api_response     
        }            

    @classmethod
    def find_cashback(cls, cashback_id):
        cashback = cls.query.filter_by(cashback_id=cashback_id).first()

        if cashback:
            return cashback   
        return None

    @classmethod
    def send_cashback_maistodos(cls, document, cashback_value):
        url = 'https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback'

        body = {'document': document,
                'cashback': cashback_value  
        }

        header = {
            'Content-Type': 'application/json'
        }

        response = post(url, json=body, headers=header)   

        if response.status_code == 201:
            return response.json()

        return None

    def save_cashback(self):
        banco.session.add(self)
        banco.session.flush()
        banco.session.commit()
