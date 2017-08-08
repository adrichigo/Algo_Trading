import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick2_ochl
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
import urllib.request as urllib2
import my_utilities
import matplotlib

matplotlib.rcParams.update({'font.size':9})

class quote_plot:
    my_quote = ""
    dates   = []
    opens   = []
    closes  = []
    highs   = []
    lows    = []
    volumes = []

    def get_quote_data(self, startTime):
        # getting the data from google finance
        response = urllib2.urlopen(my_utilities.construct_Quote_Request(self.my_quote,startTime))
        if response == 0:
            raise SystemExit
        quote = pd.read_csv(response)
        final_quote = quote[::-1]

        ##################################################
        #                Data of the quote               #
        ##################################################
        self.dates       = final_quote["Date"]
        self.opens       = final_quote["Open"]
        self.closes      = final_quote["Close"]
        self.highs       = final_quote["High"]
        self.lows        = final_quote["Low"]
        self.volumes     = final_quote["Volume"]

    # Declare and register callbacks to get x_min and x_max
    # When the plot is zoomed in or zoomed out
    def on_ylims_change(self, axe):
        labels = [item.get_text() for item in axe.get_xticklabels()]
        ticks = [item for item in axe.get_xticks()]
        for x in range(len(labels)):
            if ticks[x] >= 0 and ticks[x] <= len(self.dates):
                labels[x] = self.dates[len(self.dates)-1-int(ticks[x])]
            else:
                labels[x] = ""
        axe.set_xticklabels(labels)

    def display_quote(self):
        N = len(self.dates)
        ###################################################
        # Calculating the color for the volume (Bar plot) #
        ###################################################
        colorbar = self.closes >= self.opens
        my_colorbar = colorbar.replace((False, True), ("r", "g"))

        ##################################################
        #                 Candelstick Plot               #
        ##################################################
        fig = plt.figure()

        # Stock Price
        ax = plt.subplot2grid((6,5), (0,0), rowspan=5, colspan=5)
        ax.set_ylabel('Stock Price')
        ax.grid(True)
        ax.callbacks.connect('ylim_changed', self.on_ylims_change)

        # Volume
        ax_1 = plt.subplot2grid((6,5), (5,0), sharex=ax, rowspan=1, colspan=5)
        ax_1.bar(np.arange(N), self.volumes, color=my_colorbar)
        ax_1.set_xlim(0, N)
        ax_1.yaxis.set_ticklabels([])
        ax_1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax_1.grid(True)
        ax_1.set_ylabel('Volume')

        # Figure properties
        plt.subplots_adjust(bottom=0.08, top=0.95, right=0.97, left=0.10, hspace=0.0)
        plt.suptitle(self.my_quote + ' Stock Price')
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(plt.gca().get_xticklabels(), rotation=18, horizontalalignment='right')

        # Display the candelstick plot for the chosen quote
        candlestick2_ochl(ax, self.opens, self.closes, self.highs, self.lows, width=0.85, colorup='g', alpha =.55)
        plt.show()

my_plot = quote_plot()
my_plot.my_quote = "GOOGL"
my_plot.get_quote_data("jan-01-2016")
my_plot.display_quote()
