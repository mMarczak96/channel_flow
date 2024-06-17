import pyvista as pv
import numpy as np

# Define the serpentine path parameters
num_channels = 17  # Number of vertical channels
segment_length = 50  # Length of each segment
spacing = 0.93  # Spacing between segments
width = 2  # Width of the path
start_x, start_y = 0, 0  # Starting point of the path

# Create the serpentine path using only horizontal and vertical lines
points = [[0, -2*width-spacing, 0]]
lines = []

current_point = [start_x, start_y, 0]
points.append(current_point)
point_id = 0

for i in range(num_channels):
    y = start_y + i * (width + spacing)
    if i % 2 == 0:
        next_point = [start_x + segment_length, y, 0]
        lines.extend([2, point_id, point_id + 1])
        point_id += 1
        points.append(next_point)
        if i != num_channels - 1:  # Vertical connecting segment
            next_point = [start_x + segment_length, y + width + spacing, 0]
            lines.extend([2, point_id, point_id + 1])
            point_id += 1
            points.append(next_point)
    else:
        next_point = [start_x, y, 0]
        lines.extend([2, point_id, point_id + 1])
        point_id += 1
        points.append(next_point)
        if i != num_channels - 1:  # Vertical connecting segment
            next_point = [start_x, y + width + spacing, 0]
            lines.extend([2, point_id, point_id + 1])
            point_id += 1
            points.append(next_point)

# Convert points to numpy array
points = np.array(points)
print(points)
# Create a polyline from the points
line = pv.PolyData()
line.points = points
line.lines = np.array(lines)

# Extrude the line to create a surface mesh
extrusion = line.extrude((0, 0, width))  # Extrude along the z-axis
extrusion = extrusion.triangulate()
# Refine the mesh to increase the resolution
high_res_mesh = extrusion.subdivide(5, subfilter='linear')  # Increase the level to refine further

# Save the high-resolution surface mesh to an STL file
# high_res_mesh.save('high_res_serpentine_channel.stl')

wall2 = extrusion.translate((-width, 0, 0))
wall2.save('inner_wall.stl')

# Plot the high-resolution extruded surface mesh
plotter = pv.Plotter()
plotter.add_mesh(high_res_mesh, color='lightblue')
# plotter.add_mesh(wall2, color='lightblue')
plotter.add_axes()

plotter.show()
