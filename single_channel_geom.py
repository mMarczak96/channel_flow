import pyvista as pv
import numpy as np
import os
from subprocess import PIPE, run
# Global variables
cwd = os.getcwd()
# Functions 
def run_cmd(command : str):
    """
    run a command and return its output
    """
    return run(
        command, 
        stdout=PIPE, 
        stderr=PIPE, 
        universal_newlines=True, 
        shell=True
    )

def nameSTLpart(name: str, path: str):
    nameStart = f'sed -i "/solid Visualization Toolkit generated SLA File/c solid {name} " {path}'

    return nameStart

def nameSTLpartEnd(name: str, path: str):
    nameEnd = f'sed -i "/endsolid/c endsolid {name} " {path}'

    return nameEnd

def create_lines(points: list, lines: list):
    for point_id in range(len(points)):
        lines.append([2, point_id, point_id + 1])
    return lines


def single_channel_geometry(num_channels: int, length: float, spacing: float, width: float, geom_dir=f'{cwd}/geometry', plot=False):
    # Initial parameters (also can be modified if needed)
    step = 3 * width + spacing
    start_x_right, start_y_right, start_z_right = width, 0, 0
    start_x_left, start_y_left, start_z_left = 0, -width - spacing, 0
    # Points calcualtion
    point_0_right = [start_x_right, start_y_right, start_z_right] 
    point_1_right = [start_x_right, start_y_right + width, start_z_right ]  
    point_2_right = [start_x_right + length, start_y_right + width, start_z_right] 
    point_3_right = [start_x_right + length, start_y_right + step, start_z_right] 

    point_0_left = [start_x_left, start_y_left, start_z_left] 
    point_1_left = [start_x_left, start_y_left + step, start_z_left]
    point_2_left = [start_x_left + length, start_y_left + step, start_z_left]
    point_3_left = [start_x_left + length, start_y_left + step + spacing, start_z_left]

    right_wall_points, right_wall_lines = [], []
    left_wall_points, left_wall_lines = [], []

    for c in range(num_channels):

        new_right_point_0 = [point_0_right[0], point_0_right[1] + step * c, point_0_right[2]]
        new_right_point_1 = [point_1_right[0], point_1_right[1] + step * c, point_1_right[2]]
        new_right_point_2 = [point_2_right[0], point_2_right[1] + step * c, point_2_right[2]]
        new_right_point_3 = [point_3_right[0], point_3_right[1] + step * c, point_3_right[2]]

        right_wall_points.append(new_right_point_0)
        right_wall_points.append(new_right_point_1)
        right_wall_points.append(new_right_point_2)
        right_wall_points.append(new_right_point_3)

        new_left_point_0 = [point_0_left[0], point_0_left[1] + step * c + spacing, point_0_left[2]]
        new_left_point_1 = [point_1_left[0], point_1_left[1] + step * c, point_1_left[2]]
        new_left_point_2 = [point_2_left[0], point_2_left[1] + step * c, point_2_left[2]]
        new_left_point_3 = [point_3_left[0], point_3_left[1] + step * c, point_3_left[2]]

        left_wall_points.append(new_left_point_0)
        left_wall_points.append(new_left_point_1)
        left_wall_points.append(new_left_point_2)
        left_wall_points.append(new_left_point_3)
    # Final point maniulations
    left_wall_points[0] = [start_x_left, 0, start_z_left] # Cutting left channel inlet edge
    # Right channel outlet
    pre_exit_right_point = [start_x_right, right_wall_points[-1][1], start_z_right]
    exit_right_point = [start_x_right, right_wall_points[-1][1] + width, start_z_right]
    right_wall_points.append(pre_exit_right_point)
    right_wall_points.append(exit_right_point)
    # Left channel outlet
    pre_exit_left_point = [start_x_left, left_wall_points[-1][1], start_z_left]
    exit_left_point = [start_x_left, left_wall_points[-1][1] + 2 * width, start_z_left]
    left_wall_points.append(pre_exit_left_point)
    left_wall_points.append(exit_left_point)
    # Lines calculations
    for point_id in range(len(right_wall_points)):
        right_wall_lines.append([2, point_id, point_id + 1])

    for point_id in range(len(left_wall_points)):
        left_wall_lines.append([2, point_id, point_id + 1])
    # Mesh generation
    # Right Wall
    right_mesh = pv.PolyData(right_wall_points)
    right_mesh.points = np.array(right_wall_points)
    right_mesh.lines = np.array(right_wall_lines[:-1])
    right_extrusion = right_mesh.extrude((0, 0, width)) 
    right_extrusion = right_extrusion.triangulate()
    right_extrusion = right_extrusion.subdivide(5, subfilter='linear')  
    # Left wall
    left_mesh = pv.PolyData(left_wall_points)
    left_mesh.points = np.array(left_wall_points)
    left_mesh.lines = np.array(left_wall_lines[:-1])
    left_extrusion = left_mesh.extrude((0, 0, width)) 
    left_extrusion = left_extrusion.triangulate()
    left_extrusion = left_extrusion.subdivide(5, subfilter='linear')  
    # Bottom wall
    inlet_line = pv.Line(right_wall_points[0], left_wall_points[0])
    inlet_line_extrusion = inlet_line.extrude([0, width, 0])

    inlet_line_extrusion_moved_1 = inlet_line_extrusion.translate([0, width,0 ])

    channel_line = pv.Line(right_wall_points[1], [right_wall_points[1][0], right_wall_points[1][0] + width, right_wall_points[1][2]])
    channel_line_extrusion = channel_line.extrude([length - width, 0, 0])

    inlet_line_extrusion_moved_2 = inlet_line_extrusion.translate([length, width,0 ])

    inlet_line_extrusion_spacing = inlet_line.extrude([0, spacing, 0])
    inlet_line_extrusion_spacing_moved = inlet_line_extrusion_spacing.translate([length, 2 * width, 0])

    inlet_line_extrusion_moved_3 = inlet_line_extrusion.translate([length, 2 * width + spacing, 0 ])

    channel_line_extrusion_moved = channel_line_extrusion.translate([0, spacing + width, 0])

    inlet_line_extrusion_moved_4 = inlet_line_extrusion.translate([0, 2 * width + spacing, 0 ])

    inlet_line_extrusion_moved_5 = inlet_line_extrusion.translate([0, num_channels * step , 0 ])

    bottom_wall_surfaces_list = [
        inlet_line_extrusion, 
        inlet_line_extrusion_moved_1,
        channel_line_extrusion, 
        inlet_line_extrusion_moved_2,
        inlet_line_extrusion_spacing_moved,
        inlet_line_extrusion_moved_3,
        channel_line_extrusion_moved,
        inlet_line_extrusion_moved_4
        ]

    bottom_wall = pv.PolyData()
    for surface in bottom_wall_surfaces_list:
        bottom_wall = bottom_wall.merge(surface)

    bottom_wall_total = pv.PolyData()
    for c in range(num_channels):
        bottom_wall_moved = bottom_wall.translate([0, c * step, 0])
        bottom_wall_total = bottom_wall_total.merge(bottom_wall_moved)

    bottom_wall_total = bottom_wall_total.merge(inlet_line_extrusion_moved_5)

    bottom_wall_total = bottom_wall_total.triangulate()
    bottom_wall_total = bottom_wall_total.subdivide(3, subfilter='linear')
    # Upper wall
    upper_wall = bottom_wall_total.translate([0, 0, width])
    # Inlet 
    inlet = inlet_line.extrude([0, 0, width])
    inlet = inlet.triangulate()
    inlet = inlet.subdivide(5, subfilter='linear')  
    # Outlet
    outlet = inlet.translate([0, num_channels * step + width, 0])
    # Saving separate patches
    patch_dict = {
        'right_wall': right_extrusion, 
        'left_wall': left_extrusion, 
        'bottom_wall': bottom_wall_total, 
        'upper_wall': upper_wall, 
        'inlet': inlet, 
        'outlet': outlet}
    
    for name, item in patch_dict.items():
        item.save(f'{geom_dir}/{name}.stl', binary=False)
        run_cmd(nameSTLpart(name, f'{geom_dir}/{name}.stl'))
        run_cmd(nameSTLpartEnd(name, f'{geom_dir}/{name}.stl'))
        
    # Saving as a one .stl file
    channel_file = 'single_channel.stl'
    if os.path.isfile(channel_file):
        run_cmd(f'rm {channel_file}')
    else: 
        run_cmd(f'touch {channel_file}')
    
    for patch, item in patch_dict.items():
        fPatch = open(f'{geom_dir}/{patch}.stl', 'r')
        dPatch = fPatch.read()
        fPatch.close()
        fChannel = open(f'{geom_dir}/single_channel.stl', 'a')
        fChannel.write(dPatch)
        fChannel.close()

    # Optional Plotting
    if plot == True:
        plotter = pv.Plotter()
        plotter.add_mesh(right_extrusion, show_edges=True, color='blue')
        plotter.add_mesh(left_extrusion, show_edges=True, color='red')
        plotter.add_mesh(bottom_wall_total, show_edges=True, color='grey')
        plotter.add_mesh(upper_wall, show_edges=True, color='white')
        plotter.add_mesh(outlet, show_edges=True, color='yellow')
        plotter.add_mesh(inlet, show_edges=True, color='green')
        plotter.add_axes()
        plotter.show()


################################################ MAIN PROGRAM ################################################

# Initial parameters
num_channels = 2 # Creates geometry with number of channels equal to: 2 * num_channels 
length = 50  
spacing = 1 
width = 2  

single_channel_geometry(num_channels, length, spacing, width, plot=True)
