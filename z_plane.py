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

        # Connect mouse press event to the function
        self.widget.scene().sigMouseClicked.connect(self.mouse_clicked)

    def setup_z_plane(self):
        """Set up the z-plane plot."""
        # Create the z-plane plot
        self.widget.setBackground('black')
        self.widget.setLabel('left', 'Imaginary')
        self.widget.setLabel('bottom', 'Real')
        self.widget.setXRange(-1.5, 1.5, padding=0)
        self.widget.setYRange(-1.5, 1.5, padding=0)
        self.widget.showGrid(True, True, 0.5)
        self.widget.setMouseEnabled(x=False, y=False)
        self.widget.setMenuEnabled(False)
        self.widget.setMouseEnabled(x=False, y=False)
        self.widget.hideButtons()
        # Add Title
        self.widget.setTitle("Z-Plane Plot", color="w", size="12pt")
        # Plot real and imaginary axes
        self.widget.plot([0, 0], [-1, 1], pen=pg.mkPen('w'))  # Real axis
        self.widget.plot([-1, 1], [0, 0], pen=pg.mkPen('w'))  # Imaginary axis

        # Plot the unit circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        self.widget.plot(x, y, pen=pg.mkPen('r'))

        # Set axis labels
        self.widget.setLabel('left', "Imaginary")
        self.widget.setLabel('bottom', "Real")

        # Add a grid
        self.widget.showGrid(x=True, y=True)

    def mouse_clicked(self, event):
        # Get the coordinates of the mouse click in the z-plane
        pos = self.widget.mapToView(event.pos())
        x, y = pos.x(), pos.y()
        print('x: ', x, 'y: ', y)
        


        # Check if the click is inside the unit circle
        if x ** 2 + y ** 2 <= 1:
            # Check if the click is close to any existing zero or pole
            for position, markers in {'zeros': self.zeros, 'poles': self.poles}.items():
                for marker, coords in markers.items():
                    if np.abs(x - coords[0]) < 0.1 and np.abs(y - coords[1]) < 0.1:
                        # Click is close to an existing marker, do nothing
                        return

            # Add a new marker based on left or right mouse button press
            if event.button() == 1:  # Left button for zeros
                marker = pg.ScatterPlotItem(pos=np.array([[x, y]]), symbol='o', pen='w')
                self.widget.addItem(marker)
                self.zeros[len(self.zeros) + 1] = (x, y)
            elif event.button() == 2:  # Right button for poles
                marker = pg.ScatterPlotItem(pos=np.array([[x, y]]), symbol='x', pen='w')
                self.widget.addItem(marker)
                self.poles[len(self.poles) + 1] = (x, y)