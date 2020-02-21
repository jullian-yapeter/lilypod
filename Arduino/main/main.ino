#include <Servo.h>
#include "Arduino.h"
#include "src/sensor/Conductivity.h"
#include "src/sensor/PhSensor.h"
#include "src/actuator/Motor.h"
#include "src/actuator/ServoDoor.h"
#include "src/Serialcomm.h"

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
Serialcomm serialcomm;

Motor testMotor;
ServoDoor garage;

void setup(){
    Serial.begin(9600);
    testMotor.setupMotor(motorPin1, motorPin2, motorEn);
    garage.setupDoor(servoGaragePin, limSwitchTop, limSwitchBottom);
    
}

void loop(){
    //  phSensor.samplePh();
    // testMotor.testFunction();
    //  garage.closeDoor();
    // serialcomm.runSerialComm();

    float commandsData[serialcomm.messageLength] = {0.0};
    serialcomm.receiveCommandsData();
    serialcomm.getCommandsData(commandsData);

    float pumpState = commandsData[0];
    float pumpDir = commandsData[1];
    float pumpSpeed = commandsData[2];
    float garageState = commandsData[3];
    float garageDir = commandsData[4];
    float trapState = commandsData[5];
    float trapDir = commandsData[6];
    float phState = commandsData[7];
    float condState = commandsData[8];

    // Do stuff with commands: get sensor data and run actuators
    float phValue = 3.14;
    float condValue = 24.8;
    float newGarageState = 1.0;
    float newTrapState = 0.0;
    ////

    float sensorData[serialcomm.messageLength] = {0.0};
    sensorData[0] = phValue;
    sensorData[1] = condValue;
    sensorData[2] = newGarageState;
    sensorData[3] = newTrapState;

    serialcomm.setSensorData(sensorData);
    serialcomm.sendSensorData();

    // If we want to check what the Arduino is receiving
    // serialcomm.mirrorReceiveData();
}
