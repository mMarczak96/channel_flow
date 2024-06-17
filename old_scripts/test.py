import pyvista as pv
import numpy as np

# Define the serpentine path parameters
num_channels = 11  # Number of vertical channels
segment_length = 50  # Length of each segment
spacing = 1  # Spacing between segments
width = 2  # Width of the path
start_x_outer, start_y_outer = 0, 0
start_x_inner, start_y_inner = -width, -2 *width - spacing

# Create the serpentine path using only horizontal and vertical lines_outer
points_outer, lines_outer = [[0, -2*width, 0]], []
points_inner, lines_inner = [[-width, -3*width, 0]], []

current_point_outer = [start_x_outer, start_y_outer, 0]
current_point_inner = [start_x_inner, start_y_inner, 0]
points_outer.append(current_point_outer)
points_inner.append(current_point_inner)
point_id_outer, point_id_inner = 0, 0
for channel in ['outer', 'inner']:
    for i in range(num_channels):
        if channel == 'outer':
            y = start_y_outer + i * (2*width + spacing)
            if i % 2 == 0:
                y = start_y_outer + i * (2*width + spacing)
                next_point = [start_x_outer + segment_length, y, 0]
                lines_outer.extend([2, point_id_outer, point_id_outer + 1])
                point_id_outer += 1
                points_outer.append(next_point)
                if i != num_channels - 1:  # Vertical connecting segment
                    next_point = [start_x_outer + segment_length, y + width*2 + spacing, 0]
                    lines_outer.extend([2, point_id_outer, point_id_outer + 1])
                    point_id_outer += 1
                    points_outer.append(next_point)
            else:
                y = start_y_outer + i * spacing
                next_point = [start_x_outer, y, 0]
                lines_outer.extend([2, point_id_outer, point_id_outer + 1])
                point_id_outer += 1
                points_outer.append(next_point)
                if i != num_channels - 1:  # Vertical connecting segment
                    next_point = [start_x_outer, y * spacing, 0]
                    lines_outer.extend([2, point_id_outer, point_id_outer + 1])
                    point_id_outer += 1
                    points_outer.append(next_point)



        elif channel == 'inner':
            y = start_y_inner + i * (2*width + spacing)
            if i % 2 != 0:
                next_point = [start_x_inner + segment_length, y, 0]
                lines_inner.extend([2, point_id_inner, point_id_inner + 1])
                point_id_inner += 1
                points_inner.append(next_point)
                if i != num_channels - 1:  # Vertical connecting segment
                    next_point = [start_x_inner + segment_length, y + width*2 + spacing, 0]
                    lines_inner.extend([2, point_id_inner, point_id_inner + 1])
                    point_id_inner += 1
                    points_inner.append(next_point)
            else:
                next_point = [start_x_inner, y, 0]
                lines_inner.extend([2, point_id_inner, point_id_inner + 1])
                point_id_inner += 1
                points_inner.append(next_point)
                if i != num_channels - 1:  # Vertical connecting segment
                    next_point = [start_x_inner, y + width*2 + spacing, 0]
                    lines_inner.extend([2, point_id_inner, point_id_inner + 1])
                    point_id_inner += 1
                    points_inner.append(next_point)

channel_dict = {
    "points_outer": points_outer,
    "lines_outer": lines_outer,
    "points_inner": points_inner,
    "lines_inner": lines_inner,
    }

plotter = pv.Plotter()

for channel in ['outer', 'inner']:
    points = np.array(channel_dict[f'points_{channel}'])
    line = pv.PolyData()
    line.points = points
    line.lines = np.array(channel_dict[f'lines_{channel}'])
    
    if channel == 'inner':
        plotter.add_mesh(points, color='black')
        # plotter.add_mesh(line, color='black')

    else:
        plotter.add_mesh(points, color='red')
        plotter.add_mesh(line, color='red')

    # extrusion = line.extrude((0, 0, width))
    # extrusion = extrusion.triangulate()
    # extrusion_refined = extrusion.subdivide(5, subfilter='linear')
    # extrusion_refined.save(f'channel_{channel}.stl')

plotter.add_axes()
plotter.show()
# # Convert points_outer to numpy array
# points_outer = np.array(points_outer)
# # Create a polyline from the points_outer
# line = pv.PolyData()
# line.points = points_outer
# line.lines = np.array(lines_outer)

# # Extrude the line to create a surface mesh
# extrusion = line.extrude((0, 0, width))  # Extrude along the z-axis
# extrusion = extrusion.triangulate()
# # Refine the mesh to increase the resolution
# high_res_mesh = extrusion.subdivide(5, subfilter='linear')  # Increase the level to refine further

# # Save the high-resolution surface mesh to an STL file
# high_res_mesh.save('inner_wall.stl')

# wall2 = extrusion.translate((-width, 0, 0))

# # Plot the high-resolution extruded surface mesh
# plotter = pv.Plotter()
# plotter.add_mesh(high_res_mesh, color='lightblue')
# # plotter.add_mesh(wall2, color='lightblue')
# plotter.add_axes()

# plotter.show()
