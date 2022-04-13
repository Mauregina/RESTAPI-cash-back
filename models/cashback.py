from sql_alchemy import banco
from requests import post

class CashbackModel(banco.Model):
    __tablename__ = 'cachbacks'

    cashback_id = banco.Column(banco.Integer, primary_key=True)
    cashback_value = banco.Column(banco.Float(precision=2), nullable=False)
    cashback_sent = banco.Column(banco.Boolean, nullable=False)
    api_response = banco.Column(banco.String(500))
    sale_id = banco.Column(banco.Integer, banco.ForeignKey('sales.sale_id'), nullable=False)   

    def __init__(self, total, sale_id):
        self.cashback_value = self.calc_cashback(total)
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

    def calc_cashback(self, total):
        total_float = float(total)
        cashback = total_float*0.1
        return "{:.2f}".format(cashback)          

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
