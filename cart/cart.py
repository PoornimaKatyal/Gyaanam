from decimal import Decimal

from django.conf import settings

from cart import module_loading
from cart import settings


class CartItem(object):
    """
    A cart item, with the associated book, its quantity and its price.
    """
    def __init__(self, book, quantity, price):
        self.book = book
        self.quantity = int(quantity)
        self.price = Decimal(str(price))

    def __repr__(self):
        return u'CartItem Object (%s)' % self.book

    def to_dict(self):
        return {
            'book_pk': self.book.pk,
            'quantity': self.quantity,
            'price': str(self.price),
        }

    @property
    def subtotal(self):
        """
        Subtotal for the cart item.
        """
        return self.price * self.quantity


class Cart(object):

    """
    A cart that lives in the session.
    """
    def __init__(self, session, session_key=None):
        self._items_dict = {}
        self.session = session
        self.session_key = session_key or settings.CART_SESSION_KEY
        print("in the cart class")
        print(self.session_key)
        print("user name %s" %self.session['username'])
            # If a cart representation was previously stored in session, then we
        if self.session_key in self.session:
            # rebuild the cart object from that serialized representation.
            cart_representation = self.session[self.session_key]
            print(cart_representation)
            ids_in_cart = cart_representation.keys()
            books_queryset = self.get_queryset().filter(pk__in=ids_in_cart)
            print("books_queryset")
            print(books_queryset)
            for book in books_queryset:
                item = cart_representation[str(book.pk)]
                self._items_dict[book.pk] = CartItem(book, item['quantity'], Decimal(item['price']))

    def __contains__(self, book):
        """
        Checks if the given book is in the cart.
        """
        return book in self.books

    def get_book_model(self):
        return module_loading.get_book_model()

    def filter_books(self, queryset):
        """
        Applies lookup parameters defined in settings.
        """
        lookup_parameters = getattr(settings, 'CART_book_LOOKUP', None)
        if lookup_parameters:
            queryset = queryset.filter(**lookup_parameters)
        return queryset

    def get_queryset(self):
        book_model = self.get_book_model()
        queryset = book_model._default_manager.all()
        queryset = self.filter_books(queryset)
        return queryset

    def update_session(self):
        """
        Serializes the cart data, saves it to session and marks session as modified.
        """
        self.session[self.session_key] = self.cart_serializable
        self.session.modified = True

    def add(self, book, price=None, quantity=1):
        """
        Adds or creates books in cart. For an existing book,
        the quantity is increased and the price is ignored.
        """
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError('Quantity must be at least 1 when adding to cart')
        if book in self.books:
            self._items_dict[book.pk].quantity += quantity
        else:
            if price == None:
                raise ValueError('Missing price when adding to cart')
            self._items_dict[book.pk] = CartItem(book, quantity, price)
        self.update_session()
        print("updated session:")
        print(self.session)

    def remove(self, book):
        """
        Removes the book.
        """
        if book in self.books:
            del self._items_dict[book.pk]
            self.update_session()

    def remove_single(self, book):
        """
        Removes a single book by decreasing the quantity.
        """
        if book in self.books:
            if self._items_dict[book.pk].quantity <= 1:
                # There's only 1 book left so we drop it
                del self._items_dict[book.pk]
            else:
                self._items_dict[book.pk].quantity -= 1
            self.update_session()

    def clear(self):
        """
        Removes all items.
        """
        self._items_dict = {}
        self.update_session()

    def set_quantity(self, book, quantity):
        """
        Sets the book's quantity.
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError('Quantity must be positive when updating cart')
        if book in self.books:
            self._items_dict[book.pk].quantity = quantity
            if self._items_dict[book.pk].quantity < 1:
                del self._items_dict[book.pk]
            self.update_session()

    @property
    def items(self):
        """
        The list of cart items.
        """
        return self._items_dict.values()

    @property
    def cart_serializable(self):
        """
        The serializable representation of the cart.
        For instance:
        {
            '1': {'book_pk': 1, 'quantity': 2, price: '9.99'},
            '2': {'book_pk': 2, 'quantity': 3, price: '29.99'},
        }
        Note how the book pk servers as the dictionary key.
        """
        cart_representation = {}
        for item in self.items:
            # JSON serialization: object attribute should be a string
            book_id = str(item.book.pk)
            cart_representation[book_id] = item.to_dict()
        return cart_representation


    @property
    def items_serializable(self):
        """
        The list of items formatted for serialization.
        """
        return self.cart_serializable.items()

    @property
    def count(self):
        """
        The number of items in cart, that's the sum of quantities.
        """
        return sum([item.quantity for item in self.items])

    @property
    def unique_count(self):
        """
        The number of unique items in cart, regardless of the quantity.
        """
        return len(self._items_dict)

    @property
    def is_empty(self):
        return self.unique_count == 0

    @property
    def books(self):
        """
        The list of associated books.
        """
        return [item.book for item in self.items]

    @property
    def total(self):
        """
        The total value of all items in the cart.
        """
        return sum([item.subtotal for item in self.items])
