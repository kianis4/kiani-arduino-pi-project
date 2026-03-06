# Critical Parts Analysis: Gesture-Controlled Robotic Hand

While the Bill of Materials (BOM) contains many necessary components for building the robotic hand, certain parts are fundamental to the project's performance and structural integrity. Substituting or downgrading these specific items will heavily compromise the ML workload, power stability, or mechanical grip.

Based on the project's requirements, here are the most important parts:

## 1. Core Compute & Control
* **Raspberry Pi 5 (8GB)**: The brain of the project. It handles the heavy machine learning and computer vision workload (MediaPipe hand tracking). The 8GB version ensures there's enough RAM for the camera and ML models to run smoothly without bottlenecks.
* **Arduino Mega 2560**: Crucial for offloading real-time tasks from the Pi. It seamlessly interfaces with the servo driver and leaves ample pins for future sensor expansion.
* **PCA9685 16-Channel Servo Driver Board**: Directly driving 8 servos from an Arduino can cause jitter. This board offloads the work and generates clean, jitter-free PWM signals via I2C, requiring only 2 pins.

## 2. Uncompromised Power Systems
Power instability is a primary failure point in robotics. Underpowering this setup will cause brownouts and erratic behavior.
* **Raspberry Pi 5 Official 27W USB-C Power Supply**: The Pi 5 natively requires 5V/5A. Third-party power supplies or standard phone chargers will cause the Pi to throttle, severely degrading ML tracking frame rates.
* **6V 10A DC Power Supply (for servos)**: 8 servos pulling stall current can reach ~9.6A in a worst-case scenario. The 10A supply provides the necessary headroom to prevent voltage drops. Furthermore, running at 6V (instead of 5V) maximizes the torque of the servos. Providing proper power here is considered a "no-regret" choice.

## 3. Thermal Management
* **Raspberry Pi 5 Active Cooler**: Under sustained MediaPipe/ML vision workloads, the Pi 5 generates significant heat. The active cooler is mandatory to prevent thermal throttling and maintain real-time hand-tracking performance.

## 4. Mechanical & Actuation
* **MG996R Metal Gear Servos**: Standard plastic servos (like the cheaper SG90s) are highly prone to stripping their gears under real-world loads. The MG996R servos feature metal gears and provide the necessary 10 kg·cm of torque required for a strong, reliable grip.
* **Braided Fishing Line (80lb / 36kg test)**: Acts as the artificial tendons for the fingers. Its properties are critically important—it is incredibly strong, very thin, low-stretch, and holds knots perfectly, which prevents the fingers from slacking over time.

> [!WARNING]
> **Cost-Cutting Caveats**
> 
> If you are on a strict budget, you can save money by utilizing university lab equipment (multimeters, soldering irons) or temporarily dropping down to a Pi 5 4GB model. However, **do not downgrade the servos (to SG90s) or the servo power supply (to a 5V/6A unit).** Downgrading these will critically impact the mechanical grip and stability of the robotic hand.
