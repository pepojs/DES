# This Python file uses the following encoding: utf-8

# if__name__ == "__main__":
#     pass

from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as la
from math import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class MplWidget(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())


        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
        self.toolbar = NavigationToolbar2QT(self.canvas,self,coordinates=True)
        vertical_layout.addWidget(self.toolbar)

        img = plt.imread('map.png',0)

        print(self.points_for_ride([5,5],[20,20], 2, 5))

        self.canvas.axes.imshow(img)


    def draw_hospital_on_map(self,hospitals):
        for i in range(len(hospitals)):
            img = plt.imread('szpital1.png')
            imagebox= OffsetImage(img,zoom=0.02)
            ab = AnnotationBbox(imagebox,(hospitals[i].location[0],hospitals[i].location[1]))
            self.canvas.axes.add_artist(ab)
            self.canvas.axes.text(hospitals[i].location[0]-5,hospitals[i].location[1]+6,str(i+1),zorder=1000,fontSize=6, color='red')
        self.canvas.draw()

    def clean_hospital_on_map(self):
        import matplotlib
        for artist in self.canvas.axes.get_children():
            if isinstance(artist,AnnotationBbox) or (isinstance(artist,matplotlib.text.Text) and artist._remove_method):
                artist.remove()
        self.canvas.draw()

    def draw_accident_on_map(self,location):
        img = plt.imread('covid.png')
        imagebox= OffsetImage(img,zoom=0.05)
        ab = AnnotationBbox(imagebox,location)
        self.canvas.axes.add_artist(ab)
        self.canvas.draw()

    def remove_accident_from_map(self,location):
        count=0
        for picture in self.canvas.axes.get_children():
            if isinstance(picture,AnnotationBbox):
                if picture.xy == location and count == 0:
                    picture.remove()
                    count=1
        self.canvas.draw()

    def draw_car_on_map(self,location):
        img = plt.imread('karetka.png')
        imagebox= OffsetImage(img,zoom=0.02)
        ab = AnnotationBbox(imagebox,location)
        self.canvas.axes.add_artist(ab)
        self.canvas.draw()

    def remove_car_from_map(self,location):
        count=0
        for picture in self.canvas.axes.get_children():
            if isinstance(picture,AnnotationBbox):
                if picture.xy == location and count == 0:
                    picture.remove()
                    count=1
        self.canvas.draw()

    def ride_to_emergency(self,start_point, end_point, start_time, end_time):
        import time
        points = self.points_for_ride(start_point, end_point, start_time, end_time)
        points.insert(0,start_point)
        points.append(end_point)
        self.draw_car_on_map(points[0])
        for i in range(1, len(points)):
            self.remove_car_from_map(points[i-1])
            self.draw_car_on_map(points[i])
            time.sleep(1)
        self.remove_car_from_map(points[:-1])
        self.remove_accident_from_map(end_point)

    def points_for_ride(self, start_point, end_point, start_time, end_time):
#        print('start_point {}, end_point {}, start_time {}, end_time {}'.format(start_point, end_point, start_time, end_time))
        number_of_points = int(round(np.sqrt((start_point[0] - end_point[0])**2 + (start_point[1] - end_point[1])**2) / (end_time - start_time)))
#        print('number_of_points', number_of_points)
        x_spacing = (end_point[0] - start_point[0]) / (number_of_points + 1)
        y_spacing = (end_point[1] - start_point[1]) / (number_of_points + 1)

        return [(start_point[0] + i * x_spacing, start_point[1] +  i * y_spacing) for i in range(1, number_of_points+1)]



