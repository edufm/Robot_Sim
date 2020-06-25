"""
This script intends to help the user create the Denavit-Hatemberg Matrix by allowing
him to plot both the "usual" cordinate version of a robot, and the Denavit-
matrix he is developing
"""

import robot_sim as rs

# Defines which daa to plot
method = "Cordsys"

# Method with normal coordinates
if method == "Cordsys":
    a = rs.CordSys(rs.coords_to_cordsys(0, 0, 0, 0, 0, 0))
    b = rs.CordSys(rs.coords_to_cordsys(0, 5, 0, 30, 0, 0))
    c = rs.CordSys(rs.coords_to_cordsys(0, 7, 0, 0, 30, 0))
    
    # Plot the results
    rs.plot(rs.trace([a, b, c]))

# Method with Denavit_Hatemberg
# theta, a, d, alpha
if method == "DH":
    dh_matrix = [[30, 0, 5, 0],
                 [30, 0, 7, 0]]
    
    # Create a DvHb object
    dvhb = rs.DvHb(dh_matrix)
    
    # Plot the results
    rs.plot(rs.trace(dvhb.to_cordsys()))