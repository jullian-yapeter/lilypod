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
// global variables
const float EPSILON = 0.0001;
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

bool checkequals(float a, float b){
    return (fabs(a - b) < EPSILON);
}

void setup(){
    Serial.begin(9600);
    testMotor.setupMotor(motorPin1, motorPin2, motorEn);
    garage.setupDoor(servoGaragePin, limSwitchTop, limSwitchBottom);
    
}

void loop(){
    // phSensor.samplePh();
    // testMotor.testFunction();
    // garage.closeDoor();
    // serialcomm.runSerialComm();

    float commandsData[serialcomm.messageLength] = {0.0};
    serialcomm.receiveCommandsData();
    serialcomm.getCommandsData(commandsData);

    float pumpState = commandsData[0];
    float pumpSpeed = commandsData[1];
    float garageState = commandsData[2];
    float garageDir = commandsData[3];
    float trapState = commandsData[4];
    float trapDir = commandsData[5];
    float phState = commandsData[6];
    float condState = commandsData[7];
    float ussState = commandsData[8];
    float ledState = commandsData[9];

    // Do stuff with commands: get sensor data and run actuators
    float newGarageState = 0.0;
    float newTrapState = 0.0;
    float phValue = 0.0;
    float condValue = 0.0;
    float ussValue = 0.0;

    if (checkequals(pumpState,1.0)){
        // Run pump with speed = pumpSpeed
    }
    else{
        // Turn off pump
    }
    if (checkequals(garageState,1.0)){
        // Move garage in direction = garageDir
        // update garageState to inform Rpi
        newGarageState = 1.0;
    }
    else{
        // Keep same garage state
    }
    if (checkequals(trapState,1.0)){
        // Move trap in direction = trapDir
        // update trapState to inform Rpi
        newTrapState = 1.0;
    }
    else{
        // Keep same trap state
    }
    if (checkequals(phState,1.0)){
        // get new pH reading and store it in phValue
        phValue = 3.14;
    }
    if (checkequals(condState,1.0)){
        // get new conductivity reading and store it in phValue
        condValue = 24.8;
    }
    if (checkequals(ussState,1.0)){
        // get new ultrasonic reading and store it in phValue
        ussValue = 10.10;
    }
    if (checkequals(ledState,0.0)){
        // shine blue
    }
    else if (checkequals(ledState,1.0)){
        // shine green
    }
    else if (checkequals(ledState,2.0)){
        // shine yellow
    }
    else if (checkequals(ledState,3.0)){
        // shine red
    }


    ////////////////////////////////////////////////////////////

    float sensorData[serialcomm.messageLength] = {0.0};
    sensorData[0] = newGarageState;
    sensorData[1] = newTrapState;
    sensorData[2] = phValue;
    sensorData[3] = condValue;
    sensorData[4] = ussValue;

    serialcomm.setSensorData(sensorData);
    serialcomm.sendSensorData();

    // If we want to check what the Arduino is receiving
    // serialcomm.mirrorReceiveData();
}
