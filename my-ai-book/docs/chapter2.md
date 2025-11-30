---
id: chapter2
title: Chapter 2 — The Digital Twin (Gazebo Simulation)
sidebar_label: Chapter 2 — The Digital Twin (Gazebo Simulation)
---

# **Chapter 2 — The Digital Twin (Gazebo Simulation)**

---

## **2.1 Physics Simulation: Gravity, Collisions, and URDF**

```md
---
id: gazebo-physics
title: 2.1 Physics Simulation
---
```

### **Why Physics Simulation Matters**

Before deploying to a real robot, we must test behaviours in a safe environment.
A **Digital Twin** of the robot provides:

* Accurate physics
* Collision detection
* Sensor replication
* Virtual testing of AI agents
* High-speed debugging without hardware damage

Gazebo (Ignition Gazebo) is the primary simulation environment used with ROS 2.

### **Physics Concepts**

#### **Gravity**

Gazebo models gravitational acceleration, typically:

```
-9.81 m/s² on the Z-axis
```

Robots must compensate for gravity when lifting arms or balancing.

#### **Collisions**

Every model includes a *collision mesh* used for:

* Obstacles
* Robot arms
* Wheels
* Tools

Gazebo’s physics engine resolves:

* Contact points
* Bounce
* Sliding
* Friction coefficients

#### **URDF: Unified Robot Description Format**

Robot models in ROS 2 are usually written in **URDF**, an XML-based format describing:

* Links (rigid bodies)
* Joints (how links connect)
* Sensors
* Collision geometry
* Visual appearance
* Inertial parameters

Simple URDF snippet:

```xml
<link name="base">
  <inertial>
    <mass value="1.0"/>
    <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
  </inertial>
  <visual>
    <geometry>
      <box size="0.5 0.5 0.2"/>
    </geometry>
  </visual>
</link>
```

URDF files are the blueprint of the robot in both simulation and hardware.

---

## **2.2 Simulating Sensors: LiDAR and Depth Cameras**

```md
---
id: gazebo-sensors
title: 2.2 Simulating Sensors
---
```

Robots depend heavily on sensors for perception. Gazebo provides accurate simulation of:

* Laser scanners
* Depth cameras
* IMUs
* GPS
* Force/torque sensors

### **Simulated LiDAR**

Simulated LiDAR works by emitting virtual rays around the robot and computing distances.

Properties:

* Angular resolution
* Minimum and maximum range
* Number of beams
* Noise profiles

Typical use: navigation and object avoidance

URDF example:

```xml
<sensor name="lidar" type="gpu_laser">
  <update_rate>30</update_rate>
  <ray>
    <scan>
      <horizontal>
        <samples>360</samples>
        <resolution>1</resolution>
      </horizontal>
    </scan>
  </ray>
</sensor>
```

### **Depth Cameras**

Depth cameras generate:

* RGB images
* Depth maps (per-pixel distance)

Used for:

* 3D mapping
* Object detection
* Grasp planning

Example:

```xml
<sensor name="depth_camera" type="depth_camera">
  <update_rate>30</update_rate>
  <camera>
    <horizontal_fov>1.05</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
    </image>
  </camera>
</sensor>
```

These sensors publish ROS 2 topics such as:

* `/camera/image_raw`
* `/camera/depth/image_raw`
* `/scan`

This symmetry allows AI agents to use simulated and real sensors interchangeably.

---

## **2.3 Environment Building: Creating Worlds in Gazebo**

```md
---
id: gazebo-environments
title: 2.3 Environment Building
---
```

A robot is only as capable as the environment it is tested in.
Gazebo “worlds” define everything surrounding the robot.

### **Elements of a Gazebo World**

* Ground plane
* Light sources
* Walls, obstacles, furniture
* Terrain (sand, grass, concrete)
* Other robots
* Human avatars
* Weather and ambient lighting

Worlds are described using **SDF (Simulation Description Format)**.

### **Example: A Simple World File**

```xml
<world name="test_world">
  <gravity>0 0 -9.81</gravity>

  <include>
    <uri>model://ground_plane</uri>
  </include>

  <model name="box_obstacle">
    <static>true</static>
    <link name="box">
      <visual>
        <geometry>
          <box size="1 1 1"/>
        </geometry>
      </visual>
    </link>
  </model>

  <light type="directional" name="sun">
    <direction>-0.5 -0.2 -1</direction>
  </light>
</world>
```

### **Environment Design Workflow**

1. Start with an empty world
2. Add floor and lighting
3. Place obstacles and interactive objects
4. Import the robot URDF
5. Connect Gazebo to ROS 2 using `ros_gz_bridge`
6. Spawn the robot into the world
7. Run navigation, manipulation, and AI experiments

Well-designed environments allow researchers to test:

* Grasping
* Navigation
* Social robotics
* Human-robot interaction
* Hazard handling

before deploying on real hardware.