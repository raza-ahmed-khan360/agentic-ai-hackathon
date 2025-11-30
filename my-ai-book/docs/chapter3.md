---
id: chapter3
title: Chapter 3 — Sensors and the Perception Stack
sidebar_label: Chapter 3 — Sensors and the Perception Stack
---

# **Chapter 3 — Sensors and the Perception Stack**

Robots require accurate awareness of their surroundings to behave intelligently in the physical world. Perception provides the foundation for localisation, navigation, manipulation, and high-level decision-making. This chapter explores the structure of the perception pipeline and how ROS 2 integrates data from multiple sensors.

## 3.1 The Role of Perception in Physical AI

Perception converts raw sensor readings into meaningful information. While raw data may include pixel intensities or ranges from a laser scanner, perception transforms these into actionable outputs:

* The robot’s position in the world
* The 3D layout of the environment
* Object identities and locations
* Human pose and gesture
* Contact forces and surface properties

Unlike digital AI, which processes perfect images, physical robots must interpret noisy, incomplete, and ambiguous sensory data. This makes filtering, fusion, and probabilistic reasoning essential.

## 3.2 Core Robotic Sensors

Robots commonly use a mixture of the following sensors:

### Cameras (RGB and Depth)

Cameras provide rich information but require significant compute for processing. Depth cameras (structured light, stereo, or Time-of-Flight) add per-pixel distance measurement, essential for grasping and 3D mapping.

### LiDAR

LiDAR provides accurate range measurements with high angular precision, making it ideal for mapping and navigation. Modern multi-layer LiDARs give dense 3D pointclouds.

### IMU (Inertial Measurement Unit)

The IMU provides acceleration, angular velocity, and sometimes orientation. It is essential for motion tracking, balancing, and sensor fusion.

### Force and Torque Sensors

Used at robot joints, grippers, and feet. These allow compliant motion, safe human–robot interaction, and precise manipulation tasks.

### Joint Encoders

These measure the position or velocity of robot joints and are crucial for forward and inverse kinematics.

## 3.3 The Perception Pipeline in ROS 2

A standard ROS 2 perception stack includes the following stages:

### 1. Sensor Drivers

These nodes interface directly with hardware or simulation, publishing raw sensor data.

### 2. Pre-processing

Noise removal, rectification, calibration, and depth filtering happen here.

### 3. Feature Extraction

Keypoints, descriptors, edges, and higher-level structures are extracted.

### 4. Data Fusion

Techniques such as EKF (Extended Kalman Filter), UKF, and particle filters merge data from cameras, LiDAR, and IMUs.

### 5. Semantic Understanding

Object detection, semantic segmentation, or 3D scene understanding via neural networks.

### 6. Publishing to Downstream Systems

Navigation, mapping, manipulation, and behaviour nodes consume perception outputs.

This modular approach allows multiple algorithms to be swapped without changing the entire system.


