from sql_alchemy import banco

class CustomerModel(banco.Model):
    __tablename__ = 'costumers'

    document = banco.Column(banco.Integer, primary_key=True)
    name = banco.Column(banco.String(100))

    def __init__(self, document, name):
        self.document = document
        self.name = name

    def json(self):
        return {
            'document': self.document,
            'name': self.name
        }

    @classmethod
    def find_customer(cls, document):
        customer = cls.query.filter_by(document=document).first()

        if customer:
            return customer
        return None    

    def save_customer(self):
        banco.session.add(self)
        banco.session.commit()
