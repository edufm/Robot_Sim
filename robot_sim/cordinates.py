from .matrix_funcs import multiply, transl, trotx, troty, trotz, dhline2matrix, transf2angs
import numpy as np
from scipy.optimize import minimize


class CordSys():
    def __init__(self, matrix):
        """
        Class used to hold a transformation matrix (very limited use)
        
        args:
            matrix: the transformation matrix to be held
            
        returns:
            object that represents a transformation matrix
        """
        self.cord_x = matrix[:3, 0]
        self.cord_y = matrix[:3, 1]
        self.cord_z = matrix[:3, 2]
        self.x, self.y, self.z = matrix[:3, 3]
        
        self.matrix = matrix
        
        
    def coords(self):
        """
        Function that converts the transformation matrix in the absolute position
        
        returns:
            list of cordnates x, y, z, theta, psi, phi
        """
        theta, psi, phi = transf2angs(self.matrix)
        
        return [self.x, self.y, self.z, self.theta, self.psi, self.phi]


class DvHb():
    def __init__(self, dh_matrix, joints=[]):
        """
        Class used to manipulate and represents Denavit-Hatemberg Matrix
        
        args:
            dh_matrix: Denavit-Hartenberg matrix for this robot
            joints: joints with variable angle/lenght [(line, 'r'), (line, 't')]
            
        returns:
            object taht reppresents the Denavit-Hatemberg function
        """
        self.dh_matrix = np.array(dh_matrix, dtype=np.float64)
        self.cordsys_list = []
        
        self.joints = joints
        
        
    def to_cordsys(self):
        """ 
        Function to convert Denavit-Hatemberg matrix in to transformation matrixes for each line.
        
        returns:
            list of transformation matrixes
        """
        self.cordsys_list = [np.identity(4)]
        for line in self.dh_matrix:
            
            self.cordsys_list.append(dhline2matrix(*line))
            
        return self.cordsys_list
    
    
    def final_position(self):
        """ 
        Function used to calculate the robot final transformation matrix
        
        returns:
            transformation matrix of the point of the claw
        """
        return multiply(self.to_cordsys())
    
    
    def rotate_theta(self, line, ang):
        """ 
        Function that changes a specifc theta in a specific line of the Denavit-Hatemberg matrix
        
        args:
            line: which line to edit (joint)
            ang: new_angle for the joint
        """
        self.dh_matrix[line][0] = ang


    def extend_d(self, line, lenght):
        """ 
        Function that changes a specifc d in a specific line of the Denavit-Hatemberg matrix
        
        args:
            line: which line to edit (joint)
            lenght: new lenght for the joint
        """
        self.dh_matrix[line][1] = lenght
        
        
    def get_curr_theta(self, line):
        """ 
        Function that finds the value of a specifc theta on the Denavit-Hatemberg matrix
        
        args:
            line: which line to look
            
        returns:
            the vvalue of theta for taht line
        """
        return self.dh_matrix[line][0]
    
    
    def get_curr_d(self, line):
        """ 
        Function that finds the value of a specifc d on the Denavit-Hatemberg matrix
        
        args:
            line: which line to look
            
        returns:
            the value of d for taht line
        """
        return self.dh_matrix[line][1]
    
    
    def get_all_curr(self):
        """ 
        Function that finds the position of all joints on the Denavit-Hatemberg object
            
        returns:
            a vector with all the positions of the joints
        """
        curr = []
        for joint in self.joints:
            if joint[1] == "r":
                curr.append(self.get_curr_theta(joint[0]))
            if joint[1] == "t":
                curr.append(self.get_curr_d(joint[0]))
                
        return curr
    
    
    def recalculate_joints(self, joints_pos):
        """ 
        Function that assign a new position vector to the  Denavit-Hatemberg matrix
            
        args:
            a vector with all the positions of the joints
        """
        for n, variable in enumerate(joints_pos):
            if self.joints[n][1] == "r":
                self.rotate_theta(self.joints[n][0], variable)
            elif self.joints[n][1] == "t":
                self.extend_d(self.joints[n][0], variable)
    
    
    def inverse_kinematic_target(self, joints_pos, target_matrix):
        """  
        Function that calculates the distance between the a sugested pose 
        trasnformation matrix and the target transformation matrix
        
        args:
            joints_pos: a vector with all the positions of the joints
            target_matrix: a transformation matrix to calculate the distance to
        """
        
        self.recalculate_joints(joints_pos)
        
        return abs(self.final_position() - target_matrix).sum()
    
    
    def inverse_kinematic(self, target_matrix, max_iter=100, trys=1, castrule='safe'):
        """
        Function that performs a inversed kinematic calculaion with a numerial algorithm
        
        args:
            target_matrix: a transformation matrix to calculate the position for
            max_iter: Maximum number of iterations in the solver, default=100
            trys: How many times restart the solver if the simulation failes, default = 1
            castule: if "safe" will raise a error when the optimazation fails, default "safe"
        """
        
        joints_pos = self.get_all_curr()
        
        bnds = [(0, 360) if joint[1] == "r" else (0, 10) for joint in self.joints]
    
        results = minimize(self.inverse_kinematic_target, joints_pos, 
                               bounds=bnds, args=[target_matrix], tol=10e-8, 
                               options={"maxiter":max_iter})
    
        if results.success and results.fun < 1:
            self.recalculate_joints(joints_pos)
            print("uncertenty of calculation:", results.fun)
            return results.x
        
    
        all_results = []
        for i in range(trys):
            initial = np.array([n[1] for n in bnds]) * np.random.random(len(bnds))/2
            results = minimize(self.inverse_kinematic_target, initial, 
                               bounds=bnds, args=[target_matrix], tol=10e-8, 
                               options={"maxiter":max_iter})
            
            all_results.append([results.fun, results.success, results.x])
        
        
        best_result = (10000, 0)
        for result in all_results:
            if result[0] < best_result[0]:
                best_result = (result[0], result[1], result[2])
    
        self.recalculate_joints(joints_pos)
        if not best_result[1] and castrule == 'safe':
            
            raise Exception("Optimization failed to converge")
            
        else:
            print("uncertenty of calculation:", results.fun)
            return results.x


def coords_to_cordsys(x, y, z, theta, phi, psi):
    """
    Function that converts absolute position into a transformation matrix
    
    args:
        x, y, z, theta, psi, phi
        
    returns:
        transformation matrix that represents the specified position
    """
    return multiply([transl(x, y, z), trotx(theta), troty(phi), trotz(psi)])


def trace(cordsys_list):
    """
    Function that converts a list of transformation matrix in a list of 
    multiplied transformation matrixes that represents the continuos motion 
    of the initial matrix. Very usefull for plotting data.
    
    args:
        cordsys_list: List of transformation matrixes
        
    returns:
        list of multiplied transformation matrixes
    """
    points = []
    for i in range(1, len(cordsys_list)+1):
        points.append(multiply(cordsys_list[:i]))
    
    return points

