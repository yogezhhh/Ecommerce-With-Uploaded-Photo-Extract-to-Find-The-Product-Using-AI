from decimal import Decimal
from .models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, qty=1):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {'qty': 0, 'price': str(product.price)}
        self.cart[pid]['qty'] += qty
        self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def update(self, product_id, qty):
        pid = str(product_id)
        if pid in self.cart:
            if qty <= 0:
                del self.cart[pid]
            else:
                self.cart[pid]['qty'] = qty
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        self.session.modified = True

    def __iter__(self):
        ids = self.cart.keys()
        products = Product.objects.filter(id__in=ids)
        for p in products:
            item = self.cart[str(p.id)]
            yield {
                'product': p,
                'qty': item['qty'],
                'price': Decimal(item['price']),
                'subtotal': Decimal(item['price']) * item['qty'],
            }

    def __len__(self):
        return sum(i['qty'] for i in self.cart.values())

    def total(self):
        return sum(Decimal(i['price']) * i['qty'] for i in self.cart.values())