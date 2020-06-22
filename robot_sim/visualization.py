import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot(cordsys_list, ind_limit=False):
    """Function to visualize the cordinate systems created limiting axis to nearby constrains
    
    args:
        cordsys_list: a list of cordsys or transformation matrix
        ind_limit: limit each plot axle individually or by the global min/max, default=False
        
    returns:
        plot with the cordinates system
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Renomeia os eixos
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    # Cria um ponto na origem
    ax.plot([0], [0], [0], "bo", markersize=20)
    
    # Verifica quais são todos os pontos de dados
    all_points = []
    for cordsys in cordsys_list:
        
        if isinstance(cordsys, np.ndarray):
            matrix = cordsys
        else:
            matrix = cordsys.matrix
            
        all_points.append(matrix[:3, 3])
    all_points = np.array(all_points)
    maxs, mins = all_points.max(axis=0), all_points.min(axis=0)
    abs_max, abs_min = max(maxs), min(mins)
    vec_scale = 0.1*abs_max
    space = 2*vec_scale
    
    # Liga os pontos com uma linha
    ax.plot(all_points[:, 0], all_points[:, 1], all_points[:, 2])
    
    
    for cordsys in cordsys_list:
        
        if isinstance(cordsys, np.ndarray):
            matrix = cordsys
        else:
            matrix = cordsys.matrix
            
        cord_x = matrix[:3, 0] * vec_scale
        cord_y = matrix[:3, 1] * vec_scale
        cord_z = matrix[:3, 2] * vec_scale
        x, y, z = matrix[:3, 3]
        
    
        ax.quiver(x, y, z, *cord_x, color="red")
        ax.quiver(x, y, z, *cord_y, color="green")
        ax.quiver(x, y, z, *cord_z, color="blue")

    
    if ind_limit:
        ax.set_xlim([mins[0]-space, maxs[0]+space])
        ax.set_ylim([mins[1]-space, maxs[1]+space])
        ax.set_zlim([mins[2]-space, maxs[2]+space])
    else:
        ax.set_xlim([abs_min-space, abs_max+space])
        ax.set_ylim([abs_min-space, abs_max+space])
        ax.set_zlim([abs_min-space, abs_max+space])
