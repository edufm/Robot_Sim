import robot_sim as rs

method = "DH"

# Method with normal coordinates
if method == "Cordsys":
    a = rs.CordSys(rs.coords_to_cordsys(0, 0, 0, 0, 0, 0))
    b = rs.CordSys(rs.coords_to_cordsys(0, 5, 0, 30, 0, 0))
    c = rs.CordSys(rs.coords_to_cordsys(0, 7, 0, 0, 30, 0))
    
    rs.plot(rs.trace([a, b, c]))

# Method with Denavit_Hatemberg
# theta, a, d, alpha
if method == "DH":
    dh_matrix = [[30, 0, 5, 0],
                 [30, 0, 7, 0]]
    
    dvhb = rs.DvHb(dh_matrix)
    
    rs.plot(rs.trace(dvhb.to_cordsys()))