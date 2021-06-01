# PID HUMIDIFIER
Welcome to our PID Humidifier Project. This project was done for PHYS 15C LAB class with the aid of Daniel Sorensen, Simon Mitchell, and Nic Arnaud.

Our goal for this project was to convert a commercial, manually controlled, humidifier to an electronically controlled one. Humidifiers meant for bedrooms and rooms of similar size are not very sophisticated as in they are either on or off, with their knobs changing their strength. They get the job done but they can’t set and maintain the humidity of rooms on their own. We wanted to improve upon the design and turn a humidifier into a PID controlled humidifier which can maintain given humidity levels using feedback from sensors. This project required us to construct a system to measure and maintain humidity with the only prebuilt parts being the humidifier, Raspberry Pi, and electrical peripherals from Adafruit and other suppliers.

# List of Components:
* 4 x Adafruit HTU21D-F Temperature & Humidity Sensor Breakout Board ($16 each)
* Raspberry PI (Already had)
* Pure Enrichment MistAire XL Ultrasonic Cool Mist Humidifier ($64)
* Etekcity ZAP 5LX Wireless Remote Control Outlet Switch ($39 for 5)
* 433Mhz Rf Transmitter and Receiver Module Board ($15)
* HiLetgo ULN2003 28BYJ-48 4-Phase Stepper Motor ($13 for 5)
* Adafruit TCA9548A 1-to-8 I2C Multiplexer ($8)
* 100 ft red 18 gauge wire ($10)

Total cost came to around $210 but we only used about $130 of the materials (we had extra sensors, motors, and outlets). For reference, humidifiers with built in humidistats range between $70-$110. 

# Motivation
Maintaining humidity levels is crucial in many temperamental setups. For instance in a lab environment, too high humidity can cause the air to reach its dew point and cause water to collect on equipment. On the other hand, if the humidity is too low, static electricity could build in the air resulting in unwanted electric discharge. Another important use is in greenhouse control, maintaining suitable living conditions for whatever plant you are trying to grow. Controlling humidity is a subtle yet important component of many room scaled projects, not just a cure for dry skin. We wanted to see how well we could construct a sophisticated humidifier without wasting our budget and provide a sort of tutorial for others to do the same.
# Design
Our project is composed of two modules: humidity sensing, and humidity control. The sensing component consists of four Adafruit humidity sensors connected to a multiplexer that allows the Raspberry Pi to interface with all of them through a single I2C port. By gathering humidity data through the sensors, the Raspberry Pi runs our algorithm to decide a level to set the humidifier to, which is accomplished through the control module. The control module consists of a commercial humidifier, outfitted with a stepper motor to manually manipulate its power knob, and plugged into a remote control outlet which toggles its power. By actuating the motor and sending radio signals to toggle the outlet, our Raspberry Pi is able to toggle the humidifier’s power state, as well as making finer adjustments to its power level. *Pictures of the whole setup*
# Wiring
Most of the components were connected together via breadboard. Our radio transmitter and receiver are wired straight to the Raspberry Pi. The humidity sensors, with the same, unchangeable I2C port address needed to be wired through the I2C Multiplexer so that the Pi could communicate with all of them separately. The stepper motor is connected to a breakout board that interfaces directly with the Pi, which takes power, ground, and data connections and actuated the motor itself. 
## Sensor Circuit
![Screen Shot 2021-06-01 at 14 22 34](https://user-images.githubusercontent.com/54754917/120393211-68b6a900-c2e6-11eb-885a-6968c94bdb74.jpeg)
 HTU21D-F Sensor |  TCA9548A Multiplexer
:-------------------------:|:-------------------------:
![IMG_2329](https://user-images.githubusercontent.com/54754917/120395690-43c43500-c2ea-11eb-85f1-8dcfb18fe851.jpeg)  |  ![IMG_2327](https://user-images.githubusercontent.com/54754917/120395844-86860d00-c2ea-11eb-8b9f-ee08fb5c4edd.jpeg)
## Motor/Transmitter/Reciever Circuit
![71D705D0-E963-4D03-8B7A-882E52D9CAC2_1_105_c](https://user-images.githubusercontent.com/54754917/120394406-3908a080-c2e8-11eb-9981-4eaf4ddb1052.jpeg)
hello |
:-----------------------------------:|
![fullDiagram](https://user-images.githubusercontent.com/54754917/120396783-006ac600-c2ec-11eb-94d8-b10ef70cf266.jpeg)

# Building Process
 We are using a commercial humidifier so all of the building concerns the electrical components. Firstly, we used a remote controlled outlet switch to turn the humidifier on and off from the PI and connected a humidity sensor to the Pi. Once enough testing was done with a single sensor, we added the multiplexer to our circuit to be able to use our 4 sensors at once. After experimenting with that we went onto attaching a stepper motor setup to the knob so that we could control the power on a finer level than simple power toggling. At this point we decided on the volume in which we would test our algorithms - a small backpacking tent that was lying around. We assembled the whole setup, with a single sensor hanging from the ‘ceiling’ of the tent above the humidifier.
# Testing/Constructing the PID
 Our first tests were done in a bedroom with a single sensor, we let the humidifier turn at max strength for about 30 minutes to see how strong the humidifier was. These first few tests did not tell us much other than we had a working sensor and humidifier. Due to the difference in size between humidifier and room, we decided to move our set-up to a one person tent; its smaller volume and relative airtightness made our data collection much faster and smoother. 
# Code
 We 
# A Note on Multiple Sensors
Our project is fully wired up to make use of multiple sensors, which can improve humidity control by cross-referencing to reduce signal noise, or perhaps measuring humidity at multiple different points in a single volume. However, the sensors’ readings differ from each other substantially and inconsistently, so much so that our calibration attempts failed miserably. As a result our final project makes use of only a single sensor. One may be able to make multiple sensors work by collecting information on each sensor’s bias at a range of humidity levels and using that to calibrate future readings. Our efforts in this direction, however, were unsuccessful. :(
# Finished Project
* TBD

