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
th9 = 0

dh_matrix = [[th1,    l1,  0, 90],
             [90,     l2,  0,   0],
             [th3,     0, l3, 180],
             [th4,    l4,  0,   0],
             [0,       0, l5, 180],
             [90+th6, l6,  0,  90],
             [th7,    l7,  0, -90],
             [th9,    l8,  0,   0]
             ]

dvhb = rs.DvHb(dh_matrix, joints=[(1,"r"), (3,"r"), (4,"t"), (6,"r")])

#rs.plot(rs.trace(dvhb.to_cordsys()), ind_limit=True)
rs.animate(dvhb)