import dataTicker as dt
from flask import Flask, render_template, make_response
from flask import request, redirect
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-data", methods=["GET", "POST"])
def get_data():
    ticker = "NOT FOUND"
    if request.method == "POST":
        try:
            req = request.form
            ticker = req.get("ticker")
            dTicker = dt.DataTicker(ticker)
            return render_template("index.html", volumAvg=dTicker.volumAvg, volumMean = dTicker.volumMean,
                                   HighLowMean = dTicker.HighLowMean, HighLowMedian = dTicker.HighLowMedian, OpenCloseMean = dTicker.OpenCloseMean,
                                   OpenCloseMedian = dTicker.OpenCloseMedian, diffInHighAvg = dTicker.diffInHighAvg,
                                   diffInHighMedian = dTicker.diffInHighMedian, diffInLowAvg = dTicker.diffInLowAvg, diffInLowMedian = dTicker.diffInLowMedian
                                   )


        except:
            pass

    render_template("index.html")
