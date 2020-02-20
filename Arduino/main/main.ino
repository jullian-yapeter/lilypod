#include "Arduino.h"
#include "src/sensor/Conductivity.h"
#include "src/sensor/PhSensor.h"
#include "src/actuator/Motor.h"
#include <Servo.h>
#include "src/actuator/Garage.h"
// #include "src/actuator/Trap.h"

// by Team Lilypod <http://www.projectlilypod.com>

// Main script to run Arduino's responsibilities: pH sensor, conductivity sensor,
// garage door, and trap door

// Created 22 Jan 2020
// Pin intializations
const int pHSensorPin = A0;
const int motorPin1 = 24;
const int motorPin2 = 25;
const int motorEn = 2;
const int servoGaragePin = 4;
const int limSwitchTop = 8;
const int limSwitchBottom = 9;


PhSensor phSensor(pHSensorPin);
Motor testMotor(motorPin1, 
                motorPin2,
                motorEn);
Garage garage;

void setup(){
    Serial.begin(9600);
    garage.setupGarage(servoGaragePin, limSwitchTop, limSwitchBottom);
    
}

void loop(){
    //  phSensor.samplePh();
    // testMotor.testFunction();
    // garage.closeGarage();

}
