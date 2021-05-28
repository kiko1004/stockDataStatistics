import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import yfinance as yf
from matplotlib.pyplot import figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import statistics

class DataTicker:

    def __init__(self, ticker, period):
        self.asset = yf.Ticker(ticker)
        asset = self.asset
        self.data = self.asset.history(period=period)
        data = self.data
        data['H_L'] = (
            abs(data['High'] - data['Low'])
        )
        data['O_C'] = (
            abs(data['Open'] - data['Close'])
        )
        data['difInHigh'] = (
            abs(data['High'] - data['High'].shift(1))
        )
        data['difInLow'] = (
            abs(data['Low'] - data['Low'].shift(1))
        )
        conditions = [
            (data['Open'] >= data['Close']),
            (data['Open'] < data['Close']),
        ]
        values = ['Bear', 'Bull']
        data['Bar'] = np.select(conditions, values)
        conditions = [
            (data['Open'] >= data['Close'].shift(1)),
            (data['Open'] < data['Close'].shift(1)),
        ]
        values = ['OpenedHigher', 'OpenedLower']
        data['OpenedGap'] = np.select(conditions, values)

        self.volumAvg = round(statistics.mean(data['Volume']), 2)
        self.volumMean = round(statistics.median(data['Volume']), 2)

        self.HighLowMean = round(statistics.mean(data['H_L']), 4)
        self.HighLowMedian = round(statistics.median(data['H_L']), 4)

        self.OpenCloseMean = round(statistics.mean(data['O_C']), 4)
        self.OpenCloseMedian = round(statistics.median(data['O_C']), 4)

        self.diffInHighAvg = round(np.nanmean(data['difInHigh']), 4)
        self.diffInHighMedian = round(statistics.median(data['difInLow']), 4)

        self.diffInLowAvg = round(np.nanmean(data['difInLow']), 4)
        self.diffInLowMedian = round(statistics.median(data['difInLow']), 4)
        self.industry = asset.info['sector']
        Bear = data['Bar'].value_counts()['Bear']
        Bull = data['Bar'].value_counts()['Bull']
        BearPercent = round(Bear / (Bull + Bear) * 100, 3)
        BullPercent = round(Bull / (Bull + Bear) * 100, 3)
        OpenedHigher = data['OpenedGap'].value_counts()['OpenedHigher']
        OpenedLower = data['OpenedGap'].value_counts()['OpenedLower']
        OHpercent = round(OpenedHigher * 100 / (OpenedHigher + OpenedLower), 3)
        OLpercent = round(OpenedLower * 100 / (OpenedHigher + OpenedLower), 3)
        data['DiffinOpen'] = (
            abs(data['Close'].shift(1) - data['Open'])
        )
        DiffinOpenAvg = round(np.nanmean(data['DiffinOpen']), 4)
        DiffinOpenMedian = round(statistics.median(data['DiffinOpen']), 4)
        self.DiffinOpenAvg = DiffinOpenAvg
        self.DiffinOpenMedian = DiffinOpenMedian
        self.Bear = Bear
        self.Bull = Bull
        self.BullPercent = BullPercent
        self.BearPercent = BearPercent
        self.OpenedHigher = OpenedHigher
        self.OpenedLower = OpenedLower
        self.OHpercent = OHpercent
        self.OLpercent = OLpercent
        Last_Low = data['Low'].iloc[-1]
        Bid = round((Last_Low - ((self.diffInLowAvg + self.diffInLowMedian) / 2)), 2)
        self.Bid = Bid
        Last_High = data['High'].iloc[-1]
        Ask = round((Last_High + ((self.diffInHighAvg + self.diffInHighMedian) / 2)), 2)
        self.Ask = Ask
        self.Last_Low = Last_Low
        self.Last_High = Last_High
        conditions = [
            ((data['Open'] > data['Close'].shift(1)) & (data['Open'] > data['Close'])),
            ((data['Open'] < data['Close'].shift(1)) & (data['Open'] < data['Close'])),
            ((data['Open'] < data['Close'].shift(1)) & (data['Open'] > data['Close'])),
            ((data['Open'] > data['Close'].shift(1)) & (data['Open'] < data['Close'])),

        ]
        values = [True, True, False, False]
        data['ImbalanceCounter'] = np.select(conditions, values)
        x = (data['ImbalanceCounter'].sum() / data['ImbalanceCounter'].count()) * 100
        percent = str(round(x, 2)) + '%'
        self.ImbalanceCounter = percent


    def plotG(self):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        xs = self.data['Date']
        ys = self.data['H_L']
        axis.plot(xs, ys)
        return fig

