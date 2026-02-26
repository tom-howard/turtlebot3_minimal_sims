#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription, 
    DeclareLaunchArgument,
    TimerAction,
    LogInfo
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition

def generate_launch_description():

    gz_ros = os.path.join(
        get_package_share_directory('ros_gz_sim'), 'launch'
    )
    world = os.path.join(
        get_package_share_directory('turtlebot3_minimal_sims'), 'worlds', 'empty.world'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    with_gui_arg = DeclareLaunchArgument(
        'with_gui', 
        description="Select whether to launch Gazebo with or without Gazebo Client (i.e. the GUI).",
        default_value='false'
    )
    x_pose_arg = DeclareLaunchArgument(
        'x_pose',
        description='Starting X-position of the robot',
        default_value='0.0'
    )
    y_pose_arg = DeclareLaunchArgument(
        'y_pose',
        description='Starting Y-position of the robot',
        default_value='0.0'
    )
    yaw_arg = DeclareLaunchArgument(
        'yaw',
        description='Starting orientation of the robot (radians)',
        default_value='0.0'
    )
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    with_gui = LaunchConfiguration('with_gui')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    yaw = LaunchConfiguration('yaw')

    gz_srvr_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gz_ros,
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': ['-r -s -v2 ', world], 'on_exit_shutdown': 'true'
        }.items()
    )

    gz_gui_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gz_ros,
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-g -v2 '
        }.items(),
        condition=IfCondition(with_gui)
    )

    tb3_state_publisher_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('turtlebot3_gazebo'), 
                'launch',
                'robot_state_publisher.launch.py'
            )
        ),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    spawn_tb3_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('turtlebot3_minimal_sims'), 
                'launch', 
                'spawn_tb3.launch.py'
            )
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose,
            'yaw': yaw
        }.items()
    )

    launch_desc = LaunchDescription()

    # launch args
    launch_desc.add_action(use_sim_time_arg)
    launch_desc.add_action(with_gui_arg)
    launch_desc.add_action(x_pose_arg)
    launch_desc.add_action(y_pose_arg)
    launch_desc.add_action(yaw_arg)

    # launchj actions
    launch_desc.add_action(gz_srvr_launch)
    launch_desc.add_action(gz_gui_launch)
    launch_desc.add_action(tb3_state_publisher_launch)
    launch_desc.add_action(spawn_tb3_launch)
    launch_desc.add_action(TimerAction(
        period=5.0,
        actions=[
            LogInfo(msg="\nA TurtleBot3 Waffle simulation has been launched 'headless' (i.e. no GUI will be presented).\nKey nodes and topics should now be available for interrogation from a separate terminal.")
        ]
    ))
    return launch_desc 
    