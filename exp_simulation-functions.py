import robot_sim as rs

# Method with Denavit_Hatemberg
# theta, a, d, alpha

l1 = 0.08956
l2 = 0.1091
l3 = 0.425
l4 = 0.1091
l5 = 0.3922
l6 = 0.1091
l7 = 0.09465 
l8 = 0.0823

th1 = 0
th3 = 0
th4 = 0
th6 = 0
th7 = 0
th8 = 0

dh_matrix = [[th1,    l1,  0, 90],
             [90,     l2,  0,   0],
             [th3,     0, l3, 180],
             [th4,    l4,  0,   0],
             [0,       0, l5, 180],
             [90+th6, l6,  0,  90],
             [th7,    l7,  0, -90],
             [th8,    l8,  0,   0]
             ]

dvhb = rs.DvHb(dh_matrix, joints=[(0,"r"), (2,"r"), (3,"r"), (5,"r"), (6,"r"), (7,"r")])

# Code to view the robot 
if False:
    rs.plot(rs.trace(dvhb.to_cordsys()), ind_limit=False)
    
# Code to simulate the robot
if True:
    rs.simulate(dvhb)

# Code to animate robot movement
if False:
    initial_pos = [0,-90,0,0,0,0]
    final_pos = [90,90,0,180,0,0]
    
    rs.animate(dvhb, initial_pos, final_pos, frames=200)


# Code to try to move robot to new position and animate the movement
if False:
    new_coords = [[-0.766 ,  0.6428, -0.    ,  0.0],
                  [ 0.    , -0.    , -1.    ,  -0.2214],
                  [-0.6428, -0.766 ,  0.    ,  0.9793],
                  [ 0.    ,  0.    ,  0.    ,  1.    ]]
    joint_pos, coords= dvhb.inverse_kinematic(new_coords, keep_results=True)
    print(joint_pos)
    print(coords.round(4))
    
    rs.animate(dvhb, dvhb.get_all_curr(), joint_pos)