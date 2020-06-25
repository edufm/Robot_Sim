# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 18:58:45 2020

@author: edufe
"""
import numpy as np
import math as m

# -----------------------------------------------------------------------------
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
        result = cordsys_list[0].matrix
    
    
    for cordsys in cordsys_list[1:]:
        if isinstance(cordsys, np.ndarray):
            matrix = cordsys
        else:
            matrix = cordsys.matrix
            
        result = np.dot(result, matrix)
        
    return result


# -----------------------------------------------------------------------------
def sin(deg):
    """ 
    Function to calculate sine of angle in degrees
    
    args:
        deg: angle in degree
        
    returns:
        sine of angle
    """    
    return np.sin(np.deg2rad(deg))

def cos(deg):
    """ 
    Function to calculate cosisne of angle in degrees
    
    args:
        deg: angle in degree
        
    returns:
        cosine of angle
    """ 
    return np.cos(np.deg2rad(deg))


# -----------------------------------------------------------------------------
def dhline2matrix(theta, d, a, alpha):
    """ 
    Function to calculate a transformation matrix from Denavit-Hatemberg inputs
    
    args:
        theta (in degrees), d, a, alpha (in degrees)
        
    returns:
        transformation matrix for that input
    """ 
    return np.array([[cos(theta), -sin(theta)*cos(alpha),    sin(theta)*sin(alpha), a*cos(theta)],
                     [sin(theta),  cos(theta)*cos(alpha),   -cos(theta)*sin(alpha), a*sin(theta)],
                     [         0,             sin(alpha),               cos(alpha),            d],
                     [         0,                      0,                        0,            1]])

# -----------------------------------------------------------------------------
def transl(x, y, z):
    """ 
    Function to calculate a transformation matrix from x, y, z inputs
    
    args:
        x, y, z
        
    returns:
        transformation matrix for that input
    """ 
    return np.array([[1,  0,  0, x],
                     [0,  1,  0, y],
                     [0,  0,  1, z],
                     [0 , 0,  0, 1]])
    
# -----------------------------------------------------------------------------
def rotx(deg):
    """ 
    Function to calculate a rotation matrix from a agle in x
    
    args:
        deg: angle in degrees
        
    returns:
        transformation matrix for that input
    """ 
    return np.array([[1,        0,         0],
                     [0, cos(deg), -sin(deg)],
                     [0, sin(deg),  cos(deg)]])

def trotx(deg):
    """ 
    Function to calculate a transformation matrix from a agle in x
    
    args:
        deg: angle in degrees
        
    returns:
        transformation matrix for that input
    """ 
    return np.array([[1,        0,         0, 0],
                     [0, cos(deg), -sin(deg), 0],
                     [0, sin(deg),  cos(deg), 0],
                     [0,        0,         0, 1]])
    
# -----------------------------------------------------------------------------
def roty(deg):
    """ 
    Function to calculate a rotation matrix from a agle in y
    
    args:
        deg: angle in degrees
        
    returns:
        transformation matrix for that input
    """ 
    return np.array([[cos(deg),  0,   sin(deg)],
                     [0,         1,          0],
                     [-sin(deg), 0,   cos(deg)]])

def troty(deg):
    """ 
    Function to calculate a transformation matrix from a agle in y
    
    args:
        deg: angle in degrees
        
    returns:
        transformation matrix for that input
    """ 
    return np.array([[cos(deg),  0,   sin(deg),  0],
                     [        0, 1,          0,  0],
                     [-sin(deg), 0,   cos(deg),  0],
                     [       0 , 0,           0, 1]])
    
# -----------------------------------------------------------------------------
def rotz(deg):
    """ 
    Function to calculate a rotation matrix from a agle in y
    
    args:
        deg: angle in degrees
        
    returns:
        transformation matrix for that input
    """ 
    return np.array([[cos(deg), -sin(deg),  0],
                     [sin(deg), cos(deg),   0],
                     [       0,        0,   1]])

def trotz(deg):
    """ 
    Function to calculate a transformation matrix from a agle in z
    
    args:
        deg: angle in degrees
        
    returns:
        transformation matrix for that input
    """ 
    return np.array([[cos(deg), -sin(deg),    0, 0],
                     [sin(deg),  cos(deg),    0, 0],
                     [       0,         0,    1, 0],
                     [       0 ,        0,    0, 1]])
    
# -----------------------------------------------------------------------------
def transf2angs(matrix, single=True):
    """ 
    Function to calculate the angles row, pitch, yall from transformation matrix
    
    args:
        transformation matrix
        
    returns:
         row, pitch, yall
    """ 
    theta  = -m.asin(matrix[0][2])
    theta1 = np.pi - theta
    
    psi    = m.atan2(matrix[2][1]/m.cos(theta), matrix[2][2]/m.cos(theta))
    psi1   = m.atan2(matrix[2][1]/m.cos(theta1), matrix[2][2]/m.cos(theta1))
    
    phi    = m.atan2(matrix[1][0]/m.cos(theta), matrix[0][0]/m.cos(theta))
    phi1   = m.atan2(matrix[1][0]/m.cos(theta1), matrix[0][0]/m.cos(theta1))
    
    if single:    
        return (np.rad2deg(theta), np.rad2deg(psi), np.rad2deg(phi))    
    else:
        return (np.rad2deg(theta), np.rad2deg(theta1), 
                np.rad2deg(psi), np.rad2deg(psi1), 
                np.rad2deg(phi), np.rad2deg(phi1))