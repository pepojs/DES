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
#        self.canvas.axes.set_ylim(self.canvas.axes.get_ylim()[::-1])
#        self.canvas.axes.invert_yaxis()
        self.toolbar = NavigationToolbar2QT(self.canvas,self,coordinates=True)
        vertical_layout.addWidget(self.toolbar)

        img = plt.imread('map.png',0)
#        print(img.transpose())
#        print(np.delete(img,3,1))
#        fig, ax = plt.subplots()

        print(self.points_for_ride([5,5],[20,20], 2, 5))

        self.canvas.axes.imshow(img)




#        self._figure = plt.figure("Example plot")
#        self._dragging_point = None
#        self._figure.canvas.mpl_connect('button_press_event', self._on_click)
#        self._figure.canvas.mpl_connect('button_release_event', self._on_release)
#        self._figure.canvas.mpl_connect('motion_notify_event', self._on_motion)

    def draw_hospital_on_map(self,hospitals):
        for i in range(len(hospitals)):
            img = plt.imread('szpital1.png')
            imagebox= OffsetImage(img,zoom=0.02)
            ab = AnnotationBbox(imagebox,(hospitals[i].location[0],hospitals[i].location[1]))
            self.canvas.axes.add_artist(ab)
            self.canvas.axes.text(hospitals[i].location[0]-5,hospitals[i].location[1]+6,str(i+1),zorder=1000,fontSize=6, color='red')
        self.canvas.draw()
#        for i in range(len(hospitals):
#            hospital_location = QWidget()
#            id_hospital = QLabel(i+1)
#            pic_hospital = QLabel()
#            pic_hospital.setPixmap(QPixmap("cat.jpg"))
#            vbox = QVBoxLayout()
#            vbox.addWidget(id_hospital)
#            vbox.addStretch()
#            vbox.addWidget(pic_hospital)
#            vbox.addStretch()
#            hospital_location.setLayout(vbox)
#            hospital_location.setGeometry(hospitals[i].location[0],hospitals[i].location[1],10,10)
#            self.canvas.axes.plot

    def clean_hospital_on_map(self):
        import matplotlib
        for artist in self.canvas.axes.get_children():
            if isinstance(artist,AnnotationBbox) or (isinstance(artist,matplotlib.text.Text) and artist._remove_method):
                artist.remove()
        self.canvas.draw()

    def draw_accident_on_map(self,location):
        img = plt.imread('crash.PNG',0)
        imagebox= OffsetImage(img,zoom=0.02)
        ab = AnnotationBbox(imagebox,location)
        self.canvas.axes.add_artist(ab)
        self.canvas.draw()

    def remove_accident_from_map(self,location):
        for picture in self.canvas.axes.get_children():
            if isinstance(picture,AnnotationBbox):
                if picture.xy == location:
                    picture.remove()
        self.canvas.draw()

    def draw_car_on_map(self,location):
        img = plt.imread('karetka.png')
        imagebox= OffsetImage(img,zoom=0.02)
        ab = AnnotationBbox(imagebox,location)
        self.canvas.axes.add_artist(ab)
        self.canvas.draw()

    def remove_car_from_map(self,location):
        for picture in self.canvas.axes.get_children():
            if isinstance(picture,AnnotationBbox):
                if picture.xy == location:
                    picture.remove()
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
        print('start_point {}, end_point {}, start_time {}, end_time {}'.format(start_point, end_point, start_time, end_time))
        number_of_points = int(round(np.sqrt((start_point[0] - end_point[0])**2 + (start_point[1] - end_point[1])**2) / (end_time - start_time)))
        print('number_of_points', number_of_points)
        x_spacing = (end_point[0] - start_point[0]) / (number_of_points + 1)
        y_spacing = (end_point[1] - start_point[1]) / (number_of_points + 1)

        return [(start_point[0] + i * x_spacing, start_point[1] +  i * y_spacing) for i in range(1, number_of_points+1)]


    def draw_function(self,points,x1min,x1max,x2min,x2max,delta=0.025):
        import function

        self.canvas.figure.clf()
        self.canvas.draw()
        self.canvas.axes=self.canvas.figure.add_subplot(111)
        #Wyznaczanie zakresow dla poszczegolnych osi
        if x1max<=x1min:
            x1min = np.min(points)-0.5
            x1max = np.max(points)+0.5
        if x2max<=x2min:
            x2min = np.min(points)-0.5
            x2max = np.max(points)+0.5

        #Definicja osi w zakresie (min;max) z krokiem delta
        x1 = np.arange(x1min,x1max,delta)
        x2 = np.arange(x2min,x2max,delta)
        X1,X2 = np.meshgrid(x1,x2)
        Y = X1**2

        for i in range(len(x1)):
            for j in range(len(x2)):
                x = np.array([x1[i],x2[j]],dtype=float)
                Y[j][i] = function.f(x)

        levels = []
        x_point = []
        y_point = []
        for point in points:
            levels.append(function.f(point))
            x_point.append(point[0])
            y_point.append(point[1])

        levels.sort()


        #poziomice
        CS = self.canvas.axes.contour(X1,X2,Y,levels,colors='k')

        #kolorki, kolorki
        self.canvas.axes.imshow(Y, cmap=cm.jet,
               origin='lower', extent=[x1min, x1max, x2min, x2max])

        #Kolejne punkty znalezione przez algorytm
        self.canvas.axes.plot(x_point,y_point,"or--",color='red',linewidth=2)
