# RMF Demos

![](https://github.com/open-rmf/rmf_demos/workflows/build/badge.svg)
![](https://github.com/open-rmf/rmf_demos/workflows/style/badge.svg)

The Open Robotics Middleware Framework (Open-RMF) enables interoperability among heterogeneous robot fleets while managing robot traffic that share resources such as space, building infrastructure systems (lifts, doors, etc) and other automation systems within the same facility. Open-RMF also handles task allocation and conflict resolution  among its participants (de-conflicting traffic lanes and other resources). These capabilities are provided by various libraries in [Open-RMF](https://github.com/open-rmf/rmf).
For more details about Open RMF, refer to the comprehensive documentation provided [here](https://osrf.github.io/ros2multirobotbook/intro.html).

This repository contains demonstrations of the above mentioned capabilities of RMF. It serves as a starting point for working and integrating with Open-RMF.

You can also find a nice demonstration of Open-RMF using `Nav2` and `MoveIt!` built into the [Ionic Release Demo](https://github.com/gazebosim/ionic_demo).

[![Robotics Middleware Framework](../media/thumbnail.png?raw=true)](https://vimeo.com/405803151)

#### (Click to watch video)

## System Requirements

These demos were built and tested on

* [Ubuntu 24.04 LTS](https://releases.ubuntu.com/24.04/)

* [ROS 2 - Kilted](https://docs.ros.org/en/jazzy/Releases/Release-Kilted-Kaiju.html)

* [Gazebo Ionic](https://gazebosim.org/docs/ionic)
> Note: The `main` branches of the core RMF libraries are fully supported on ROS 2 Humble, Iron, and Jazzy as well, but you will need to use the distro-specific branches for `rmf_traffic_editor` and `rmf_simulation`.
>

## LAUNCHING TEST1 

1. First off, navigate to the repository where you've cloned the respository. In my case, the route is this:

```bash
maria@maria:~$ cd Documentos/GitHub/IR2134/
```
2. After being inside the desired directoty, we have to start the Docker container. Depending on the Grpahics Card that you have in you pc, you may have to adapt this command. In my case, the command is this one: 

```bash 
 rocker --nvidia --x11 --name traffic-editor --user \
  --volume /home/maria/Documentos/GitHub/IR2134/rmf_ws:/home/maria/rmf_ws -- \
  ghcr.io/open-rmf/rmf/rmf_demos:jazzy-rmf-latest \
   bash 
```

3. Once in the Docker, move to the folder where you have your workspace. In my case: 
```bash 
  maria@624a8113b68f:~$ cd rmf_ws/
```

4. Now, compile the porject. To do so, use this command: 
 ```
colcon build 
```

5. After this, source the environmnet: 
```
source install/setup.bash
```
6. Before launching the simulaton, to make sure that you don't have any problems with Gazebo, I recommend you write this in the terminal were you've put the other instructions:
```
export LIBGL_ALWAYS_SOFTWARE=1
```

To launch the simulation, use this command: 
```
ros2 launch project_simulation test1.launch.xml server_uri:="ws://localhost:8000/_internal"
```
Now, Gazebo and Rviz should have opened. In Gazebo you should be ale to see the world and the TinyRobot. In Rviz (which I have not been able to open in this simulation), should show where the robot is located and the graphs. 

![Foto Gazebo y Rviz](/home/maria/Documentos/GitHub/IR2134/rmf_ws/src/project/project_assets/fotos_readme/foto1.png)

![Foto Gazebo](/home/maria/Documentos/GitHub/IR2134/rmf_ws/src/project/project_assets/fotos_readme/foto2.png)

To execute tasks, you must open the RMF-WEB. To do so, execute this command in a new terminal (without closing the previous one) for the API Server
```
docker run --network host -it \
  -e ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST \
  -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp \
	ghcr.io/open-rmf/rmf-web/api-server:jazzy-nightly
```
On a third terminal, write this to open the RMF- WEB dashborad:
```
docker run --network host -it \
  -e RMF_SERVER_URL=http://localhost:8000 \
  -e TRAJECTORY_SERVER_URL=ws://localhost:8006 \
  ghcr.io/open-rmf/rmf-web/dashboard
```

Now, online open the RMF-WEB: 
```
localhost::3000
```
There, you cand add tasks 
![Foto terminal y RMF-Web](/home/maria/Documentos/GitHub/IR2134/rmf_ws/src/project/project_assets/fotos_readme/foto3.png)



## LAUNCHING ICC_KYOTO 
In my project, this world is called "classroom". 
If you have closed the previous terminals, you must re-do steps from 1 to 6. 
Once all of that is done, launch the simulation with this command: 
```
ros2 launch project_simulation classroom.launch.xml server_uri:="ws://localhost:8000/_internal"
```
![Gazebo y Rviz](/home/maria/Documentos/GitHub/IR2134/rmf_ws/src/project/project_assets/fotos_readme/foto4.png)

![Gazebo](/home/maria/Documentos/GitHub/IR2134/rmf_ws/src/project/project_assets/fotos_readme/foto5.png)

Now on a second terminal for the API Server: 
```
docker run --network host -it \
  -e ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST \
  -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp \
	ghcr.io/open-rmf/rmf-web/api-server:jazzy-nightly
```
On a third terminal, write this to open the RMF- WEB dashborad:
```
docker run --network host -it \
  -e RMF_SERVER_URL=http://localhost:8000 \
  -e TRAJECTORY_SERVER_URL=ws://localhost:8006 \
  ghcr.io/open-rmf/rmf-web/dashboard
```

Now, online open the RMF-WEB: 
```
localhost::3000
```
There, you cand add tasks 
![Gazebo](/home/maria/Documentos/GitHub/IR2134/rmf_ws/src/project/project_assets/fotos_readme/foto6.png)


## NOTES 
- I can't open Rviz for test1 and I don't know the reason why. 
- I can't open RMF-Web. The command shown on the slides to open de dashboard is not working on my pc so I adjusted it. The one in the slides gives me this error: 

![Foto error](/home/maria/Documentos/GitHub/IR2134/rmf_ws/src/project/project_assets/fotos_readme/foto7.png)
The only thing I had left to fully complete the proyect is to send tasks. 








