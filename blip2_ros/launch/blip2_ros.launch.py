from launch import LaunchDescription
from launch_ros.actions import LifecycleNode, Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess
import os

def generate_launch_description():

    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Flag to enable use_sim_time'
    )

    # Get the launch configuration for use_sim_time
    use_sim_time = LaunchConfiguration('use_sim_time')

    blip2_config = os.path.join(
        get_package_share_directory("blip2_ros"),
        'config',
        'blip2_ros.yaml'
    )

    blip2_ros_node = Node(
        package="blip2_ros",
        executable='blip2_ros_node',
        name="blip2_ros",
        namespace="blip2_ros",
        output='screen',
        emulate_tty=True,
        # arguments=['--ros-args', '--log-level', 'debug'],
        parameters=[
            {'use_sim_time': use_sim_time},
            blip2_config
        ]
    )

    lcm = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_detection',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart': True,
            'bond_timeout': 0.0,
            'node_names': [
                '/blip2_ros/blip2_ros'
            ]
        }]
    )

    ld = LaunchDescription()
    ld.add_action(sim_time_arg)
    ld.add_action(blip2_ros_node)
    ld.add_action(lcm)
    return ld
