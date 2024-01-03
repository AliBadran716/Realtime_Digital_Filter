from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUiType
import pyqtgraph as pg
import numpy as np
import pandas as pd
import os
import sys
from os import path
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import numpy as np
from os import path
from scipy import signal
from filter import Filter
from z_plane import z_plane_plot

FORM_CLASS, _ = loadUiType(
    path.join(path.dirname(__file__), "main.ui")
)  # connects the Ui file with the Python file


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.handle_buttons()
        self.zeros = []  # list of tuples (real, imaginary)
        self.poles = []
        self.gain = 1
        self.is_zeros = True
        self.handle_graphs()
        self.handle_graphs()
        self.last_pos = None
        self.time = np.arange(0, 1, 0.1)
        self.frequency = 0
        self.widget.mouseMoveEvent = self.widget_mouseMoveEvent
        self.signal_list = []
        self.zplane = z_plane_plot(self.z_plane_plot)
        # self.filter = Filter()
        # self.filter.set_filter_components([1j, 1], [-0.5 - 0.5j], 1)
        # frequency, magnitude, phase = self.filter.get_frequency_response()
        # self.plot_frequency_response(frequency, magnitude, phase)

    def handle_graphs(self):
        self.magnitude_plot.plotItem.setTitle("Magnitude Response")
        self.magnitude_plot.plotItem.setLabel('left', 'Magnitude (dB)')
        self.magnitude_plot.plotItem.setLabel('bottom', 'Frequency (rad/sample)')
        self.phase_plot.plotItem.setTitle("Phase Response")
        self.phase_plot.plotItem.setLabel('left', 'Phase (radians)')
        self.phase_plot.plotItem.setLabel('bottom', 'Frequency (rad/sample)')




    def plot_frequency_response(self, frequency, magnitude, phase):
        # Plot magnitude response
        self.magnitude_plot.plot(frequency, magnitude, pen='b', clear=True)
        # Set labels and title
        self.magnitude_plot.setLabel('left', 'Magnitude (dB)')
        self.magnitude_plot.setLabel('bottom', 'Frequency')
        self.magnitude_plot.setTitle('Frequency Response - Magnitude')

        # Plot phase response
        self.phase_plot.plot(frequency, phase, pen='r', clear=True)
        # Set labels and title
        self.phase_plot.setLabel('left', 'Phase (radians)')
        self.phase_plot.setLabel('bottom', 'Frequency')
        self.phase_plot.setTitle('Frequency Response - Phase')


    def handle_buttons(self):
        pass

    def widget_mouseMoveEvent(self, event):
        # print(event.pos())
        if self.last_pos:
            # Calculate mouse speed
            delta_x = event.x() - self.last_pos.x()
            delta_y = event.y() - self.last_pos.y()
            speed = (delta_x**2 + delta_y**2)**0.5

            # Update frequency based on speed
            self.frequency = int(speed)  # Adjust this factor to control the sensitivity

            # Display mouse information
            # print(f"Mouse Speed: {speed:.2f} | Frequency: {self.frequency}")

            # Generate arbitrary signal based on frequency
            signal = self.generate_arbitrary_signal(self.time, self.frequency,event.x())
            self.signal_list = self.signal_list + list(signal)
            self.graphicsView_2.clear()
            self.graphicsView_2.plot(self.signal_list)

            # Do something with the generated signal if needed

        self.last_pos = event.pos()


    def generate_arbitrary_signal(self, time, frequency,mag):

        return mag*(np.sin(2 * np.pi * frequency * time) + np.sin(2 * np.pi * 2 * frequency * time)) / 2


def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == "__main__":
    main()
