import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    ld = LaunchDescription()

    package_name = 'project_my_bot'

    display_launch_file_path = os.path.join(get_package_share_directory(package_name), 'launch', 'display.launch.py')

    display_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(display_launch_file_path),
        launch_arguments={'use_sim_time': 'true'}.items())
    
    gazebo_launch_file_path = os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file_path))
    
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=['-entity', 'my_autonomous_bot', '-topic', '/robot_description']
    )

    # gazebo_world_arg = DeclareLaunchArgument(
    #     'world', 
    #     default_value=os.path.join(get_package_share_directory('robot_description'), 'worlds', 'house_1.world'),
    #     description='Gazebo world file'
    # )

    ld.add_action(gazebo_launch)
    ld.add_action(spawn_robot)
    ld.add_action(display_launch)

    return ld
