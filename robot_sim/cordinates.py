from .matrix_funcs import multiply, transl, trotx, troty, trotz, dhline2matrix, transf2angs
import numpy as np
from scipy.optimize import minimize


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
    
    
    def final_position(self):
        
        return multiply(self.to_cordsys())
    
    
    def rotate_theta(self, line, ang):
        
        self.dh_matrix[line][0] = ang


    def extend_d(self, line, lengh):
        
        self.dh_matrix[line][1] = lengh
        
    def get_curr_theta(self, line):
        
        return self.dh_matrix[line][0]
    
    def get_curr_d(self, line):
        
        return self.dh_matrix[line][1]
    
    def get_all_curr(self):
    
        curr = []
        for joint in self.joints:
            if joint[1] == "r":
                curr.append(self.get_curr_theta(joint[0]))
            if joint[1] == "t":
                curr.append(self.get_curr_d(joint[0]))
                
        return curr
    
    def recalculate_joints(self, joints_pos):
        
        for n, variable in enumerate(joints_pos):
            if self.joints[n][1] == "r":
                self.rotate_theta(self.joints[n][0], variable)
            elif self.joints[n][1] == "t":
                self.extend_d(self.joints[n][0], variable)
    
    def inverse_kinematic_target(self, vectors, target_matrix):
        
            self.recalculate_joints(vectors)
            
            return abs(self.final_position() - target_matrix).sum()
    
    def inverse_kinematic(self, target_matrix, max_iter=100, keep_results=False):
        
        vectors = self.get_all_curr()
        
        bnds = [(0, 360) if joint[1] == "r" else (0, 5) for joint in self.joints]
    
        
        results = minimize(self.inverse_kinematic_target, vectors, 
                           bounds=bnds, args=[target_matrix], tol=10e-8, 
                           options={"max_iter":max_iter})
        
        if keep_results:
            coords = self.final_position()
        
        self.recalculate_joints(vectors)
        
        print("uncertenty of calculation:", results.fun)
        
        if not results.success:
            raise Exception("Optimization failed to converge")
            
        elif keep_results:
            return results.x, coords
            
        else:
            return results.x
    

def trace(cordsys_list):
    
    points = []
    for i in range(1, len(cordsys_list)+1):
        points.append(multiply(cordsys_list[:i]))
    
    return points