#        self.ui.graphWidget.plot(x_point,y_point)

        #opis
        self.canvas.axes.grid(True)
        self.canvas.axes.set_title('Metoda najszybszego spadku')
        self.canvas.axes.set_xlabel('x1')
        self.canvas.axes.set_ylabel('x2')

#        self.ui.graphWidget.setLabel('bottom', 'x1')
#        self.ui.graphWidget.setLabel('left', 'x2')


        self.canvas.draw()

    def clear(self):
        self.canvas.figure.clf()
        self.canvas.draw()

    def _update_plot(self):
        if not self._points:
            self._line.set_data([], [])
        else:
            x, y = zip(*sorted(self._points.items()))
            # Add new plot
            if not self._line:
                self._line, = self._axes.plot(x, y, "b", marker="o", markersize=10)
            # Update current plot
            else:
                self._line.set_data(x, y)
        self._figure.canvas.draw()

    def _add_point(self, x, y=None):
        if isinstance(x, MouseEvent):
            x, y = int(x.xdata), int(x.ydata)
        self._points[x] = y
        return x, y

    def _remove_point(self, x, _):
        if x in self._points:
            self._points.pop(x)

    def _find_neighbor_point(self, event):
        u""" Find point around mouse position
        :rtype: ((int, int)|None)
        :return: (x, y) if there are any point around mouse else None
        """
        distance_threshold = 3.0
        nearest_point = None
        min_distance = math.sqrt(2 * (100 ** 2))
        for x, y in self._points.items():
            distance = math.hypot(event.xdata - x, event.ydata - y)
            if distance < min_distance:
                min_distance = distance
                nearest_point = (x, y)
        if min_distance < distance_threshold:
            return nearest_point
        return None

    def _on_click(self, event):
        u""" callback method for mouse click event
        :type event: MouseEvent
        """
        # left click
        if event.button == 1 and event.inaxes in [self._axes]:
            point = self._find_neighbor_point(event)
            if point:
                self._dragging_point = point
            else:
                self._add_point(event)
            self._update_plot()
        # right click
        elif event.button == 3 and event.inaxes in [self._axes]:
            point = self._find_neighbor_point(event)
            if point:
                self._remove_point(*point)
                self._update_plot()

    def _on_release(self, event):
        u""" callback method for mouse release event
        :type event: MouseEvent
        """
        if event.button == 1 and event.inaxes in [self._axes] and self._dragging_point:
            self._dragging_point = None
            self._update_plot()

    def _on_motion(self, event):
        u""" callback method for mouse motion event
        :type event: MouseEvent
        """
        if not self._dragging_point:
            return
        if event.xdata is None or event.ydata is None:
            return
        self._remove_point(*self._dragging_point)
        self._dragging_point = self._add_point(event)
        self._update_plot()


