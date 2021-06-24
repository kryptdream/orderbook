from orderbook import OrderBook, Order, Part 
import pytest
import re
import random

def generate_new_order(order_id):
    return Order(order_id, random.choices([Part.BUY.value, Part.SELL.value])[0], \
                random.randint(2000,10000), random.randint(100,1000))

def test_orderbook_class_positive():
    OrderBook()

def test_orderbook_class_with_redundancy_arg():
    with pytest.raises(TypeError):
        OrderBook(123)

def test_add_order_positive():
    orderbook = OrderBook()
    orderbook.add_order(Order(1006, Part.SELL.value, 9600, 255))
    
def test_add_order_empty_field():
    orderbook = OrderBook()
    with pytest.raises(TypeError):
        orderbook.add_order()
        
def test_add_order_wrong_order():
    orderbook = OrderBook()
    with pytest.raises(TypeError):
        orderbook.add_order('123')

def test_add_order_wrong_type():
    orderbook = OrderBook()
    with pytest.raises(TypeError):
        orderbook.add_order(Order(1006, [], 9600, 255))
    with pytest.raises(TypeError):
        orderbook.add_order(Order('g', Part.SELL.value, 9600, 255))
    with pytest.raises(TypeError):
        orderbook.add_order(Order(1001, Part.SELL.value, 'g', 255))
    with pytest.raises(TypeError):
        orderbook.add_order(Order(1001, Part.SELL.value, 9600, 'g'))

def test_remove_order_positive():
    orderbook = OrderBook()
    orderbook.add_order(Order(1004, Part.SELL.value, 9600, 255))
    orderbook.remove_order(1004)

def test_remove_order_wrong_order_id():
    orderbook = OrderBook()
    orderbook.add_order(Order(1004, Part.SELL.value, 9600, 255))
    with pytest.raises(KeyError):
        orderbook.remove_order(1005)

def test_get_order_by_id_positive():
    pattern_type = re.compile('ask|bid')
    orderbook = OrderBook()
    orderbook.add_order(Order(1004, Part.SELL.value, 9600, 255))
    d = orderbook.get_order_by_id(1004)
    assert isinstance(d[0], str)
    assert isinstance(d[1], int)
    assert isinstance(d[2], int)
    assert re.match(pattern_type, d[0])
    assert re.match('[0-9]+', str(d[1]))
    assert re.match('[0-9]+', str(d[2]))

def test_get_order_by_id_wrong_order_id():
    orderbook = OrderBook()
    orderbook.add_order(Order(1004, Part.SELL.value, 9600, 255))
    with pytest.raises(KeyError):
        orderbook.get_order_by_id(1005)

def test_modify_order_positive():
    orderbook = OrderBook()
    orderbook.add_order(Order(1004, Part.SELL.value, 9600, 255))
    orderbook.modify_order(1004, 7600, 155)

def test_modify_order_wrong_order_id():
    orderbook = OrderBook()
    orderbook.add_order(Order(1004, Part.SELL.value, 9600, 255))
    with pytest.raises(KeyError):
        orderbook.modify_order(1005, 7600, 155)

def test_modify_order_price_wrong_type():
    orderbook = OrderBook()
    orderbook.add_order(Order(1004, Part.SELL.value, 9600, 255))
    with pytest.raises(TypeError):
        orderbook.modify_order(1004, '1', 155)

def test_modify_order_volume_wrong_type():
    orderbook = OrderBook()
    orderbook.add_order(Order(1004, Part.SELL.value, 9600, 255))
    with pytest.raises(TypeError):
        orderbook.modify_order(1004,  7600, [])

def test_get_book_snapshot_positive():
    ask_pattern_orderbook = re.compile(r'{ \'Asks\': \[(?:{\'price\': [0-9]+, \'volume\': [0-9]+}..)+')
    bid_pattern_orderbook = re.compile(r'.*\'Bids\': \[(?:{\'price\': [0-9]+, \'volume\': [0-9]+}..)+')
    orderbook = OrderBook()
    orders = [Order(1001, Part.BUY.value, 7500, 400),
          Order(1002, Part.BUY.value, 7500, 250),
          Order(1003, Part.SELL.value, 7600, 300),
          Order(1004, Part.SELL.value, 7600, 150),
          Order(1005, Part.BUY.value, 9500, 250),
          Order(1006, Part.SELL.value, 9600, 255),
          ]
    orderbook.add_order(orders)
    orderbook.get_book_snapshot()
    assert isinstance(orderbook.get_book_snapshot(), str)
    assert re.match(ask_pattern_orderbook, orderbook.get_book_snapshot())
    assert re.match(bid_pattern_orderbook, orderbook.get_book_snapshot())
    
def test_get_book_snapshot_for_small_list_of_order():
    ask_pattern_orderbook = re.compile(r'{ \'Asks\': \[(?:{\'price\': [0-9]+, \'volume\': [0-9]+}..)+')
    bid_pattern_orderbook = re.compile(r'.*\'Bids\': \[(?:{\'price\': [0-9]+, \'volume\': [0-9]+}..)+')
    orders = []
    orderbook = OrderBook()
    for i in range(1001,1100):
        orders.append(generate_new_order(i))
    orderbook.add_order(orders)
    orderbook.get_book_snapshot()
    assert isinstance(orderbook.get_book_snapshot(), str)
    assert re.match(ask_pattern_orderbook, orderbook.get_book_snapshot())
    assert re.match(bid_pattern_orderbook, orderbook.get_book_snapshot())

def test_get_book_snapshot_for_big_list_of_order():
    ask_pattern_orderbook = re.compile(r'{ \'Asks\': \[(?:{\'price\': [0-9]+, \'volume\': [0-9]+}..)+')
    bid_pattern_orderbook = re.compile(r'.*\'Bids\': \[(?:{\'price\': [0-9]+, \'volume\': [0-9]+}..)+')
    orders = []
    orderbook = OrderBook()
    for i in range(1001,5900):
        orders.append(generate_new_order(i))
    orderbook.add_order(orders)
    orderbook.get_book_snapshot()
    assert isinstance(orderbook.get_book_snapshot(), str)
    assert re.match(ask_pattern_orderbook, orderbook.get_book_snapshot())
    assert re.match(bid_pattern_orderbook, orderbook.get_book_snapshot())
