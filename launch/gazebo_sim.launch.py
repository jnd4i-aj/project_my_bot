import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    ld = LaunchDescription()

    package_name = 'project_my_bot'

    display_launch_file_path = os.path.join(get_package_share_directory(package_name), 'launch', 'display.launch.py')

    display_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(display_launch_file_path))
    
    gazebo_world_arg = DeclareLaunchArgument(
        'world', 
        default_value=os.path.join(get_package_share_directory(package_name), 'worlds', 'obstacles.world'),
        description='Gazebo world file'
    )

    gazebo_launch_file_path = os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')


    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file_path),
        launch_arguments={'world': LaunchConfiguration('world')}.items()
    )
    
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=['-entity', 'my_autonomous_bot', '-topic', '/robot_description']
    )

    ld.add_action(gazebo_world_arg)
    ld.add_action(gazebo_launch)
    ld.add_action(spawn_robot)
    ld.add_action(display_launch)

    return ld
