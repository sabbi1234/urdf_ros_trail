import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'roscontrol'
    file_subpath = 'urdf_description/example_robot.urdf.xacro'
    rviz_path = 'urdf_description/config.rviz'

    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    rviz_file = os.path.join(get_package_share_directory(pkg_name),rviz_path)
    print(rviz_file)

    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}] # add other parameters here if required
    )
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen', # You can change 'screen' to 'log' if you prefer logging
        arguments=['-d', rviz_file]  # Path to your RViz config file
    )

    gazebo_node = Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'diffdrive', '-topic', 'robot_description'],
            output='screen')
    
    gazebo_exute = ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so',  '-world', '/usr/share/gazebo-11/worlds/empty.world'], output='screen')

    sim = DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true')

    # Run the node
    return LaunchDescription([
        node_robot_state_publisher,rviz_node,sim,gazebo_node,gazebo_exute
    ])