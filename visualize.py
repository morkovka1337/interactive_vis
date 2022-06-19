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
volume_l_top= []
volume_l_bottom= []
labels_pred = []
price_pred_l = []
vol2 = vol.twinx()
labels_top = []
labels_bottom = []
price_l_top = []
price_l_bottom = []

def draw_volume(df, drawing_tokens, vol, cmap, selected_line_style, marker, volume_l_top, volume_l_bottom, vol2, labels_top, labels_bottom):
    for i, ticker in enumerate(drawing_tokens):
        x = pd.Series(map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').date(), df[df.Ticker == ticker].Date.to_list()))
        y = df[df.Ticker == ticker].Volume.astype(int)
        if ticker in ("BTC-USD", "ETH-USD"):
            l, = vol2.plot(x, y, label=ticker, color=cmap(i), marker=marker, markersize=1, ls=selected_line_style)
            volume_l_bottom.append(l)
            labels_bottom.append(ticker + " (dashed)")

        else:
            if ticker == "BTCB-USD":
                l, = vol.plot(x, y, label=ticker, color=cmap(i), marker=marker, markersize=1, ls=selected_line_style)
                volume_l_bottom.append(l)
                labels_bottom.append(ticker + " (dashed)")
            else:
                l, = vol.plot(x, y, label=ticker, color=cmap(i))
                volume_l_top.append(l)
                labels_top.append(ticker)

draw_volume(df, drawing_tokens, vol, cmap, selected_line_style, marker, volume_l_top, volume_l_bottom, vol2, labels_top, labels_bottom)

vol.set_xlabel('Date')
vol.set_ylabel('Volume')
vol.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
vol.set_title('Volume over time', size=20)
prc2 = prc.twinx()


def draw_price(df, drawing_tokens, prc, cmap, selected_line_style, marker, labels_pred, price_pred_l, price_l_top, price_l_bottom, prc2):
    for i, ticker in enumerate(drawing_tokens):
        x = pd.Series(map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').date(), df[df.Ticker == ticker].Date.to_list()))
        y = (df[df.Ticker == ticker].Open + df[df.Ticker == ticker].Close) / 2
        if ticker in ("BTC-USD", "BTCB-USD"):
            l, = prc2.plot(x, y, label=ticker, color=cmap(i), marker=marker, markersize=1, ls=selected_line_style)
            price_l_bottom.append(l)

        else:
            if ticker == 'ETH-USD':
                l, = prc.plot(x, y, label=ticker, color=cmap(i), marker=marker, markersize=1, ls=selected_line_style)
                price_l_bottom.append(l)
            else:
                l, = prc.plot(x, y, label=ticker, color=cmap(i))
                price_l_top.append(l)

        if ticker in ("BTC-USD", "ETH-USD", ):
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
                l, = prc2.plot(x, y_pred, label=ticker + " (prediction)", color=cmap(i))
            else:
                l, = prc.plot(x, y_pred, label=ticker + " (prediction)", color=cmap(i))
            labels_pred.append(ticker + ' (prediction)')
            price_pred_l.append(l)

draw_price(df, drawing_tokens, prc, cmap, selected_line_style, marker, labels_pred, price_pred_l, price_l_top, price_l_bottom, prc2)

prc.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

lines = np.array([volume_l_top, price_l_top]).T

def create_legend(fig, labels_top, lines, visible, offset):
    interactive_legend_top = plugins.InteractiveLegendPlugin(lines,
                                                     labels_top,
                                                     alpha_unsel=0.05,
                                                     alpha_over=1.5,
                                                     start_visible=visible, legend_offset = offset)
    plugins.connect(fig, interactive_legend_top)

create_legend(fig, labels_top, lines, False, offset=(100, 50))
lines = np.array([volume_l_bottom, price_l_bottom]).T
create_legend(fig, labels_bottom, lines, True, offset=(100, 580))
create_legend(fig, labels_pred, price_pred_l, False, offset=(100, 630))


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
