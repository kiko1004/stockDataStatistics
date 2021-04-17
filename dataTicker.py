import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import yfinance as yf
from matplotlib.pyplot import figure
import statistics

class DataTicker:

    def __init__(self, ticker):
        asset = yf.Ticker(ticker)
        data = asset.history(period="max")
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
