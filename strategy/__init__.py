# -*- coding:utf-8 -*- 
from pyalgotrade import strategy
from lib import mongofeed
import os
import datetime
class TroyStrategy(strategy.BacktestingStrategy):
    
    def __init__(self,start,end):
        ''' load all the ashare feed'''
        '''
        project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_root_dir = os.path.join(project_root_dir,"data","history")
        feed = yahoofeed.Feed()
        for _,_,filenames in os.walk(data_root_dir):
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.csv':
                    stock_code = os.path.splitext(filename)[0]
                    csvfile = os.path.join(data_root_dir, filename)
                    feed.addBarsFromCSV(stock_code, csvfile)
        '''
    
        self._start_date = datetime.datetime.strptime(start,'%Y-%m-%d')
        self._end_date = datetime.datetime.strptime(end,'%Y-%m-%d')
        
        #1 year ago
        start_date_last_year = self._start_date - datetime.timedelta(days=360)
        feed_start_date = start_date_last_year.strftime('%Y-%m-%d')
        feed_end_date = self._end_date.strftime('%Y-%m-%d')
            

        feed = mongofeed.Feed(feed_start_date, feed_end_date)
        feed.loadAllBars()
        project_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(project_root_dir,"data","sh.csv")
        feed.loadBarsFromCSV("sh", csv_file_path)
        
        strategy.BacktestingStrategy.__init__(self, feed)
        self.setUseAdjustedValues(True)
        self._feed = self.getFeed()
        self._universe = []
        
        
    def before_trading(self,bars):
        '''更新股票池'''
        pass
    def handle_data(self,bars):
        pass
    def onBars(self, bars):
        current_date = bars.getDateTime()
        if self._start_date is not None and current_date < self._start_date:
            return
        if self._end_date is not None and current_date > self._end_date:
            return
        self.before_trading(bars)
        instruments = self.get_universe()
        self.handle_data(bars,instruments)
    def get_universe(self):
        return self._universe
    def update_universe(self,instruments):
        self._universe = instruments
    
    def history(self,instrument,field,period):
        assert(type(period) is int)
        assert(period > 0)
        bards = self._feed.getDataSeries(instrument)
        if field == 'open':
            ds = bards.getOpenDataSeries()
        elif field == 'high':
            ds = bards.getHighDataSeries()
        elif field == 'low':
            ds = bards.getLowDataSeries()
        elif field == 'close':
            ds = bards.getCloseDataSeries()
        elif field == 'adjclose':
            ds = bards.getAdjCloseDataSeries()
        elif field == 'volume':
            ds = bards.getVolumeDataSeries()
        else:
            ds = bards.getPriceDataSeries()
        return ds[-period:]
        