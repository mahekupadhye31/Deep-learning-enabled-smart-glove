# 🖐️ Gesture Vocalizer – Bridging Communication Through Technology

[![Arduino](https://img.shields.io/badge/Arduino-Mega-blue?logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-orange?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📘 Overview

The **Gesture Vocalizer** project empowers individuals with **speech and hearing impairments** by translating **hand gestures into speech or text output**.  
By combining **flex sensors**, **accelerometers**, and **deep learning models**, this wearable system bridges the communication gap — enabling real-time gesture-to-voice translation.

---

## 🧠 Proposed Design

The design phase focuses on translating the identified problem into a **functional, wearable prototype** that captures, processes, and vocalizes gestures.

---

### 🧩 Hardware Design

#### 1. Arduino Mega Microcontroller  
- Acts as the computational hub with multiple I/O pins.  
- Handles real-time sensor integration and data transmission.

#### 2. Flex Sensors  
- Five sensors attached to a glove detect finger bending through resistance changes.  
- Provide continuous analog data reflecting hand posture.

#### 3. MPU-6050 Accelerometer  
- Measures acceleration and angular velocity to capture spatial orientation.  
- Enhances motion precision and dynamic gesture recognition.

#### ⚙️ Hardware Design Workflow

1. **Sensor Integration:** Connect flex sensors to Arduino analog pins.  
2. **MPU-6050 Integration:** Interface via I2C to capture acceleration and rotation.  
3. **Power Supply:** Powered through USB to ensure stable operation.  
4. **Encapsulation:** Mounted on a glove to maintain sensor stability and comfort.

<p align="center">
  <img src="src/assets/hardware-design.png" alt="Hardware Design" width="600"/>
  <br>
  <em>Fig 1. Proposed Hardware Design</em>
</p>

---

## 💻 Software Design

### 1. Neural Network  
- Implements a **Bi-directional LSTM** for gesture recognition.  
- Processes sequences of sensor readings to identify dynamic and static gestures.  
- Trained using a **custom dataset** for enhanced accuracy.

### 2. Custom Dataset  
- Captures 3-second intervals of sensor data per gesture.  
- Combines flex sensor and MPU-6050 outputs into a single input vector.  
- Stored in CSV format for efficient model training and testing.

### 3. User Interface  
- A simple **Python-based UI** displays recognized gestures in real time.  
- Enables recording of new gesture data and live model inference.

<p align="center">
  <img src="src/assets/ui.png" alt="User Interface" width="600"/>
  <br>
  <em>Fig 4. User Interface</em>
</p>

---

## ⚙️ Implementation

### 🔧 Algorithm Overview

#### Initialization
- Define analog pins for flex sensors (A0–A4).  
- Initialize MPU6050 and set up I2C communication.  

#### Setup Function
- Begin serial communication and initialize all sensors.  
- Configure pin modes for flex sensors.

#### Loop Function
- Read analog flex sensor data.  
- Capture accelerometer and gyroscope readings.  
- Print all data to the serial monitor for real-time observation.

```cpp
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
int flexPins[5] = {A0, A1, A2, A3, A4};

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  for (int i = 0; i < 5; i++) pinMode(flexPins[i], INPUT);
}

void loop() {
  for (int i = 0; i < 5; i++) {
    int flexVal = analogRead(flexPins[i]);
    Serial.print(flexVal);
    Serial.print("\t");
  }
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  Serial.println();
  delay(100);
}
