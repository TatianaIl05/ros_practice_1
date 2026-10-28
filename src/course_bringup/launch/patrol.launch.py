from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'namespace',
            default_value='robot_a',
            description='namespace для системы'
        ),
        DeclareLaunchArgument(
            'record',
            default_value='false',
            description='запускать ли recorder'
        ),
        DeclareLaunchArgument(
            'bag_dir',
            default_value='evidence/pr05/bag',
            description='куда писать bag'
        ),
        DeclareLaunchArgument(
            'subscriber_reliability',
            default_value='reliable',
            description='Qos подписчика'
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            output='screen'
        ),
        Node(
            package='patrol',
            executable='patrol',
            namespace=LaunchConfiguration('namespace'),
            remappings=[('cmd_vel', '/turtle1/cmd_vel')],
            output='screen'
        ),
        Node(
            package='course_bringup',
            executable='pose_relay',
            namespace=LaunchConfiguration('namespace'),
            output='screen'
        ),
        ExecuteProcess(
            cmd=[
                'ros2', 'bag', 'record', '-s', 'mcap',
                '-o', LaunchConfiguration('bag_dir'),
                '--topics', '/robot_a/sensor_pose',
            ],
            condition=IfCondition(LaunchConfiguration('record')),
            output='screen',
        )
    ])
