---
id: chapter1
title: Chapter 1 — The Robotic Nervous System (ROS 2)
sidebar_label: Chapter 1 — The Robotic Nervous System (ROS 2)
---

# **Chapter 1 — The Robotic Nervous System (ROS 2)**

---

## **1.1 From Digital to Physical: The Embodied Intelligence Gap**

```md
---
id: embodied-intelligence
title: 1.1 From Digital to Physical
---
```

### **The Embodied Intelligence Gap**

Modern AI models excel in digital domains—text, images, audio, and structured reasoning. However, when the same intelligence is transferred to the physical world, a *gap* appears. This challenge is known as the **Embodied Intelligence Gap**.

Digital intelligence has no friction, no inertia, and no real-world uncertainty. In simulation, a robot’s arm moves perfectly every time. On a real robot, slight motor offsets, battery voltage dips, and unpredictable friction mean:

* A perfectly planned trajectory may miss its target
* Sensors may return noisy or partial data
* Real-world physics may cause delays or oscillations

To address this, robotics uses structured software frameworks capable of dealing with asynchronous data, noisy sensors, and real-time physical control loops. The global standard for this capability is **ROS 2 (Robot Operating System 2)**.

### **Why ROS 2 Matters**

ROS 2 provides the communication infrastructure that allows:

* Sensors to publish data continuously
* Control algorithms to react to new information
* Planners to generate safe trajectories
* AI agents to act on physical systems reliably

It functions as the **nervous system** of a robot—coordinating perception, decision-making, and actuation across distributed computational components.

Embodied intelligence emerges when both software and hardware behave cohesively under real-world constraints, and ROS 2 is the foundational layer enabling this alignment.

---

## **1.2 ROS 2 Architecture: Nodes, Topics, and Services**

```md
---
id: ros2-architecture
title: 1.2 ROS 2 Architecture
---
```

ROS 2 provides a flexible, modular structure that ensures robots can run complex tasks reliably. At its core, ROS 2 is a **middleware** built upon the DDS (Data Distribution Service) communication standard.

### **Key Architectural Components**

### **Nodes**

A **Node** is a modular process that performs a specific function.
Examples:

* A camera driver
* A LiDAR processor
* A navigation planner
* A wheel motor controller

Nodes remain independent so that a failure in one does not collapse the whole system.

**Example: A simple ROS 2 node in Python**

```python
import rclpy
from rclpy.node import Node

class Greeter(Node):
    def __init__(self):
        super().__init__('greeter_node')
        self.get_logger().info("Greeter node initialised.")

def main():
    rclpy.init()
    node = Greeter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

---

### **Topics (Publish–Subscribe)**

Topics allow nodes to **stream data continuously**.

* A camera node publishes images to `/camera/image`
* A motor controller subscribes to `/cmd_vel`
* A LiDAR node publishes scans to `/scan`

Properties:

* Asynchronous
* One-to-many and many-to-one
* Ideal for sensors and motor commands

**Example: Publisher & Subscriber**

**Publisher:**

```python
class NumberPublisher(Node):
    def __init__(self):
        super().__init__('number_publisher')
        self.publisher = self.create_publisher(int, 'numbers', 10)
        self.timer = self.create_timer(1.0, self.publish_number)

    def publish_number(self):
        msg = int(42)
        self.publisher.publish(msg)
        self.get_logger().info("Published 42")
```

**Subscriber:**

```python
class NumberListener(Node):
    def __init__(self):
        super().__init__('number_listener')
        self.subscriber = self.create_subscription(
            int,
            'numbers',
            self.callback,
            10
        )

    def callback(self, msg):
        self.get_logger().info(f"Received: {msg}")
```

---

### **Services (Request–Response)**

Some robotic actions require a *transaction*, not a stream.
Services follow a **synchronous request-response** pattern.

Use cases:

* Resetting a sensor
* Requesting a map
* Computing an inverse kinematic solution

**Example: A simple ROS 2 service**

```python
from example_interfaces.srv import AddTwoInts

class Adder(Node):
    def __init__(self):
        super().__init__('adder_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.callback)

    def callback(self, request, response):
        response.sum = request.a + request.b
        return response
```

---

## **1.3 Bridging Python to ROS: rclpy & Agent-Based Control**

```md
---
id: ros-agents
title: 1.3 Bridging Python to ROS
---
```

### **rclpy: Python’s Gateway to ROS 2**

While ROS 2 is written in C++, the Python client library **rclpy** allows developers to:

* Write nodes
* Publish and subscribe to topics
* Call and host services
* Interface AI agents with motors and sensors
* Build high-level behaviour systems

It is particularly useful for integrating **LLM-based robotic agents** that operate at a higher level of abstraction.

### **How AI Agents Control Robots**

AI agents do not control motors directly. Instead, they use ROS 2 middleware to interact with robotics systems safely and predictably.

**Control flow example:**

1. An agent generates a goal (“Pick up the cup”).
2. The agent sends a ROS 2 service request to a motion planner.
3. The planner computes a collision-free trajectory.
4. The controller node publishes velocity commands.
5. Sensors continuously publish feedback to ensure accuracy.

Example: A Python node that exposes an AI “intent” as a ROS message:

```python
class IntentPublisher(Node):
    def __init__(self):
        super().__init__('intent_publisher')
        self.pub = self.create_publisher(String, 'robot_intent', 10)

    def send_intent(self, text):
        msg = String()
        msg.data = text
        self.pub.publish(msg)
        self.get_logger().info(f"Intent sent: {text}")
```

This method lets agents guide robots without directly handling low-level control loops—keeping operations safe and modular.

