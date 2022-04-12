from sql_alchemy import banco

class ProductModel(banco.Model):
    __tablename__ = 'products'

    sum_total_product = 0

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
        total = float(value) * int(qty)
        ProductModel.sum_total_product += total

    def json(self):
        return {
            'product_id': self.product_id,
            'sale_id': self.sale_id,
            'type': self.type,
            'value': self.value,
            'qty': self.qty           
        }

    @classmethod
    def valid_value(cls, value)->bool:
        try:
            float(value)
            return True
        except: 
            return False

    @classmethod
    def valid_qty(cls, qty)->bool:
        try:
            float(qty)
            return True
        except: 
            return False            

    @classmethod
    def valid_sum_total_product(cls, total)->bool:
        format_sum_total_product = "{:.2f}".format(cls.sum_total_product)
        format_total = "{:.2f}".format(total)
        return format_total == format_sum_total_product

    @classmethod
    def zero_sum_total_product(cls):
        cls.sum_total_product = 0               

    @classmethod
    def valid_type(cls, type: str)->bool:
        if type in ['A', 'B', 'C']:
            return True
        return False    

    @classmethod
    def calc_cash_back(cls, products_lst)->float:
        print(products_lst)

    def save_product(self):
        banco.session.add(self)
        
    def commit_product(self):
        banco.session.commit()        
