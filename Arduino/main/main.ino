#include "libraries/sensor/Conductivity.h"
#include "src/sensor/PhSensor.h"
#include "libraries/actuator/Garage.h"
#include "libraries/actuator/Trap.h"

// by Team Lilypod <http://www.projectlilypod.com>

// Main script to run Arduino's responsibilities: pH sensor, conductivity sensor,
// garage door, and trap door

// Created 22 Jan 2020
// Pin intializations
const int pHSensorPin = A0;

PhSensor phSensor(pHSensorPin);

void setup(){
    Serial.begin(9600);
    
}

void loop(){
     phSensor.samplePh();
}