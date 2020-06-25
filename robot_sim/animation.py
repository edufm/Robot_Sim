# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:44:56 2020

@author: edufe
"""

from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .cordinates import trace

class animate():
    """    
    Class that animates a dvhb object based on diferent joint positions
    obs: funtions for this class are only used by the class itself and 
    will not work outside of animation context
    
    args:
        dvhb: dvhb object already configured with mtrix and joints
        poses: list of poses the robot should move to and from
        frames: number of frames in teh animation (recomended 30 per pose), default=60
        save: if true will save the animation as a gif in the current execution folder
      
    returns:
        perform the robot animation to the poses
    """
    def __init__(self, dvhb, poses, frames=60, save=False):
        
        from IPython import get_ipython
        ipy = get_ipython()
        if ipy != None:
            ipy.run_line_magic('matplotlib', 'auto')

        self.dvhb = deepcopy(dvhb)
        
        frames = frames//len(poses)
        self.animation_pos = []
        for i in range(len(poses)-1):
            self.animation_pos += list(np.linspace(poses[i], poses[i+1], frames))
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Cria os graficos iniciais
        self.line, = self.ax.plot([], [], [], lw=2)
        self.points, = self.ax.plot([], [], [], "bo")
        self.ax.plot([0], [0], [0], "ro")
        
        #Cria os ponos iniciais e finais
        self.stop_p = [[], [], []]
        for pose in poses:
            self.dvhb.recalculate_joints(pose)
            x, y, z = self.dvhb.final_position()[:3, 3]
            self.stop_p[0].append(x)
            self.stop_p[1].append(y)
            self.stop_p[2].append(z)
            
        self.stop_points, = self.ax.plot([], [], [], "rx")
        self.dvhb.recalculate_joints(poses[0])
        
        # Cria os eixos de coordenadas da ponta do robo
        self.quiverx, = self.ax.plot([], [], [], color="red")
        self.quivery, = self.ax.plot([], [], [], color="green")
        self.quiverz, = self.ax.plot([], [], [], color="blue")
        
        # Cinfigura os limites da simulação
        self.limits = self.get_limits()
        self.scale = self.limits[1]*0.1
        
        self.ax.set_xlim(*self.limits)
        self.ax.set_ylim(*self.limits)
        self.ax.set_zlim(*self.limits)

        anim = FuncAnimation(self.fig, self.animate, 
                             frames=len(self.animation_pos), interval=20, blit=True)
    
        if save:
            anim.save('robot.gif', writer='imagemagick')
    
    
    def animate(self, i):

        self.dvhb.recalculate_joints(self.animation_pos[i])
        
        x, y, z = self.get_points()
        
        self.line.set_xdata(x)
        self.line.set_ydata(y)
        self.line.set_3d_properties(z)
        
        self.points.set_xdata(x[1:])
        self.points.set_ydata(y[1:])
        self.points.set_3d_properties(z[1:])
        
        # For the coodnates in the tip of the robot
        matrix = self.dvhb.final_position()
        cord_x = matrix[:3, 0]*self.scale
        cord_y = matrix[:3, 1]*self.scale
        cord_z = matrix[:3, 2]*self.scale
        x, y, z = matrix[:3, 3]
        
        self.quiverx.set_xdata([x, x+cord_x[0]])
        self.quiverx.set_ydata([y, y+cord_x[1]])
        self.quiverx.set_3d_properties([z, z+cord_x[2]])
        
        self.quivery.set_xdata([x, x+cord_y[0]])
        self.quivery.set_ydata([y, y+cord_y[1]])
        self.quivery.set_3d_properties([z, z+cord_y[2]])        
        
        self.quiverz.set_xdata([x, x+cord_z[0]])
        self.quiverz.set_ydata([y, y+cord_z[1]])
        self.quiverz.set_3d_properties([z, z+cord_z[2]])
        
        self.stop_points.set_xdata(self.stop_p[0])
        self.stop_points.set_ydata(self.stop_p[1])
        self.stop_points.set_3d_properties(self.stop_p[2])
        
        return (self.line, self.points, 
                self.quiverx, self.quivery, self.quiverz, 
                self.stop_points)
    

    def get_limits(self):
        
        # Verifica quais são todos os pontos de dados
        all_points = []
        for cordsys in trace(self.dvhb.to_cordsys()):
            all_points.append(cordsys[:3, 3])

        all_points = np.array(all_points)
        maxs, mins = all_points.max(axis=0), all_points.min(axis=0)
        abs_max = max([max(maxs), -min(mins)])
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

