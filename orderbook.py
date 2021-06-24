from enum import Enum
from collections import defaultdict
from dataclasses import dataclass
import re

class Part(Enum):
    """
    Data class for type of order 
    """
    BUY = 'bid'
    SELL = 'ask'

class OrderBook:
    """ 
    Base class for working with OrderBook
    """
    def __init__(self):
        self.orders = {}
        self.ask_snapshot = defaultdict(list)
        self.bid_snapshot = defaultdict(list)
        self.ask_prices = []
        self.bid_prices = []
        self.ask_volumes = []
        self.bid_volumes = []
        self.ask_book = []
        self.bid_book = []



    def _add_order(self, order):
        pattern_type = re.compile('%s|%s' %(Part.BUY.value,Part.SELL.value))
        if isinstance(order, Order):
            for i in [order.order_id, order.price, order.volume]:
                if isinstance(i, int):
                    if isinstance(order.type, str) and re.match(pattern_type, order.type):
                        self.orders[order.order_id] = order
                    else:
                        raise TypeError('{0} is not valid istance'.format(order.type))
                else:
                    raise TypeError('{0} is not int istance'.format(i))
        else:
            raise TypeError('{0} is not order istance'.format(order))

    def add_order(self, orders):
        """ 
        Adding an order or orders to the OrderBook dict
        """
        if isinstance(orders, list):
            for order in orders:
                self._add_order(order)
        else:
            self._add_order(orders)

    def remove_order(self, order_id):
        """ 
        Removing an order from the OrderBook dict
        """
        self.orders.pop(order_id)

    def get_order_by_id(self, order_id):
        """ 
        Getting the order instance by order_id
        """
        if order_id in self.orders:
            order = self.orders.get(order_id)
            return (order.type, order.price, order.volume)
        raise KeyError('{0} is not in orders dict'.format(order_id))


    def modify_order(self, order_id, price, volume):
        """ 
        Updating the price or volume of the order if they were changed
        """
        if order_id in self.orders:
            for instance in price, volume:
                if not isinstance(instance, int):
                    raise TypeError('{0} is not int istance'.format(instance))
            if self.orders[order_id].price != price:
                self.orders[order_id].price = price
            if self.orders[order_id].volume != volume:
                self.orders[order_id].volume = volume
        else:
            raise KeyError('{0} is not in orders dict'.format(order_id))

    def _get_book_prices(self):
        """
        Preparing sorted price lists
        """
        for k in self.orders.keys():
            if self.orders[k].type == 'ask':
                self.ask_prices.append(self.orders[k].price)
                self.ask_snapshot[k] = self.orders[k]
            elif self.orders[k].type == 'bid':
                self.bid_prices.append(self.orders[k].price)
                self.bid_snapshot[k] = self.orders[k]
        # Sorting and removing dubbing
        self.ask_prices = list(dict.fromkeys(sorted(self.ask_prices)))
        self.bid_prices = list(dict.fromkeys(sorted(self.bid_prices, reverse=True)))

    def _get_book_summary(self):
        """ 
        Preparing combined volume lists
        """
        self._get_book_prices()
        for price in self.ask_prices:
            volume = 0
            for k in self.ask_snapshot.keys():
                if self.ask_snapshot[k].price == price:
                    volume += self.ask_snapshot[k].volume
            self.ask_volumes.append(volume)
        for price in self.bid_prices:
            volume = 0
            for k in self.bid_snapshot.keys():
                if self.bid_snapshot[k].price == price:
                    volume += self.bid_snapshot[k].volume
            self.bid_volumes.append(volume)

    def get_book_snapshot(self):
        """
        Shows current orderbook 
        """
        self._get_book_summary()
        # Preparing book lists
        for i in range(len(self.ask_prices)):
            self.ask_book.append({'price':self.ask_prices[i], 'volume': self.ask_volumes[i]})
        for i in range(len(self.bid_prices)):
            self.bid_book.append({'price':self.bid_prices[i], 'volume': self.bid_volumes[i]})
        return "{ 'Asks': %s 'Bids': %s  }" % (self.ask_book, self.bid_book)

@dataclass
class Order:
    """ 
    Class for fixing type of the fields of the order
    """
    order_id: int 
    type: str
    price: int
    volume: int
