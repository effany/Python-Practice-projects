class CartManger:
    def __init__(self):
        self.cart_items = []
        self.total_price = 0

    def add_item(self, item):
        self.cart_items.append(item)
    
    def remove_item(self, id):
        for item in self.cart_items:
            if item['id'] == id:
                self.cart_items.remove(item)

    def sub_total(self):
        price = 0
        for item in self.cart_items:
            if item['itemDiscountPrice'] != 'None':
                price += float(item['itemDiscountPrice']) * int(item['itemCount'])
            else:
                price += float(item['itemPrice']) * int(item['itemCount'])
        self.total_price = price