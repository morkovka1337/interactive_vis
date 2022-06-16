import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
import datetime
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
    "THETA-USD"
  ]



fig, (vol, prc) = plt.subplots(2, 1, figsize=(16, 18))
cmap = plt.get_cmap("Paired")
volume_l= []
for i, ticker in enumerate(drawing_tokens):
    x = pd.Series(map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').date(), df[df.Ticker == ticker].Date.to_list()))
    y = df[df.Ticker == ticker].Volume.astype(int)
    l, = vol.plot(x, y, label=ticker, color=cmap(i))
    vol.fill_between(x,
                    y * .95, y * 1.05,
                    color=l.get_color(), alpha=.1)
    volume_l.append(l)



vol.set_xlabel('Date')
vol.set_ylabel('Volume')
vol.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
fig.subplots_adjust(right=0.8)
vol.set_title('Volume over time', size=20)
price_l = []
for i, ticker in enumerate(drawing_tokens):
    x = pd.Series(map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d').date(), df[df.Ticker == ticker].Date.to_list()))
    y = (df[df.Ticker == ticker].Open + df[df.Ticker == ticker].Close) / 2
    l, = prc.plot(x, y, label=ticker, color=cmap(i))
    prc.fill_between(x,
                    y * .95, y * 1.05,
                    color=l.get_color(), alpha=.1)
    price_l.append(l)
prc.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

lines = np.array([volume_l, price_l]).T

handles, labels = prc.get_legend_handles_labels() # return lines and labels

# tooltip = plugins.PointHTMLTooltip(lines, labels=labels)
# plugins.connect(fig, tooltip)

interactive_legend = plugins.InteractiveLegendPlugin(lines,
                                                     labels,
                                                     alpha_unsel=0.1,
                                                     alpha_over=1.5,
                                                     start_visible=True)
plugins.connect(fig, interactive_legend)


prc.set_xlabel('Date')
prc.set_ylabel('Price')
fig.subplots_adjust(right=0.8)
prc.set_title('Price over time', size=20)

mpld3.show(
    fig,
    port=8080,
    open_browser=False,
    )