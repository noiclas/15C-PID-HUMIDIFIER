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

Total cost came to around $210 but we only used about $130 of the materials (we had extra sensors, motors, and outlets). For reference, humidifiers with built in humidistats range between $70-$110 :(.

# Motivation
Maintaining humidity levels is crucial in many temperamental setups. For instance in a lab environment, too high humidity can cause the air to reach its dew point and cause water to collect on equipment. On the other hand, if the humidity is too low, static electricity could build in the air resulting in unwanted electric discharge. Another important use is in greenhouse control, maintaining suitable living conditions for whatever plant you are trying to grow. Controlling humidity is a subtle yet important component of many room scaled projects, not just a cure for dry skin. We wanted to see how well we could construct a sophisticated humidifier without wasting our budget and provide a sort of tutorial for others to do the same.
# Design
Our project is composed of two modules: humidity sensing, and humidity control. The sensing component consists of four Adafruit humidity sensors connected to a multiplexer that allows the Raspberry Pi to interface with all of them through a single I2C port. By gathering humidity data through the sensors, the Raspberry Pi runs our algorithm to decide a level to set the humidifier to, which is accomplished through the control module. The control module consists of a commercial humidifier, outfitted with a stepper motor to manually manipulate its power knob, and plugged into a remote control outlet which toggles its power. By actuating the motor and sending radio signals to toggle the outlet, our Raspberry Pi is able to toggle the humidifier’s power state, as well as making finer adjustments to its power level. 
## Full Circuit 
![fullDiagram](https://user-images.githubusercontent.com/54754917/120396783-006ac600-c2ec-11eb-94d8-b10ef70cf266.jpeg)
# Wiring
Most of the components were connected together via breadboard. Our radio transmitter and receiver are wired straight to the Raspberry Pi. The humidity sensors, with the same, unchangeable I2C port address needed to be wired through the I2C Multiplexer so that the Pi could communicate with all of them separately. The stepper motor is connected to a breakout board that interfaces directly with the Pi, which takes power, ground, and data connections and actuated the motor itself. 

## Sensor Circuit
![Screen Shot 2021-06-01 at 14 22 34](https://user-images.githubusercontent.com/54754917/120393211-68b6a900-c2e6-11eb-885a-6968c94bdb74.jpeg)
 HTU21D-F Sensor |  TCA9548A Multiplexer
:-------------------------:|:-------------------------:
![IMG_2329](https://user-images.githubusercontent.com/54754917/120395690-43c43500-c2ea-11eb-85f1-8dcfb18fe851.jpeg)  |  ![IMG_2327](https://user-images.githubusercontent.com/54754917/120395844-86860d00-c2ea-11eb-8b9f-ee08fb5c4edd.jpeg)
## Motor/Transmitter/Reciever Circuit
![71D705D0-E963-4D03-8B7A-882E52D9CAC2_1_105_c](https://user-images.githubusercontent.com/54754917/120394406-3908a080-c2e8-11eb-9981-4eaf4ddb1052.jpeg)
 Remote Outlet + Logo |  Motor + Driver Board
:-------------------------:|:-------------------------:
![IMG_2326](https://user-images.githubusercontent.com/54754917/120397570-64da5500-c2ed-11eb-9bb7-e210932ef5d7.jpeg) | ![IMG_3228](https://user-images.githubusercontent.com/54754917/120397623-7ae81580-c2ed-11eb-990d-f91b16e885d0.jpeg)


# Building Process
 We are using a commercial humidifier so all of the building concerns the electrical components. Firstly, we soldered the humidity sensors to 10-12 ft of wire; we initially wanted to have long wires so that we could freely place sensors around a room. We used a remote controlled outlet switch to turn the humidifier on and off from the PI and connected a humidity sensor to the Pi. Once enough testing was done with a single sensor, we added the multiplexer to our circuit to be able to use our 4 sensors at once. After experimenting with that we went onto attaching a stepper motor setup to the knob so that we could control the power on a finer level than simple power toggling. At this point we decided on the volume in which we would test our algorithms - a small backpacking tent that was lying around. We assembled the whole setup, with a single sensor hanging from the ‘ceiling’ of the tent above the humidifier.
# Testing/Constructing the PID
 Our first tests were done in a bedroom with a single sensor, we let the humidifier turn at max strength for about 30 minutes to see how strong the humidifier was. These first few tests did not tell us much other than we had a working sensor and humidifier. Due to the difference in size between humidifier and room, we decided to move our set-up to a one person tent; its smaller volume and relative airtightness made our data collection much faster and smoother.
   Tent |  Inside Tent
:-------------------------:|:-------------------------:
![IMG_3230](https://user-images.githubusercontent.com/54754917/120402717-a4a63a00-c2f7-11eb-9a0e-9ff0f94205a5.jpeg)|![IMG_3229](https://user-images.githubusercontent.com/54754917/120402761-b7207380-c2f7-11eb-994f-43a130b950aa.jpeg)

First we ran a simple bang-bang control algorithm, where we instructed the humidifier to go fully on when the humidity dipped below a set point, and fully off when it went above. These results (shown below) were promising, but nowhere near the accuracy we hoped to achieve with full PID control.
## Some Bang-Bang
![bangbang_feedback](https://user-images.githubusercontent.com/54754917/120405885-7aa44600-c2fe-11eb-95f9-98f74337d00c.jpeg)

At this point we began writing the PID control script. Given the noisiness of the data given by the sensors, as well as the slow-changing nature of this situation, we elected to neglect the Differential term following fruitless efforts to use it in a meaningful way. Our final script contains functions to determine the Proportional and Integral errors, with user-changeable gain parameters for each. 
We extensively tested the PID script with various gain parameters, as well as different amounts of time to calculate the Integral term over - ultimately what we landed on a Proportional gain of 3, Integral gain of 0.3, and an integration time of 20 seconds. This meant that a consistent deviation of 5% from the target would cause the humidifier to adjust its power by about 45%. This allowed the humidifier to respond relatively aggressively to deviations from the setpoint, while keeping oscillations as minimal as possible.
## Some PID
![pid_humidity](https://user-images.githubusercontent.com/54754917/120405938-9576ba80-c2fe-11eb-999e-67f08aab3d34.jpeg)
![Screen Shot 2021-06-02 at 11 15 16 AM](https://user-images.githubusercontent.com/62636144/120531808-e1277380-c393-11eb-874c-9c963b1ff864.png)




# Code
Our code made use of the PI's built in SSH features. In the most general terms, we would send the PI the parameters such as the target humidity and PID coefficients which would start up the PI and PID algorithm. The data is then saved into a pickle file which we could extract from the PI through SSH. The pickle file is then unpickled and used in our live plotter showing plots of the relative humidity and power level of the humidifier. The specifics of our code can be found under the OVERVIEW and GUIDE files in the PID-SYSTEM and EXPERIMENT-PIPELINE folders.

We wrote a Python class (sensorArray.py) that utilizes Adafruit’s HTU21D and TCA9548A libraries to communicate with the humidity sensors and multiplexer, respectively. (https://pypi.org/project/adafruit-circuitpython-HTU21D/, https://pypi.org/project/adafruit-circuitpython-tca9548a/)  This class was implemented in higher-level scripts to simplify programming.

Additionally, we wrote motorclass.py to communicate with our stepper motor, keep track of the current power level, and easily change power levels. It makes use of the RPistepper library (https://pypi.org/project/RPistepper/) to control the stepper motor.

The radio transmitter and receiver were commanded via OS-Level commands that make use of the rfoutlet library (https://github.com/timleland/rfoutlet).
# A Note on Multiple Sensors
Our project is fully wired up to make use of multiple sensors, which can improve humidity control by cross-referencing to reduce signal noise, or perhaps measuring humidity at multiple different points in a single volume. However, the sensors’ readings differ from each other substantially and inconsistently, so much so that our calibration attempts failed miserably. As a result our final project makes use of only a single sensor. One may be able to make multiple sensors work by collecting information on each sensor’s bias at a range of humidity levels and using that to calibrate future readings. Our efforts in this direction, however, were unsuccessful. :(
# Finished Project
Overall, our project was successful within a certain range of conditions. As the PID plots above show, we successfully implimented the stabilization of certain humidity levels in a tent on a calm day, which captures the spirit of what we set out to do. Our project worked best when the wind was low and there were minimal natural disturbances to the tent. However, on windy days where there were significant random losses of humidity followed by calm periods where most of the humidity was trapped inside the tent, there was only so much that our algorithm could do.

![windyDayPID](https://user-images.githubusercontent.com/62636144/120526395-01ecca80-c38e-11eb-8f0c-cf4de7bce41b.png)

As we watched this experiment unfold, it seemed that with every gust of wind the algorithm was powerless to stop the humidity from dropping far below the desired level, and it never had a chance to stabilize. 

This less sucessful trial shows the limitations of our setup, and clarifies what it accomplishes. When the humidifier is turned on to a certain power level, the enviornment will tend to favor some average humidity reading. The PID alrogithm responds to deviations from that average, and can even set the humidity to a level consistently higher or lower than that average. This works well when the enviornmental conditions do not change quickly or sharply, but naturally fails when the enviornmental conditions alter the humidity more strongly than the humidifier can.






