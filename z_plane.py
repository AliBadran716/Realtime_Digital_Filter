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
        self.selected_marker = None
        self.move_marker = False
        self.conjugate = False

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
        # Get the coordinates of the click
        x = self.widget.plotItem.vb.mapSceneToView(event.scenePos()).x()
        y = self.widget.plotItem.vb.mapSceneToView(event.scenePos()).y()
        print('x: ', x, 'y: ', y)

        # Unhighlight the previously selected marker
        self.unhighlight_marker()

        # Check if the click is close to any existing zero or pole
        for position, markers in {'zeros': self.zeros, 'poles': self.poles}.items():
            for index, (marker, coords) in markers.items():
                if np.abs(x - coords[0]) < 0.15 and np.abs(y - coords[1]) < 0.15:
                    # Click is close to an existing marker, select it and highlight it with a blue border
                    self.selected_marker = (position, index, marker)
                    self.highlight_marker(marker)
                    return

        if self.move_marker:
            # Move the selected marker to the new location
            position, index, marker = self.selected_marker
            if position == 'zeros':
                self.zeros[index] = (marker, (x, y))
            elif position == 'poles':
                self.poles[index] = (marker, (x, y))
            # Update the marker's position and plot
            marker.setData(pos=np.array([[x, y]]))
            self.highlight_marker(marker)
            return

        # Add a new marker based on left or right mouse button press
        if event.button() == 1:  # Left button for zeros
            marker = pg.ScatterPlotItem(pos=np.array([[x, y]]), symbol='o', pen='w')
            self.widget.addItem(marker)
            index = len(self.zeros) + 1
            self.zeros[index] = (marker, (x, y))
            self.selected_marker = ('zeros', index, marker)
            self.highlight_marker(marker)
            if self.conjugate:
                marker = pg.ScatterPlotItem(pos=np.array([[x, -y]]), symbol='o', pen='w')
                self.widget.addItem(marker)
                index = len(self.zeros) + 1
                self.zeros[index] = (marker, (x, -y))

        elif event.button() == 2:  # Right button for poles
            marker = pg.ScatterPlotItem(pos=np.array([[x, y]]), symbol='x', pen='w')
            self.widget.addItem(marker)
            index = len(self.poles) + 1
            self.poles[index] = (marker, (x, y))
            self.selected_marker = ('poles', index, marker)
            self.highlight_marker(marker)
            if self.conjugate:
                marker = pg.ScatterPlotItem(pos=np.array([[x, -y]]), symbol='x', pen='w')
                self.widget.addItem(marker)
                index = len(self.poles) + 1
                self.poles[index] = (marker, (x, -y))
    def highlight_marker(self, marker):
        """Highlight the selected marker with a blue border."""
        if self.selected_marker is not None:
            position, index, marker = self.selected_marker
            if position == 'zeros':
                self.zeros[index][0].setPen(pg.mkPen('b', width=2))
            elif position == 'poles':
                self.poles[index][0].setPen(pg.mkPen('b', width=2))

    def unhighlight_marker(self):
        """Unhighlight the previously selected marker."""
        if self.selected_marker is not None:
            position, index, marker = self.selected_marker
            if position == 'zeros':
                self.zeros[index][0].setPen(pg.mkPen('w'))
            elif position == 'poles':
                self.poles[index][0].setPen(pg.mkPen('w'))

    def delete_selected_marker(self, to_be_deleted):
        """Delete the selected markers."""
        if to_be_deleted == "Selected" and self.selected_marker is not None:
            position, index, marker = self.selected_marker
            if position == 'zeros':
                self.delete_marker('zeros', index)
            elif position == 'poles':
                self.delete_marker('poles', index)
            self.selected_marker = None
        elif to_be_deleted == "All zeros":
            self.delete_all_markers('zeros')
        elif to_be_deleted == "All poles":
            self.delete_all_markers('poles')
        elif to_be_deleted == "Both":
            self.delete_all_markers('zeros')
            self.delete_all_markers('poles')

    def delete_marker(self, position, index):
        """Delete a single marker."""
        if position == 'zeros' and index in self.zeros:
            self.widget.removeItem(self.zeros[index][0])
            del self.zeros[index]
        elif position == 'poles' and index in self.poles:
            self.widget.removeItem(self.poles[index][0])
            del self.poles[index]

    def delete_all_markers(self, position):
        """Delete all markers of a given type."""
        markers_dict = self.zeros if position == 'zeros' else self.poles
        for index in markers_dict.copy():
            self.widget.removeItem(markers_dict[index][0])
            del markers_dict[index]
        self.selected_marker = None