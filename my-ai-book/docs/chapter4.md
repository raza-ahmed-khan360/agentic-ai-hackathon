---
id: chapter4
title: Chapter 4 — Motion Planning and Control
sidebar_label: Chapter 4 — Motion Planning and Control
---

# **Chapter 4 — Motion Planning and Control**

Motion planning enables robots to move purposefully through space while avoiding obstacles and adhering to physical constraints. This chapter introduces the principles behind trajectory generation, inverse kinematics, and control strategies for wheeled and humanoid robots.

## 4.1 Why Planning Matters

Planning bridges perception and action. While AI agents understand goals, planners determine *how* to achieve them physically.

Examples:

* A mobile robot must reach a target location without collisions.
* A manipulator must pick up an object without hitting shelves.
* A humanoid must walk without falling.

Planning ensures movements are safe, efficient, and dynamically feasible.

## 4.2 Kinematics: The Mathematical Backbone

### Forward Kinematics (FK)

Given joint angles, FK computes the end-effector pose. This is used for sensing, verification, and visualisation.

### Inverse Kinematics (IK)

Given a desired pose, IK computes the necessary joint angles. Solutions may not be unique, and robots often prioritise smoothness, joint limits, or energy efficiency.

## 4.3 Path Planning Algorithms

Robotics uses a mixture of geometric and sampling-based planners.

### A* and Dijkstra

Good for grid maps and structured environments.

### RRT (Rapidly-exploring Random Trees)

Efficient for high-dimensional spaces, such as 7-DOF manipulators.

### PRM (Probabilistic Roadmap)

Useful when the environment is mostly static.

### Trajectory Optimisation

Includes algorithms like CHOMP and TrajOpt that refine paths into smooth, continuous motions.

## 4.4 Control Systems

After a trajectory is planned, controllers execute it.

### PID Control

The simplest and most widely used method for speed, position, and torque control.

### Model Predictive Control (MPC)

Optimises control actions over a prediction horizon, excellent for humanoids and balancing tasks.

### Whole-Body Control

Balances multiple objectives simultaneously, such as:

* Stability
* Manipulation
* Energy efficiency
* Joint limit avoidance

This level of coordination is essential for complex humanoid motion.