from .matrix_funcs import multiply, transl, trotx, troty, trotz, dhline2matrix, transf2angs
import numpy as np

class CordSys():
    def __init__(self, matrix):
        
        self.cord_x = matrix[:3, 0]
        self.cord_y = matrix[:3, 1]
        self.cord_z = matrix[:3, 2]
        self.x, self.y, self.z = matrix[:3, 3]
        
        self.matrix = matrix
        
    def coords(self):
        
        theta, psi, phi = transf2angs(self.matrix)
        
        return [self.x, self.y, self.z, self.theta, self.psi, self.phi]


def coords_to_cordsys(x, y, z, theta, phi, psi):
       
    return multiply([transl(x, y, z), trotx(theta), troty(phi), trotz(psi)])

        
class DvHb():
    def __init__(self, dh_matrix, joints=[]):
        """Function to visualize the cordinate systems created limiting axis to nearby constrains
        
        args:
            dh_matrix: Denavit-Hartenberg matrix for this robot
            joints: joints with variable angle/lengh [(line, 'r'), (line, 't')]
            
        returns:
            plot with the cordinates system
        """
        self.dh_matrix = np.array(dh_matrix)
        self.cordsys_list = []
        
        self.joints = joints
        
        
    def to_cordsys(self):
        
        self.cordsys_list = [np.identity(4)]
        for line in self.dh_matrix:
            
            self.cordsys_list.append(dhline2matrix(*line))
            
        return self.cordsys_list
    
    
    def rotate_theta(self, line, ang):
        
        self.dh_matrix[line-1][0] = ang


    def extend_d(self, line, lengh):
        
        self.dh_matrix[line-1][1] = lengh
        
    def get_curr_theta(self, line):
        
        return self.dh_matrix[line-1][0]
    
    def get_curr_d(self, line):
        
        return self.dh_matrix[line-1][1]
    
    

def trace(cordsys_list):
    
    points = [cordsys_list[0]]
    for i in range(1, len(cordsys_list)+1):
        points.append(multiply(cordsys_list[:i]))
    
    return points
