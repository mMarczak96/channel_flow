import numpy as np
import pandas as pd
import os
import pyvista as pv 

# All values are given in milimiters

# channel_width = 2
# channel_length = 50 
# channel_separation = 14 / 15
# channel_short_length = 2 * channel_width + channel_separation

# channel_long = pv.Box(bounds=(0, channel_width, 0, -channel_length, 0, channel_width), level=100, quads=False)
# channel_short = pv.Box(bounds=(0, channel_short_length, 0, channel_width, 0, channel_width), level=5, quads=False)




# c_width = 2
# c_length = 50 
# c_sep = 14 / 15
# n_c = 16

# points_0, points_1, points_2, points_3 = np.zeros([2*n_c,3]), np.zeros([2*n_c,3]), np.zeros([2*n_c,3]), np.zeros([2*n_c,3])
# point_0, point_1, point_2, point_3 = [0,0,0], [0,0,0], [0,0,0], [0,0,0]
# for i in range(2 * n_c):
#     if i%2 == 0:
#         point_0 = [0, point_0[1] + 2, 0] 
#         point_1 = [2, point_1[1] + 2, 0] 
#         point_2 = [c_length - c_width, point_2[1] + 2, 0] 
#         point_3 = [c_length, point_3[1] + 2, 0] 

#     else:
#         point_0 = [0, point_0[1] + c_sep, 0]
#         point_1 = [2, point_1[1] + c_sep, 0]
#         point_2 = [c_length - c_width, point_2[1] + c_sep, 0]
#         point_3 = [c_length, point_3[1] + c_sep, 0]

#     points_0[i] = point_0
#     points_1[i] = point_1
#     points_2[i] = point_2
#     points_3[i] = point_3


# points_merge_1 = np.append(points_0, points_1, axis=0)
# points_merge_2 = np.append(points_2, points_3, axis=0)
# points_cloud = np.append(points_merge_1, points_merge_2, axis=0)


# lines = np.array([
#     [2, 0, 1],  
#     [2, 1, 2],  
#     [2, 2, 3],  
#     [2, 3, 4]   
# ])

# line_polydata = pv.PolyData()
# line_polydata.points = points_cloud
# line_polydata.lines = lines

# plotter = pv.Plotter()
# plotter.add_mesh(line_polydata, show_edges=True, color='lightblue')
# plotter.show()



# Define the initial variables
L = 10.0  # Length of the channel
S = 2.0   # Spacing between channels
D = 2.0   # Depth and width of the channel
num_channels = 5  # Number of channels

# Initialize lists for points
points = []

# Generate the points and lines for the spiral path
for i in range(num_channels):
    y_base = i * S
    points.append([0, y_base, 0])
    points.append([L, y_base, 0])
    points.append([L, y_base + D, 0])
    points.append([0, y_base + D, 0])
    
    if i < num_channels - 1:
        points.append([0, y_base + D + S, 0])  # Connect to the next segment start

# Convert points to numpy array
points = np.array(points)
lines = np.array([
    [2,0,1],
    [2,1,2],
    [2,2,3]
])
lines = np.zeros([len(points), 3])
lines = []
for i in range(len(points)):
    line = [2,i,i+1]
    # lines[i]=line
    lines.append(line)

print(lines)

path = pv.PolyData()
path.points = points
path.lines = lines[:10]


# Optional: Visualize the geometry (commented out if running in a non-GUI environment)
plotter = pv.Plotter()
plotter.add_mesh(path, color='black')
plotter.show()

