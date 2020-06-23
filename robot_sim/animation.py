# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:44:56 2020

@author: edufe
"""

from copy import deepcopy

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from .cordinates import trace

class animate():
    def __init__(self, dvhb, initial_joints, final_joints, frames=60, save=False):
        
        from IPython import get_ipython
        ipy = get_ipython()
        if ipy != None:
            ipy.run_line_magic('matplotlib', 'auto')

        self.dvhb = deepcopy(dvhb)
        self.animation_pos = np.linspace(initial_joints, final_joints, frames)
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Cria os graficos iniciais
        self.line, = self.ax.plot([], [], [], lw=2)
        self.points, = self.ax.plot([], [], [], "bo")
        self.ax.plot([0], [0], [0], "ro")
        
        #Cria os ponos iniciais e finais
        self.dvhb.recalculate_joints(final_joints)
        self.p_fin = self.dvhb.final_position()[:3, 3]  
        self.p_final, = self.ax.plot([], [], [], "rx")
        self.dvhb.recalculate_joints(initial_joints)
        self.p_ini = self.dvhb.final_position()[:3, 3] 
        self.p_inicial, = self.ax.plot([], [], [], "gx")
        
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
                             frames=frames, interval=20, blit=True)
    
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
        
        self.p_final.set_xdata(self.p_fin[0])
        self.p_final.set_ydata(self.p_fin[1])
        self.p_final.set_3d_properties(self.p_fin[2])
        
        self.p_inicial.set_xdata(self.p_ini[0])
        self.p_inicial.set_ydata(self.p_ini[1])
        self.p_inicial.set_3d_properties(self.p_ini[2])
        
        return (self.line, self.points, 
                self.quiverx, self.quivery, self.quiverz, 
                self.p_inicial, self.p_final)
    

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

