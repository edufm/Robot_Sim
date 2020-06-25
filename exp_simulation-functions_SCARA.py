"""
This script intends to help the user understand the functions available to the 
Denavit-Hatemberg object in the module with a SCARA model
"""

import robot_sim as rs

# Method with Denavit_Hatemberg
# theta, a, d, alpha

th1 = 0
th2 = 0
d3 = 0.3

dh_matrix = [[0,   1,   0,   0],
             [th1, 0, 0.5, 180],
             [th2, 0, 0.5,   0],
             [0,  d3,   0,   0]]

# Defines the DvHb object
dvhb = rs.DvHb(dh_matrix, joints=[(1,"r"), (2,"r"), (3,"t")])

# Code to view the robot 
if False:
    rs.plot(rs.trace(dvhb.to_cordsys()), ind_limit=False)
    
    
# Code to simulate the robot
if False:
    rs.simulate(dvhb)


# Code to animate robot movement
if False:
    # Define the joint positions the robot will have
    poses = [[0,   0, 0], [-90, -90, 0.5], [0,   0, 0]]
    # Animate the robot to those positions
    rs.animate(dvhb, poses, frames=30*len(poses))


# Code to try to move robot to new position and animate the movement
if False:   
    # Create new transformation matrix for the robot to follow
    new_coords = rs.coords_to_cordsys(-0.5, -0.5, 0.5, 180, 180, 0)    
    
    # Calculate the new joints positions
    joint_pos = dvhb.inverse_kinematic(new_coords, trys=10)
    
    # Show the results to the user
    print(joint_pos)
    print()
    print(new_coords.round(3))
    print()
    original_joints = dvhb.get_all_curr()
    dvhb.recalculate_joints(joint_pos)
    print(dvhb.final_position().round(3))
    dvhb.recalculate_joints(original_joints)
    
    # Animate the results
    rs.animate(dvhb, [dvhb.get_all_curr(), joint_pos])