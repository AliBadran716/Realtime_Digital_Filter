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
        self.set_scene()

    def set_scene(self):
        self.scene = QGraphicsScene(self)
        self.z_plane_plot.setScene(self.scene)
        unit_circle = QGraphicsEllipseItem(-50, -50, 100, 100)
        self.scene.addItem(unit_circle)

        # Increase the scene size
        self.scene.setSceneRect(-100, -100, 200, 200)
        # Set up the view
        self.mousePressEvent = self.mousePressEvent
        # self.verticalLayout.addWidget(self.z_plane_plot_1)

    def handle_buttons(self):
        pass

    def handle_graphs(self):
        pass

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        # Get the mouse click position
        pos = self.z_plane_plot.mapToScene(event.pos())
        # Draw a point at the clicked position
        point = QGraphicsEllipseItem(pos.x() - 325, pos.y() - 50, 5, 5)
        self.scene.addItem(point)
        # Print the coordinates of the clicked point
        print(f"Clicked at: ({pos.x()}, {pos.y()})")


def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == "__main__":
    main()
