# PyQt ROS2 App 
This package is a topic visualization application with pyqt5 and ROS2.

## Environment
- Linux OS
    - Ubuntu 22.04 Laptop PC
- ROS
    - Foxy Fitzroy

## Install & Build
The following commands download a package from a remote repository and install it in your colcon workspace.

```shell
pip3 install pyqt5
```

```shell
git clone https://github.com/tasada038/pyqt_ros2_app.git
```

## Usage
Open two shells. In the first shell,run the pyqt application program
```shell
python3 main_pyqt_ros2.py
```

In the second shell, run the ros2 test node program:
```shell
ros2 run demo_nodes_cpp talker_loaned_message
```

After entering "/chatter_pod" in "Topic Changed", press the Enter key to reflect.
Check the "ROS2 Connection" and "Float64 msg" checkboxes to see how the application works.

## License
This repository is licensed under the Apache 2.0, see LICENSE for details.
