# PID HUMIDIFIER
Welcome to our PID Humidifier Project. This project was done for PHYS 15C LAB class with the aid of Daniel Sorensen, Simon Mitchell, and Nic Arnaud.

Our goal for this project was to convert a commercial, manually controlled, humidifer to an electronically controlled one. Humdifiers meant for bedrooms and rooms of similar size are not very sophisticated as in they are either on or off, with their knobs changing their strength. They get the job done but they cant set and maintain the humidity of rooms on their own. We wanted to improve upon the design and turn a humidifier into a PID humidifer which can maintain given humidity levels using feedback from sensors. This project required us to contruct a system to measure and maintain humdity with the only prebuilt parts being the humidifier, Raspberry Pi, and Pi peripherals.

# List of Components:
* 4 x Adafruit HTU21D-F Temperature & Humidity Sensor Breakout Board
* Raspberry PI
* Pure Enrichment MistAire XL Ultrasonic Cool Mist Humidifier
* Etekcity ZAP 5LX Wireless Remote Control Outlet Switch
* 433Mhz Rf Transmitter and Receiver Module Board
* HiLetgo ULN2003 28BYJ-48 4-Phase Stepper Motor
* Adafruit TCA9548A 1-to-8 I2C Multiplexer

# Design
* TBD
# Wiring
* TBD
# Building Process
* We are using a commercial humidifier so all of the building concerns the electrical components. Firstly, we used a remote controlled outlet switch to turn the humidifier on and off from the PI and connected a humidity sensor to the Pi. Once enough testing was done with a single sensor, we added the muliplexer to our curcuit to be able to use our 4 sensors at once. Once calibrated we went onto attaching a stepper motor setup to the knob so that we could not play with varying the strength of the humidifier (whereas we could only do Bang-Bang before) 
# Testing
* Our first tests were done in a bedroom with a single sensor, we let the humidifer turn at max strength for about 30 minutes to see how good the humidifier was. 
# Code
* TBD
# Finished Project
* TBD
