import csv
import datetime
import os, errno
class TickWriter(object):
    def __init__(self, symbol, root_path, company_name):
        self.symbol = symbol
        self.root_path = root_path
        self.company_name = company_name
        self.file = None
        self.writer = None
        self.last_tick_time = None
        self.last_tick = None
        
    def is_new_day(self, tick_time):
        result = False
        if self.last_tick_time == None:
            result = True
        elif self.last_tick_time.year != tick_time.year or self.last_tick_time.month != tick_time.month or self.last_tick_time.day != tick_time.day:
            result = True
        self.last_tick_time = tick_time
        return result
    
    def is_new_tick(self, tick):
        result = False
        if self.last_tick == None:
            result = True
        elif float(self.last_tick.time) != float(tick.time):
            result = True
        elif self.last_tick.bid != tick.bid or self.last_tick.ask != self.last_tick.ask:
            result = True
        self.last_tick = tick
        return result
    
    def get_path(self, tick_time):
        return os.path.join(self.root_path, self.symbol, self.company_name, "%04d"%(tick_time.year), "%02d"%(tick_time.month), "%02d"%(tick_time.day), "%s.csv"%(self.symbol))
        
    def open_writer(self, path):
        if self.file != None and self.file.closed == False:
            self.file.close()
        self.mkdir_p(os.path.dirname(path))
        self.file = open(path, "a")
        self.writer = csv.writer(self.file, lineterminator="\n")
        
    def write_tick(self, tick):
        self.writer.writerow(tick.to_row())
        self.file.flush()
    
    def record(self, tick, check_new_tick=True):
        tick_time = datetime.datetime.fromtimestamp(tick.time)
        
        if self.is_new_day(tick_time):
            self.file_path = self.get_path(tick_time)
            self.open_writer(self.file_path)
        if self.is_new_tick(tick) or not check_new_tick:
            self.write_tick(tick)
            
    def close(self):
        if self.file:
            self.file.close()
    
    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: 
                raise
