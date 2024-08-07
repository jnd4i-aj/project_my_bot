import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_path

def generate_launch_description():
    ld = LaunchDescription()
    urdf_path = os.path.join(get_package_share_path('project_my_bot'),
                             'urdf','main.xacro')

    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description
            }]
            )
    
    joint_state_pub = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
            )

    rviz_config_path = os.path.join(get_package_share_path('project_my_bot'),
                                    'config', 'display.rviz')

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
        )
    
    ld.add_action(robot_state_pub)
    ld.add_action(joint_state_pub)
    ld.add_action(rviz)

    return ld
