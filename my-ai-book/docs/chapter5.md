# **Chapter 5 — Humanoid Robotics and Locomotion**

Humanoid robots aim to replicate human movement, enabling them to operate in environments designed for people. This chapter explores humanoid design principles, locomotion models, and the challenges of making AI-driven humanoids stable and responsive.

## 5.1 Why Build Humanoids?

Humanoids can:

* Use human tools
* Navigate stairs, ladders, and uneven terrain
* Work in buildings and factories without redesigning infrastructure
* Interact socially with humans in a natural form

But their complexity is significantly greater than that of wheeled robots.

## 5.2 Humanoid Structure

A typical humanoid includes:

* Head with cameras and sensors
* Torso containing compute hardware and power systems
* Two arms with multi-DOF manipulators
* Two legs with hip, knee, and ankle joints
* Force sensors in the feet
* IMU for balance

### Degrees of Freedom

A standard humanoid has around 25–35 DOF, enabling human-like dexterity.

## 5.3 Locomotion Principles

Humanoid balance is modelled using concepts such as:

### Zero Moment Point (ZMP)

Ensures the centre of mass stays within the support polygon, preventing tipping.

### Inverted Pendulum Model

A mathematical simplification used to generate stable walking patterns.

### Walking Phases

1. Double support (both feet on ground)
2. Single support (one foot in the air)
3. Swing foot trajectory
4. Impact modelling

## 5.4 Whole-Body Motion and Manipulation

Humanoids must coordinate:

* Balance
* Hand placement
* Footstep adjustment
* Centre-of-mass control
* Momentum regulation

Whole-body controllers solve large optimisation problems in real time to determine the best joint accelerations and torques.

## 5.5 AI and Humanoid Behaviour

Modern humanoids are increasingly driven by agentic AI systems that:

* Interpret natural language commands
* Plan complex tasks
* Adapt to dynamic environments
* Learn from demonstrations

ROS 2 provides the infrastructure, while AI agents supply high-level reasoning. Together, they form the foundation of **Physical AI**: robots that think and act in the real world.
