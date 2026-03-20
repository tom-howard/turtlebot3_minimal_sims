# turtlebot3_minimal_sims

Very basic simulations for a TurtleBot3 Waffle.

Currently includes:

1. A "headless" simulation (i.e. no graphical user interface)
    
    ```bash
    ros2 launch turtlebot3_minimal_sims headless.launch.py
    ```

1. Nothing else, for now...

## Installing

Install this like any other ROS 2 package:

```bash
cd ~/ros2_ws/src/
```

```bash
git clone https://github.com/tom-howard/turtlebot3_minimal_sims.git
```

```bash
cd ~/ros2_ws/ && colcon build --packages-select turtlebot3_minimal_sims && source ~/.bashrc
```

Run with `ros2 launch` as above.