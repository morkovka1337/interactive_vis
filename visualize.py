import datetime
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
from mpld3 import plugins

np.random.seed(9615)
df = pd.read_csv("./currencies.csv")


drawing_tokens = [
    "UST-USD",
    "BTC-USD",
    "TONCOIN-USD",
    "SHIB-USD",
    "BTCB-USD",
    "BAT-USD",
    "BCH-USD",
    "BNB-USD",
    "DASH-USD",
    "DOGE-USD",
    "THETA-USD",
    "ETH-USD"
  ]
fig, (vol, prc) = plt.subplots(2, 1, figsize=(20, 12))
cmap = plt.get_cmap("Paired")
selected_line_style = '-.'
marker='.'
volume_l= []
labels_pred = []
price_pred_l = []
vol2 = None
for i, ticker in enumerate(drawing_tokens):
    x = pd.Series(map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').date(), df[df.Ticker == ticker].Date.to_list()))
    y = df[df.Ticker == ticker].Volume.astype(int)
    if ticker in ("BTC-USD", "BTCB-USD", "ETH-USD"):
        if vol2 is None:
            vol2 = vol.twinx()
        l, = vol2.plot(x, y, label=ticker, color=cmap(i), marker=marker, ls=selected_line_style)
        volume_l.append(l)
    else:
        l, = vol.plot(x, y, label=ticker, color=cmap(i))
        volume_l.append(l)

vol.set_xlabel('Date')
vol.set_ylabel('Volume')
vol.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
vol.set_title('Volume over time', size=20)
prc2 = None


price_l = []
for i, ticker in enumerate(drawing_tokens):
    x = pd.Series(map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').date(), df[df.Ticker == ticker].Date.to_list()))
    y = (df[df.Ticker == ticker].Open + df[df.Ticker == ticker].Close) / 2
    if ticker in ("BTC-USD", "BTCB-USD"):
        if prc2 is None:
            prc2 = prc.twinx()
        l, = prc2.plot(x, y, label=ticker, color=cmap(i), marker=marker, ls=selected_line_style)
        price_l.append(l)

    else:
        l, = prc.plot(x, y, label=ticker, color=cmap(i))
        price_l.append(l)

    if ticker in ("BTC-USD", "ETH-USD"):
        # price prediction for btc & eth
        last_date = x.tail(1).item()
        last_n_for_pred = 600
        x = x.index.to_list()[:last_n_for_pred]
        y = y.tail(last_n_for_pred)
        x_ind_last = int(x[-1])
        pol = np.polyfit(x, y, 4)
        model = np.poly1d(pol)
        x_for_pred = [ i for i in range(x_ind_last, x_ind_last + 30) ]
        y_pred = [model(i) for i in x_for_pred]
        x = pd.Series(last_date + datetime.timedelta(days = i + 1) for i in range(30))
        if ticker == 'BTC-USD':
            l, = prc2.plot(x, y_pred, label=ticker + "_prediction", color=cmap(i), ls=selected_line_style)
        else:
            l, = prc.plot(x, y_pred, label=ticker + "_prediction", color=cmap(i), ls=selected_line_style)
        labels_pred.append(ticker + '_prediction')
        price_pred_l.append(l)

labels = drawing_tokens[:]


prc.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

lines = np.array([volume_l, price_l]).T
interactive_legend = plugins.InteractiveLegendPlugin(lines,
                                                     labels,
                                                     alpha_unsel=0.05,
                                                     alpha_over=1.5,
                                                     start_visible=True, legend_offset=(50, 580))
plugins.connect(fig, interactive_legend)
interactive_legend = plugins.InteractiveLegendPlugin(price_pred_l,
                                                     labels_pred,
                                                     alpha_unsel=0.05,
                                                     alpha_over=1.5,
                                                     start_visible=True, legend_offset=(50, 880))
plugins.connect(fig, interactive_legend)

prc.set_xlabel('Date')
prc.set_ylabel('Price')
prc.set_title('Price over time', size=20)
prc2.tick_params(axis='y')
vol2.tick_params(axis='y')
prc.tick_params(axis='y')
vol.tick_params(axis='y')
fig.tight_layout()
prc2.patch.set_alpha(0.0) # otherwise lines from vol & prc do not show
vol2.patch.set_alpha(0.0)

fig.subplots_adjust(right=0.7)
mpld3.show(
    fig,
    port=8080,
    open_browser=False,
    )
