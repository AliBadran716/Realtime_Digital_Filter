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
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

class z_plane_plot():
    def __init__(self, widget):
        """Initialize the z-plane plot."""
        self.widget = widget
        self.zeros = []  # List of zero markers
        self.poles = []  # List of pole markers
        self.selected_marker = None
        self.selected_conjugated = None
        self.move_marker = False
        self.conjugate = False
        self.conjugate_pair = []

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
        """Handle mouse click events."""
        # Get the coordinates of the click
        x = self.widget.plotItem.vb.mapSceneToView(event.scenePos()).x()
        y = self.widget.plotItem.vb.mapSceneToView(event.scenePos()).y()

        # Unhighlight the previously selected marker
        self.unhighlight_marker()

        # Check if the click is close to any existing zero or pole
        for position, markers in {'zeros': self.zeros, 'poles': self.poles}.items():
            for index, (marker, coords) in enumerate(markers):
                if np.abs(x - coords[0]) < 0.15 and np.abs(y - coords[1]) < 0.15:
                    # Click is close to an existing marker, select it and highlight it with a blue border
                    self.selected_marker = (position, index, marker)
                    self.highlight_marker(marker)
                    return

        # move at the middle mouse button click
        if event.button() != 1 and event.button() != 2:
            index_conjugated = self.conjugate_marker()
            # Move the selected marker to the new location
            position, index, marker = self.selected_marker
            if position == 'zeros':
                self.zeros[index] = (marker, (x, y))
            elif position == 'poles':
                self.poles[index] = (marker, (x, y))
            # Update the marker's position and plot
            marker.setData(pos=np.array([[x, y]]))
            self.highlight_marker(marker)
            # Move conjugate if exists
            if self.selected_conjugated is not None:
                position, index, marker = self.selected_conjugated
                if position == 'zeros':
                    self.zeros[index] = (marker, (x, -y))
                elif position == 'poles':
                    self.poles[index] = (marker, (x, -y))
                # Update the marker's position and plot
                marker.setData(pos=np.array([[x, -y]]))
                self.highlight_marker(marker)
                self.conjugate_pair[index_conjugated] = [marker, (x, -y)]
            return

        # Add a new marker based on left or right mouse button press
        if event.button() == 1:  # Left button for zeros
            marker = pg.ScatterPlotItem(pos=np.array([[x, y]]), symbol='o', pen='w')
            self.widget.addItem(marker)
            index = len(self.zeros)
            self.zeros.append((marker, (x, y)))
            self.selected_marker = ('zeros', index, marker)
            self.highlight_marker(marker)
            if self.conjugate:
                marker = pg.ScatterPlotItem(pos=np.array([[x, -y]]), symbol='o', pen='w')
                self.widget.addItem(marker)
                self.zeros.append((marker, (x, -y)))
                self.conjugate_pair.append([marker, (x, -y)])

        elif event.button() == 2:  # Right button for poles
            marker = pg.ScatterPlotItem(pos=np.array([[x, y]]), symbol='x', pen='w')
            self.widget.addItem(marker)
            index = len(self.poles)
            self.poles.append((marker, (x, y)))
            self.selected_marker = ('poles', index, marker)
            self.highlight_marker(marker)
            if self.conjugate:
                marker = pg.ScatterPlotItem(pos=np.array([[x, -y]]), symbol='x', pen='w')
                self.widget.addItem(marker)
                self.poles.append((marker, (x, -y)))
                self.conjugate_pair.append([marker, (x, -y)])

    # Find the conjugate of the selected marker
    def conjugate_marker(self):
        if self.conjugate:
            position, index, marker = self.selected_marker
            conjugate_not_found = True
            index_conjugated = None
            if position == 'zeros':
                x = self.zeros[index][1][0]
                y = self.zeros[index][1][1]
                for i in range(len(self.conjugate_pair)):
                    if self.conjugate_pair[i][1][0] == x and self.conjugate_pair[i][1][1] == -y:
                        self.selected_conjugated = ('zeros', i, self.conjugate_pair[i][0])
                        conjugate_not_found = False
                        index_conjugated = i
            elif position == 'poles':
                x = self.poles[index][1][0]
                y = self.poles[index][1][1]
                for i in range(len(self.conjugate_pair)):
                    if self.conjugate_pair[i][1][0] == x and self.conjugate_pair[i][1][1] == -y:
                        self.selected_conjugated = ('poles', i, self.conjugate_pair[i][0])
                        conjugate_not_found = False
                        index_conjugated = i

            if conjugate_not_found:
                self.selected_conjugated = None
            else:
                self.highlight_marker(self.selected_conjugated[2])
                return index_conjugated

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
            index_conjugated = self.conjugate_marker()
            position, index, marker = self.selected_marker
            if position == 'zeros':
                self.delete_marker('zeros', index)
            elif position == 'poles':
                self.delete_marker('poles', index)
            self.selected_marker = None
            if self.selected_conjugated is not None:
                position, index, marker = self.selected_conjugated
                if position == 'zeros':
                    self.delete_marker('zeros', index)
                elif position == 'poles':
                    self.delete_marker('poles', index)
                self.selected_conjugated = None
        elif to_be_deleted == "All zeros":
            self.delete_all_markers('zeros')
        elif to_be_deleted == "All poles":
            self.delete_all_markers('poles')
        elif to_be_deleted == "Both":
            self.delete_all_markers('zeros')
            self.delete_all_markers('poles')

    def delete_marker(self, position, index):
        """Delete a single marker."""
        markers_list = self.zeros if position == 'zeros' else self.poles
        if 0 <= index < len(markers_list):
            marker, _ = markers_list.pop(index)
            self.widget.removeItem(marker)

    def delete_all_markers(self, position):
        """Delete all markers of a given type."""
        markers_list = self.zeros if position == 'zeros' else self.poles
        for marker, _ in markers_list:
            self.widget.removeItem(marker)
        markers_list.clear()
        self.selected_marker = None

    def get_zeros(self):
        """Return the list of zeros."""
        complex_zeros = [complex(x, y) for _, (x, y) in self.zeros]
        return complex_zeros

    def get_poles(self):
        """Return the list of poles."""
        complex_poles = [complex(x, y) for _, (x, y) in self.poles]
        return complex_poles
     






        
        
        
        
        
    