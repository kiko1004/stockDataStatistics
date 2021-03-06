import dataTicker as dt
from flask import Flask, render_template, make_response
from flask import request, redirect
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
from io import BytesIO
from flask import Response

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get-data", methods=["GET", "POST"])
def get_data():
    try:
        if len(request.form) > 0:
            ticker = "NOT FOUND"
            if request.method == "POST":
                try:
                    req = request.form
                    ticker = req.get("ticker")
                    period = req.get("period")

                    try:
                        dTicker = dt.DataTicker(ticker or "AAPL", period)
                        fig = Figure(figsize=(8, 6))
                        ax = fig.subplots()
                        ax.plot(dTicker.data['H_L'])
                        ax.set_title('High-Low Difference')
                        # Save it to a temporary buffer.
                        buf = BytesIO()
                        fig.savefig(buf, format="png")
                        # Embed the result in the html output.
                        data = base64.b64encode(buf.getbuffer()).decode("ascii")
                        code = f"data:image/png;base64,{data}"
                        return render_template("index.html", volumAvg=dTicker.volumAvg, volumMean=dTicker.volumMean,
                                               HighLowMean=dTicker.HighLowMean, HighLowMedian=dTicker.HighLowMedian,
                                               OpenCloseMean=dTicker.OpenCloseMean,
                                               OpenCloseMedian=dTicker.OpenCloseMedian,
                                               diffInHighAvg=dTicker.diffInHighAvg,
                                               diffInHighMedian=dTicker.diffInHighMedian,
                                               diffInLowAvg=dTicker.diffInLowAvg,
                                               diffInLowMedian=dTicker.diffInLowMedian, sector=dTicker.industry,
                                               ticker=ticker, img=code, data=data, Bear=dTicker.Bear,
                                               BearPercent=dTicker.BearPercent,
                                               Bull=dTicker.Bull, BullPercent=dTicker.BullPercent,
                                               OpenedHigher=dTicker.OpenedHigher, OpenedLower=dTicker.OpenedLower,
                                               OHpercent=dTicker.OHpercent, OLpercent=dTicker.OLpercent,
                                               DiffinOpenAvg = dTicker.DiffinOpenAvg, DiffinOpenMedian=dTicker.DiffinOpenMedian,
                                               Last_Low = dTicker.Last_Low, Last_High = dTicker.Last_High,
                                               Bid = dTicker.Bid, Ask = dTicker.Ask, ImbalanceCounter = dTicker.ImbalanceCounter)
                    except:
                        ticker = "N/A"
                        return render_template("index.html", ticker=ticker)



                except:
                    ticker = "N/A"
                    return render_template("index.html", ticker=ticker)

        else:
            return render_template("index.html")
    except:
        ticker = "N/A"
        return render_template("index.html", ticker = ticker)

