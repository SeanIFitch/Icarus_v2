from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from time import time


class SwitchTimePlot(pg.PlotWidget):
    # Dictionary of color to plot each channel
    CHANNEL_COLORS = {
        'target': '#FFDC00',        # yellow
        'depre_low': '#FF5252',     # salmon
        'depre_up': '#B9121B',      # red
        'pre_low': '#289976',       # cyan
        'pre_up': '#004B8D',        # dark blue
        'hi_pre_orig': '#732DD9',   # purple
        'hi_pre_sample': '#AB47BC', # magenta
        'pump': '#45BF55',          # light green
        'depre_valve': '#FD7400',   # orange
        'pre_valve': '#59D8E6',     # light blue
        'log': '#374140'            # gray
    }

    def __init__(self, parent=None, background='default', plotItem=None, **kargs):
        super().__init__(parent, background, plotItem, **kargs)

        self.setup_plot()
        self.setup_lines()


    def setup_plot(self):
        window_color = self.palette().color(QPalette.Window)
        text_color = self.palette().color(QPalette.WindowText)
        self.setBackground(window_color)
        self.setTitle("Switch Time", color=text_color, size="14pt")
        self.showGrid(x=True, y=True)
        self.setYRange(-3, 6, padding=0)
        self.setMouseEnabled(x=False, y=False) # Prevent zooming
        self.hideButtons() # Remove autoScale button

        # Axis Labels
        styles = {'color': text_color}
        self.setLabel('left', 'Time (ms)', **styles)
        self.setLabel('bottom', f'Time (s)', **styles)


    def setup_lines(self):
        self.display_channels = ['hi_pre_orig', 'hi_pre_sample']
        dummy_x = [0, 10]
        dummy_y = [0, 0]
        self.pressurize_x = []
        self.depressurize_x = []
        self.pressurize_y = {channel: [] for channel in self.display_channels}
        self.depressurize_y = {channel: [] for channel in self.display_channels}
        self.initial_time = None
        self.pressurize_line_references = {}
        self.depressurize_line_references = {}

        # Create a dictionary of lines for each channel listed in display_channels
        for channel in self.display_channels:
            color = self.CHANNEL_COLORS[channel]
            self.pressurize_line_references[channel] = self.plot_line(dummy_x, dummy_y, color)
            self.depressurize_line_references[channel] = self.plot_line(dummy_x, dummy_y, color)


    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate


    def update_pressurize_data(self, data):
        # Find switch times.
        # This is time between the event and the minimum of x + y.
        # We transform such that the range of x is 5 times the range of y.
        event_index = np.argmin(data['pre_valve'])
        for channel, y in self.pressurize_y.items():
            y_min = min(data[channel][event_index:])
            y_max = max(data[channel][event_index:])
            x_range = len(data[channel][event_index:])
            y_range = y_max - y_min
            transformed = (data[channel][event_index:] - y_min) * x_range / (y_range * 5)

            max_index = np.argmin(transformed + np.arange(0, x_range))
            sample_rate_khz = self.sample_rate / 1000
            switch_time = max_index / sample_rate_khz
            y.append(switch_time)

        # Add current time to x values
        if self.initial_time is None:
            self.initial_time = time()
        time_since_start = time() - self.initial_time
        self.pressurize_x.append(time_since_start)

        # update data for each line
        for channel, line_reference in self.pressurize_line_references.items():
            line_reference.setData(self.pressurize_x, np.asarray(self.pressurize_y[channel]))


    def update_depressurize_data(self, data):
        # Find switch times.
        # This is time between the event and the minimum of x + y.
        # We transform such that the range of x is 5 times the range of y.
        event_index = np.argmin(data['depre_valve'])
        for channel, y in self.depressurize_y.items():
            y_min = min(data[channel][event_index:])
            y_max = max(data[channel][event_index:])
            x_range = len(data[channel][event_index:])
            y_range = y_max - y_min
            transformed = (data[channel][event_index:] - y_min) * x_range / (y_range * 5)

            max_index = np.argmax(transformed + np.arange(0, x_range))
            sample_rate_khz = self.sample_rate / 1000
            switch_time = max_index / sample_rate_khz
            y.append(switch_time / 130)

        # Add current time to x values
        if self.initial_time is None:
            self.initial_time = time()
        time_since_start = time() - self.initial_time
        self.depressurize_x.append(time_since_start)

        # update data for each line
        for channel, line_reference in self.depressurize_line_references.items():
            line_reference.setData(self.depressurize_x, np.asarray(self.depressurize_y[channel]))


    def plot_line(self, x, y, color, style=Qt.SolidLine):
        pen = pg.mkPen(color=color, style=style)
        return self.plot(x, y, pen=pen)


    def reset_lines(self):
        dummy_x = [0, 10]
        dummy_y = [0, 0]
        self.pressurize_x = []
        self.depressurize_x = []
        self.pressurize_y = {channel: [] for channel in self.display_channels}
        self.depressurize_y = {channel: [] for channel in self.display_channels}
        self.initial_time = None

        for channel in self.display_channels:
            color = self.CHANNEL_COLORS[channel]
            self.pressurize_line_references[channel].setData(dummy_x, dummy_y, color)
            self.depressurize_line_references[channel].setData(dummy_x, dummy_y, color)