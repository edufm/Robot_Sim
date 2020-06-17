import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class CordSys():
    def __init__(self, x, y, z, theta, phi, psi):
        
        self.x = x
        self.y = y
        self.z = z
        
        self.transl = transl(x, y, z)
        
        self.theta = theta
        self.phi = phi
        self.psi = psi
        
        self.trotx = trotx(theta)
        self.troty = troty(phi)
        self.trotz = trotz(psi)
        
        self.trans = np.transpose(np.array([x, y, z, 1]))
        
    def coords(self):
        
        return [self.x, self.y, self.z, self.theta, self.phi, self.psi]
    
    
    def matrix(self):
        
        return np.dot(np.dot(np.dot(self.transl, self.trotx), self.troty), self.trotz)
        
        
def plot_lmt(cordsys_list):
    """Function to visualize the cordinate systems created limiting axis to nearby constrains
    
    args:
        cordsys_list: a list of cordsys or transformation matrix
        
    returns:
        plot with the cordinates system
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    maxs, mins = [0,0,0], [0,0,0]
    for cordsys in cordsys_list:
        
        if isinstance(cordsys, np.ndarray):
            matrix = cordsys
        else:
            matrix = cordsys.matrix()
            
        cord_x = matrix[:3, 0]
        cord_y = matrix[:3, 1]
        cord_z = matrix[:3, 2]
        x, y, z = matrix[:3, 3]

        maxs[0], mins[0] = max([maxs[0], x]), min([mins[0], x])
        maxs[1], mins[1] = max([maxs[1], y]), min([mins[1], y])
        maxs[2], mins[2] = max([maxs[2], z]), min([mins[2], z])
        
    
        ax.quiver(x, y, z, *cord_x)
        ax.quiver(x, y, z, *cord_y)
        ax.quiver(x, y, z, *cord_z)

    
    ax.set_xlim([mins[0]-2, maxs[0]+2])
    ax.set_ylim([mins[1]-2, maxs[1]+2])
    ax.set_zlim([mins[2]-2, maxs[2]+2])


def plot(cordsys_list):
    """Function to visualize the cordinate systems created
    
    args:
        cordsys_list: a list of cordsys or transformation matrix
        
    returns:
        plot with the cordinates system
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    maxs, mins = 0, 0
    for cordsys in cordsys_list:
        
        if isinstance(cordsys, np.ndarray):
            matrix = cordsys
        else:
            matrix = cordsys.matrix()
            
        cord_x = matrix[:3, 0]
        cord_y = matrix[:3, 1]
        cord_z = matrix[:3, 2]
        x, y, z = matrix[:3, 3]

        maxs, mins = max([x,y,z]), min([x,y,z])
        
    
        ax.quiver(x, y, z, *cord_x)
        ax.quiver(x, y, z, *cord_y)
        ax.quiver(x, y, z, *cord_z)

    
    ax.set_xlim([mins-2, maxs+2])
    ax.set_ylim([mins-2, maxs+2])
    ax.set_zlim([mins-2, maxs+2])
    
    
def multiply(cordsys_list):
    """Function to multiply cordinate systems
    
    args:
        cordsys_list: a list of cordsys or transformation matrixes
        
    returns:
        the matrix resultant of the multiplication
    """
    if isinstance(cordsys_list[0], np.ndarray):
        result = cordsys_list[0]
    else:
        result = cordsys_list[0].matrix()
    
    
    for cordsys in cordsys_list:
        if isinstance(cordsys, np.ndarray):
            matrix = cordsys
        else:
            matrix = cordsys.matrix()
            
        result = np.dot(result, matrix)
        
    return result


def sin(deg):
    
    return np.sin(np.deg2rad(deg))

def cos(deg):
    
    return np.cos(np.deg2rad(deg))
    
    
def rotx(deg):
    return np.array([[1,        0,         0],
                     [0, cos(deg), -sin(deg)],
                     [0, sin(deg),  cos(deg)]])

def trotx(deg):
    return np.array([[1,        0,         0, 0],
                     [0, cos(deg), -sin(deg), 0],
                     [0, sin(deg),  cos(deg), 0],
                     [0,        0,         0, 1]])

def roty(deg):
    return np.array([[cos(deg),  0,   sin(deg)],
                     [0,         1,          0],
                     [-sin(deg), 0,   cos(deg)]])

def troty(deg):
    return np.array([[cos(deg),  0,   sin(deg),  0],
                     [        0, 1,          0,  0],
                     [-sin(deg), 0,   cos(deg),  0],
                     [       0 , 0,           0, 1]])

def rotz(deg):
    return np.array([[cos(deg), -sin(deg),  0],
                     [sin(deg), cos(deg),   0],
                     [       0,        0,   1]])

def trotz(deg):
    return np.array([[cos(deg), -sin(deg),    0, 0],
                     [sin(deg),  cos(deg),    0, 0],
                     [       0,         0,    1, 0],
                     [       0 ,        0,    0, 1]])

def transl(x, y, z):
    return np.array([[1,  0,  0, x],
                     [0,  1,  0, y],
                     [0,  0,  1, z],
                     [0 , 0,  0, 1]])