import pyvista as pv
import numpy as np
import math
# Define the serpentine path parameters
num_channels = 1  # Number of vertical channels
length = 50  # Length of each segment
spacing = 1  # Spacing between segments
width = 2  
step = 3 * width + spacing
start_x_right, start_y_right, start_z_right = width, 0, 0
start_x_left, start_y_left, start_z_left = 0, -width, 0



point_0_right = [start_x_right, start_y_right, start_z_right] 
point_1_right = [start_x_right, start_y_right + width, start_z_right ]  
point_2_right = [start_x_right + length, start_y_right + width, start_z_right] 
point_3_right = [start_x_right + length, start_y_right + step, start_z_right] 

point_0_left = [start_x_left, start_y_left, start_z_left] 
point_1_left = [start_x_left, start_y_left + step, start_z_left]
point_2_left = [start_x_left + length, start_y_left + step, start_z_left]
point_3_left = [start_x_left + length, start_y_left + step + spacing, start_z_left]

right_channel_points, right_channel_lines = [], []
left_channel_points, left_channel_lines = [point_0_left, point_1_left, point_2_left, point_3_left], []


# for c in np.linspace(1, num_channels, num_channels):
for c in range(num_channels):
    
    new_point_0 = [point_0_right[0], point_0_right[1] + step * c, point_0_right[2]]
    new_point_1 = [point_1_right[0], point_1_right[1] + step * c, point_1_right[2]]
    new_point_2 = [point_2_right[0], point_2_right[1] + step * c, point_2_right[2]]
    new_point_3 = [point_3_right[0], point_3_right[1] + step * c, point_3_right[2]]

    right_channel_points.append(new_point_0)
    right_channel_points.append(new_point_1)
    right_channel_points.append(new_point_2)
    right_channel_points.append(new_point_3)

for point_id in range(len(right_channel_points)):
    right_channel_lines.append([2, point_id, point_id + 1])
    
print(right_channel_points)
print(left_channel_points)

right_mesh = pv.PolyData()
right_mesh.points = np.array(right_channel_points)
right_mesh.lines = np.array(right_channel_lines[:-1])

left_mesh = pv.PolyData(left_channel_points)
# left_mesh.points = np.array(left_channel_points)



plotter = pv.Plotter()
plotter.add_mesh(right_mesh, color='lightblue') 
plotter.add_mesh(left_mesh, color='red')
plotter.add_axes()
plotter.view_xy()
plotter.show()



