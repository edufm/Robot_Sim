# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:44:56 2020

@author: edufe
"""

import numpy as np

from matplotlib.widgets import Slider, Button

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from .cordinates import trace

axcolor = 'lightgoldenrodyellow'

class animate():
    def __init__(self, dvhb):
        
        self.dvhb = dvhb
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.plot_line, = self.ax.plot(*self.get_points(), lw=2)
        self.plot_dot, = self.ax.plot(*self.get_points(), "bo")
        
        plt.subplots_adjust(left=0.25, bottom=0.32)
        plt.xlabel("X")
        plt.ylabel("Y")
        
        self.limits = self.get_limits()
        self.ax.set_xlim(*self.limits)
        self.ax.set_ylim(*self.limits)
        self.ax.set_zlim(*self.limits)
        
        self.variables = []
        for n, variable in enumerate(self.dvhb.joints):
            joint_slider_loc= plt.axes([0.25, 0.20-0.05*n, 0.65, 0.03], facecolor=axcolor)
            
            if variable[1] == "r":
                joint = Slider(joint_slider_loc, f'Joint {variable[0]}', 0, 360, 
                               valinit=self.dvhb.get_curr_theta(variable[0]))
                
            elif variable[1] == "t":
                joint = Slider(joint_slider_loc, f'Joint {variable[0]}', 0, 5, 
                               valinit=self.dvhb.get_curr_d(variable[0]))
                
            joint.on_changed(self.update)
            self.variables.append(joint)
        
        resetax = plt.axes([0.1, 0.4, 0.1, 0.04])
        self.button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
        self.button.on_clicked(self.reset)
        
    def get_limits(self):
        
        # Verifica quais são todos os pontos de dados
        all_points = []
        for cordsys in trace(self.dvhb.to_cordsys()):
            
            if isinstance(cordsys, np.ndarray):
                matrix = cordsys
            else:
                matrix = cordsys.matrix
                
            all_points.append(matrix[:3, 3])

        all_points = np.array(all_points)
        maxs, mins = all_points.max(axis=0), all_points.min(axis=0)
        abs_max, abs_min = max(maxs), min(mins)
        vec_scale = 0.1*abs_max
        space = 2*vec_scale

        return [abs_min-space, abs_max+space]
    
    
    def get_points(self):
        
        # Verifica quais são todos os pontos de dados
        all_points = []
        for cordsys in trace(self.dvhb.to_cordsys()):
            
            if isinstance(cordsys, np.ndarray):
                matrix = cordsys
            else:
                matrix = cordsys.matrix
                
            all_points.append(matrix[:3, 3])

        all_points = np.array(all_points)
        
        # Liga os pontos com uma linha
        return [all_points[:, 0], all_points[:, 1], all_points[:, 2]]
    
    def update(self, val):
    
        
        for n, variable in enumerate(self.variables):
            if self.dvhb.joints[n][1] == "r":
                self.dvhb.rotate_theta(self.dvhb.joints[n][0], variable.val)
            elif self.dvhb.joints[n][1] == "t":
                self.dvhb.extend_d(self.dvhb.joints[n][0], variable.val)
                        
        x, y, z = self.get_points() 
        
        self.ax.cla()
        
        self.plot_line, = self.ax.plot(x, y, z, lw=2)
        self.plot_dot, = self.ax.plot(x, y, z, "bo")
        
        self.ax.set_xlim(*self.limits)
        self.ax.set_ylim(*self.limits)
        self.ax.set_zlim(*self.limits)
        
        self.fig.canvas.draw()
    
    
    def reset(self, event):
        for variable in self.variables:
            variable.reset()
    