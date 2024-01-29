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
        self.all_pass_filters = {}
        self.butterworthFilter = Filter(
            poles=[0.66045672 + 0.44332349j, 0.66045672 - 0.44332349j, 0.52429979 + 0.1457741j, 0.52429979 - 0.1457741j],
            zeros=[-1.00021915 + 0j, -0.99999998 + 0.00021913j, -0.99999998 - 0.00021913j, -0.99978088 + 0j],
            gain=0.004824343357716228
        )
        self.all_pass_filters.append({
            'name': 'Butterworth',
            'filter': self.butterworthFilter
        })

        self.chebyshev1Filter = Filter(
            poles=[0.78618897 + 0.53451727j, 0.78618897 - 0.53451727j, 0.84839427 + 0.2207097j, 0.84839427 - 0.2207097j],
            zeros=[-1.00021915 + 0j, -0.99999998 + 0.00021913j, -0.99999998 - 0.00021913j, -0.99978088 + 0j],
            gain=0.0010513933473130974
        )
        self.all_pass_filters.append({
            "name": "Chebyshev I Filter",
            "filter": self.chebyshev1Filter
        })

        self.chebyshev2Filter = Filter(
            poles=[0.81412081 + 0.34216671j, 0.81412081 - 0.34216671j, 0.62125795 + 0.15717069j, 0.62125795 - 0.15717069j],
            zeros=[0.16218512 + 0.98676035j, 0.16218512 - 0.98676035j, 0.77985627 + 0.62595862j, 0.77985627 - 0.62595862j],
            gain=0.0345589375728779
        )
        self.all_pass_filters.append({
            "name": "Chebyshev II Filter",
            "filter": self.chebyshev2Filter
        })

        self.ellipticFilter = Filter(
            poles=[0.79589405 + 0.56264606j, 0.79589405 - 0.56264606j, 0.80810983 + 0.29172164j, 0.80810983 - 0.29172164j],
            zeros=[0.2901308 + 0.956987j, 0.2901308 - 0.956987j, 0.73976805 + 0.67286197j, 0.73976805 - 0.67286197j],
            gain=0.041845590593020045
        )
        self.all_pass_filters.append({
            "name": "Elliptic Filter",
            "filter": self.ellipticFilter
        })
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
        self.delete_btn.clicked.connect(self.delete)
        self.move_btn.clicked.connect(self.move_marker)
        self.conjugate_check_box.stateChanged.connect(self.conjugate)
        self.apply_filter_btn.clicked.connect(self.apply_filter)


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

    def delete(self):
        to_be_deleted = self.selected_combo_box.currentText()
        self.zplane.delete_selected_marker(to_be_deleted)

    def move_marker(self):
        if self.move_btn.text() == "Move":
            self.move_btn.setText("Add")
            self.zplane.move_marker = True
        else:
            self.move_btn.setText("Move")
            self.zplane.move_marker = False

    def conjugate(self):
        self.zplane.conjugate = self.conjugate_check_box.isChecked()

    def apply_filter(self):
        zeros = self.zplane.get_zeros()
        poles = self.zplane.get_poles()
        self.filter = Filter(gain=0.5)
        self.filter.add_zero(zeros)
        self.filter.add_pole(poles)
        frequency, magnitude, phase = self.filter.get_response()
        print(frequency)
        print(magnitude)
        print(phase)
        self.plot_frequency_response(frequency, magnitude, phase)
        

def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == "__main__":
    main()
