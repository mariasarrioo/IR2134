# First Project with Open-RMF

This project contains an Open-RMF simulation of the **ICC Kyoto** environment using **two TinyRobot robots** inside the **same navigation graph**.

The system is organized so that each robot is mainly associated with a specific task type:

- **tinyRobot1** is used for **patrol tasks**
- **tinyRobot2** is used for **cleaning tasks**

Even though both robots are the same model and can technically do the same thing, they are separated by task purpose in this project.

---

## System Requirements

This project was developed and tested with:

- **Ubuntu 24.04**
- **ROS 2 Jazzy**
- **Open-RMF demos container**
- **Gazebo**
- **RViz**
- **RMF Web**

---

## Project Location

The ROS 2 workspace is located at:

```bash
/home/maria/Documentos/GitHub/IR2134/rmf_ws
```

The package used in this project is:

```bash
first_project
```

---

## Project Overview

This project simulates the **ICC Kyoto** world with two TinyRobot robots:

* **tinyRobot1**
* **tinyRobot2**

Both robots belong to the same map and the same navigation graph, but they are used with different task naming conventions:

* **Patrol task points** are named as:

```text
patrolx_n
```

* **Cleaning task points** are named as:

```text
cleaningx_n
```

Where:

* `x` is the **zone number** or **room number**
* `n` is the **vertex number** inside that zone

### Example

If the first patrol area is a room with four patrol vertices, they should be named like this:

```text
patrol1_1
patrol1_2
patrol1_3
patrol1_4
```

If the second cleaning area is another room with four cleaning vertices, they could be named like this:

```text
cleaning2_1
cleaning2_2
cleaning2_3
cleaning2_4
```

This naming system makes it easy to identify which vertices belong to the same room or task area.

---

## Launching the Simulation

### 1. Go to the repository folder

First, open a terminal on your PC and move to the project directory:

```bash
cd /home/maria/Documentos/GitHub/IR2134
```

---

### 2. Start the Open-RMF container

Run the following command:

```bash
docker rm -f first_project_rmf 2>/dev/null

rocker \
  --env __NV_PRIME_RENDER_OFFLOAD=1 \
  --env __GLX_VENDOR_LIBRARY_NAME=nvidia \
  --nvidia \
  --x11 \
  --name first_project_rmf \
  -e ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST \
  --network host \
  --user \
  --volume /home/maria/Documentos/GitHub/IR2134/rmf_ws:/home/maria/rmf_ws \
  -- \
  ghcr.io/open-rmf/rmf/rmf_demos:jazzy-rmf-latest \
  bash
```

This opens the Open-RMF Docker container with access to the local ROS 2 workspace.

---

### 3. Build the workspace

Inside the container, run:

```bash
cd ~/rmf_ws
source /opt/ros/jazzy/setup.bash
sudo cp -R /root/.gazebo .
colcon build --packages-select first_project --symlink-install
source install/setup.bash
export LIBGL_ALWAYS_SOFTWARE=1
```

Explanation:

* `source /opt/ros/jazzy/setup.bash` loads the ROS 2 environment
* `sudo cp -R /root/.gazebo .` copies Gazebo configuration files
* `colcon build --packages-select first_project --symlink-install` builds the package
* `source install/setup.bash` sources the built workspace
* `export LIBGL_ALWAYS_SOFTWARE=1` helps avoid graphics issues in Gazebo and RViz

---

### 4. Launch the ICC Kyoto world

Still inside the container, run:

```bash
ros2 launch first_project icc_kyoto.launch.xml server_uri:="ws://localhost:8000/_internal"
```

When the launch works correctly, the following should open:

* **Gazebo**, showing the ICC Kyoto world and the robots
* **RViz**, showing the map, graphs, and robot information

---

## Launching RMF Web

To send tasks through the RMF Web interface, keep the simulation terminal open and use two additional terminals on your PC.

---

### 5. Launch the API Server

In a second terminal, run:

