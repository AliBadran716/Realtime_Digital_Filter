from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUiType
import numpy as np
import pandas as pd
import os
import sys
from os import path
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from os import path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

class z_plane_plot():
    def __init__(self, widget):
        self.widget = widget
        self.zeros = {}
        self.poles = {}

        # Set up the z-plane plot
        self.setup_z_plane()

    def setup_z_plane(self):
        # Create a complex grid of points
        real_vals = np.linspace(-1, 1, 400)
        imag_vals = np.linspace(-1j, 1j, 400)
        real, imag = np.meshgrid(real_vals, imag_vals)
        z_plane = real + imag

        # Plot the infinite real and imaginary axes
        self.widget.plot([-np.inf, np.inf], [0, 0], pen='w')  # Real axis
        self.widget.plot([0, 0], [-np.inf, np.inf], pen='w')  # Imaginary axis

        # Create circle ROIs to show the unit circle and an additional circle of radius 2
        self.roi_unitCircle = pg.CircleROI([-1, -1], [2, 2], pen=pg.mkPen('r', width=2), movable=False, resizable=False,
                                           rotatable=False)

        # Set the origin point to the center of the widget
        self.plot_unitCircle.setYRange(-1.1, 1.1, padding=0)
        self.plot_unitCircle.setXRange(-1.1, 1.1, padding=0)
        self.plot_unitCircle.setMouseEnabled(x=False, y=False)

        self.plot_unitCircle.addItem(self.roi_unitCircle)
        self.roi_unitCircle.removeHandle(0)

        # Plot the z-plane surface
        surf = pg.PlotDataItem(z_plane.real, z_plane.imag, np.zeros_like(z_plane), symbol='o', size=5, pen=None)
        self.widget.addItem(surf)

        # Add a grid
        self.widget.showGrid(True, True, alpha=0.3)


