"""
This script intends to help the user understand the functions available to the 
Denavit-Hatemberg object in the module with a inveted model
"""

import robot_sim as rs

l0 = 0.08956
l1 = 0
l2 = 0.425
l3 = 0
l4 = 0.3922
l5 = 0.1091
l6 = 0.09465 
l7 = 0.0823

th0 = 0
th1 = 90
th2 = 0
th3 = 270
th4 = 0
th5 = 0

dh_matrix = [[th0,  l0,  0,    90],
             [th1,  l1, l2,     0],
             [th2, -l3, l4,     0],
             [th3,  l5,  0,   -90],
             [th4,  l6,  0,    90],
             [th5,  l7,  0,     0]]

# Defines the DvHb object
dvhb = rs.DvHb(dh_matrix, joints=[(0,"r"), (1,"r"), (2,"r"), (3,"r"), (4, "r"), (5,"r")])

# Code to view the robot 
if False:
    rs.plot(rs.trace(dvhb.to_cordsys()), ind_limit=False)
    
    
# Code to simulate the robot
if False:
    rs.simulate(dvhb)


# Code to animate robot movement
if False:
    # Define the joint positions the robot will have
    poses = [[0,90,0,0,0,0], [0,135,-60,90,90,0]]
    # Animate the robot to those positions
    rs.animate(dvhb, poses, frames=30*len(poses))


# Code to try to move robot to new position and animate the movement
if False:
    # Create new transformation matrix for the robot to follow
    new_coords = rs.coords_to_cordsys(-0.3030, -0.1091, 0.6988, 0, -75, 90)
    
    # Calculate the new joints positions
    joint_pos = dvhb.inverse_kinematic(new_coords, trys=10, castrule=None)
    
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