```bash
docker run --network host -it \
  -e ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST \
  -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp \
  ghcr.io/open-rmf/rmf-web/api-server:jazzy-nightly
```

---

### 6. Launch the RMF Web Dashboard

In a third terminal, run:

```bash
docker run --network host --rm -it \
  -e RMF_SERVER_URL=http://localhost:8000 \
  -e TRAJECTORY_SERVER_URL=ws://localhost:8006 \
  ghcr.io/open-rmf/rmf-web/demo-dashboard:jazzy-nightly
```

Then open this address in your browser:

```
http://localhost:3000/
```

From there, the RMF Web dashboard should display the map, doors, robots, and available tasks.

---

## Robot Configuration in Traffic Editor

The robots are spawned from charger vertices in Traffic Editor.

### Example for `tinyRobot1`

```yaml
name: tinyRobot1_charger
is_charger: true
is_parking_spot: true
spawn_robot_name: tinyRobot1
spawn_robot_type: TinyRobot
```

### Example for `tinyRobot2`

```yaml
name: tinyRobot2_charger
is_charger: true
is_parking_spot: true
spawn_robot_name: tinyRobot2
spawn_robot_type: TinyRobot
```

These vertices are the robot spawn points and charging points.

---

## Vertex Naming Convention for Tasks

### Patrol vertices

Patrol points are named using:

```text
patrolx_n
```

Example for patrol area 1:

```text
patrol1_1
patrol1_2
patrol1_3
patrol1_4
```

These vertices usually define the corners or important points of a patrol route inside the same room.

### Cleaning vertices

Cleaning points are named using:

```text
cleaningx_n
```

Example for cleaning area 2:

```text
cleaning2_1
cleaning2_2
cleaning2_3
cleaning2_4
```

These vertices belong to the same cleaning zone or room.

---

## Task Logic Used in This Project

This project separates tasks into two robot roles:

### tinyRobot1

* Main task type: **Patrol**
* Patrol routes are defined using vertices named:

```text
patrolx_n
```

Example:

```text
patrol1_1
patrol1_2
patrol1_3
patrol1_4
```

### tinyRobot2

* Main task type: **Cleaning**
* Cleaning areas are defined using vertices named:

```text
cleaningx_n
```

Example:

```text
cleaning1_1
cleaning1_2
cleaning1_3
cleaning1_4
```

Although the project assigns patrol to `tinyRobot1` and cleaning to `tinyRobot2`, both robots are the same TinyRobot model and can move through the environment in the same way.

---

## Important Notes About Traffic Editor

* All vertices used for tasks must be properly connected by lanes
* If a task point is disconnected from the graph, the robot will not be able to reach it
* Charger vertices must include the correct robot spawn properties
* Vertex names must be written exactly as expected in the task setup
* After any change in Traffic Editor, the project must be rebuilt

---

## Rebuilding After Changes

If you modify the map, the graph, or the vertex properties in Traffic Editor, rebuild the package again.

Inside the container:

```bash
cd ~/rmf_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select first_project --symlink-install
source install/setup.bash
```

---

## Troubleshooting

### Gazebo or RViz does not open correctly

Make sure you ran:

```bash
export LIBGL_ALWAYS_SOFTWARE=1
```

### The container name already exists

Remove it and launch it again:

```bash
docker rm -f first_project_rmf
```

### RMF Web does not show the robots

Make sure that:

* the simulation is still running
* the API server is running
* the dashboard is running
* the robots have correct spawn vertices in Traffic Editor
* the graph is connected
* the workspace has been rebuilt after editing the map

---

## Summary

This project simulates the **ICC Kyoto** environment in Open-RMF with two TinyRobot robots in the same graph:

* **tinyRobot1** → patrol robot
* **tinyRobot2** → cleaning robot

The task areas follow these naming conventions:

* **Patrol** → `patrolx_n`
* **Cleaning** → `cleaningx_n`

Where:

* `x` identifies the room or area
* `n` identifies the vertex inside that room

This structure makes it easier to organize tasks room by room while keeping the project simple and easy to understand.
