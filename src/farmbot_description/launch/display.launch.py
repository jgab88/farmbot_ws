from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
import xacro
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Check if use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    share_dir = get_package_share_directory('farmbot_description')
    pkg_path = os.path.join(get_package_share_directory('farmbot_description'))
    xacro_file = os.path.join(share_dir, 'urdf', 'farmbot.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    rviz_config_file = os.path.join(share_dir, 'config', 'display.rviz')

    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='False'
    )

    #show_gui = LaunchConfiguration('gui')
    
    #robot_state_publisher - create
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time':
    use_sim_time}
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[params,
            {'robot_description': robot_urdf}
        ]
        
    )

    joint_state_publisher_node = Node(
    #    condition=UnlessCondition(show_gui),
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

#    joint_state_publisher_gui_node = Node(
#        condition=IfCondition(show_gui),
#        package='joint_state_publisher_gui',
#        executable='joint_state_publisher_gui',
#        name='joint_state_publisher_gui'
#    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use sim time if true'),
        gui_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
#        joint_state_publisher_gui_node,
        rviz_node
    ])
