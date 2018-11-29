from future.utils import tobytes
from ctypes import *
from passlib.handlers.mssql import BIDENT

class BaseTickStruct(Structure):
    _pack_ = 1
    _fields_ = [
        ('symbol',c_char*16),
        ('time',c_double),
        ('bid',c_int),
        ('ask',c_int)]
    
    def __init__(self, symbol="NONE", time=0, bid=0, ask=0):
        self.symbol = tobytes(symbol)
        self.time = time
        self.bid = bid
        self.ask = ask
        
    def to_row(self):
        return [str(self.symbol.decode('utf8')), self.time, self.bid, self.ask]
    
    def __repr__(self):
        return "BaseTickStruct symbol:%s time:%.5f bid:%.5f ask:%.5f"%(self.symbol, self.time, self.bid, self.ask)

class ExecutionTickStruct(Structure):
    _pack_ = 1
    _fields_ = [
        ('symbol',c_char*16),
        ('time',c_double),
        ('price',c_int),
        ('order_type',c_int),
        ('amount',c_int)]
    
    def __init__(self, symbol="NONE", time=0, price=0, order_type=0, amount=0):
        self.symbol = tobytes(symbol)
        self.time = time
        self.price = price
        self.bid = price
        self.ask = price
        self.order_type = order_type
        self.amount = amount
        
    def to_row(self):
        return [str(self.symbol.decode('utf8')), self.time, self.price, self.order_type, self.amount]
    
    def __repr__(self):
        return "BaseTickStruct symbol:%s time:%.5f price:%d order_type:%d, amount:%d"%(self.symbol, self.time, self.price, self.order_type, self.amount)
