# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:44:56 2020

@author: edufe
"""

from copy import deepcopy

import numpy as np

from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from .cordinates import trace

axcolor = 'lightgoldenrodyellow'

class simulate():
    def __init__(self, dvhb):
        
        from IPython import get_ipython
        ipy = get_ipython()
        if ipy != None:
            ipy.run_line_magic('matplotlib', 'auto')

        
        self.dvhb = deepcopy(dvhb)
        self.limits = self.get_limits()
        self.scale = self.limits[1]*0.1
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        plt.subplots_adjust(left=0.25, bottom=0.40, top=1)
        
        self.variables = []
        for n, variable in enumerate(self.dvhb.joints):
            joint_slider_loc= plt.axes([0.25, 0.30-0.05*n, 0.65, 0.03], facecolor=axcolor)
            
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
        
        self.update(None, init=True)
        
        plt.show()
        
        
    def get_limits(self):
        
        # Verifica quais são todos os pontos de dados
        all_points = []
        for cordsys in trace(self.dvhb.to_cordsys()):
            all_points.append(cordsys[:3, 3])

        all_points = np.array(all_points)
        maxs, mins = all_points.max(axis=0), all_points.min(axis=0)
        abs_max = max(max(abs(maxs)), min(abs(mins)))
        vec_scale = 0.1*abs_max
        space = 2*vec_scale

        return [-abs_max-space, abs_max+space]
    
    
    def get_points(self):
        
        # Verifica quais são todos os pontos de dados
        all_points = []
        for cordsys in trace(self.dvhb.to_cordsys()):
            all_points.append(cordsys[:3, 3])

        all_points = np.array(all_points)
        
        # Liga os pontos com uma linha
        return [all_points[:, 0], all_points[:, 1], all_points[:, 2]]
    
    
    def update(self, val, init=False):
        
        if not init:    
            new_pos = [variable.val for variable in self.variables]
            self.dvhb.recalculate_joints(new_pos)
                            
        x, y, z = self.get_points() 
        
        self.ax.cla()
        
        # For the body of the robot
        self.ax.plot(x, y, z, lw=2)
        self.ax.plot(x[1:], y[1:], z[1:], "bo")
        
        # For the origin marker
        self.ax.plot([0], [0], [0], "ro")
        
        # For the coodnates in the tip of the robot
        matrix = self.dvhb.final_position()       
        cord_x = matrix[:3, 0]
        cord_y = matrix[:3, 1]
        cord_z = matrix[:3, 2]
        x, y, z = matrix[:3, 3]
    
        self.ax.quiver(x, y, z, *cord_x*self.scale, color="red")
        self.ax.quiver(x, y, z, *cord_y*self.scale, color="green")
        self.ax.quiver(x, y, z, *cord_z*self.scale, color="blue")
        
        # For the ax limits
        self.ax.set_xlim(*self.limits)
        self.ax.set_ylim(*self.limits)
        self.ax.set_zlim(*self.limits)
        
        # For the ax labels
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        
        self.fig.canvas.draw()
    
    
    def reset(self, event):
        for variable in self.variables:
            variable.reset()
    