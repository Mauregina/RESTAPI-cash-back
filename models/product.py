from sql_alchemy import banco

class ProductModel(banco.Model):
    __tablename__ = 'products'

    product_id = banco.Column(banco.Integer, primary_key=True)
    type = banco.Column(banco.String(1), nullable=False)
    value = banco.Column(banco.Float(precision=2), nullable=False)
    qty = banco.Column(banco.Integer, nullable=False)
    sale_id = banco.Column(banco.Integer, banco.ForeignKey('sales.sale_id'), nullable=False)

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
    def valid_sum_total_product(cls, total, products_lst)->bool:
        sum_total_products = 0
        for product in products_lst:
            value = product.get('value')
            qty = product.get('qty')

            total_product = float(value) * int(qty)
            sum_total_products += total_product
        
        format_sum_total_product = "{:.2f}".format(sum_total_products)
        format_total = "{:.2f}".format(total)
        
        return format_total == format_sum_total_product             

    @classmethod
    def valid_type(cls, type: str)->bool:
        if type in ['A', 'B', 'C']:
            return True
        return False    

    def save_product(self):
        banco.session.add(self)
               
