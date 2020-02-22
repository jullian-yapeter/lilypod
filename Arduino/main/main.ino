#include <Servo.h>
#include "Arduino.h"
#include "src/sensor/Conductivity.h"
#include "src/sensor/PhSensor.h"
#include "src/sensor/Sonar.h"
#include "src/actuator/Motor.h"
#include "src/actuator/ServoDoor.h"
#include "src/Serialcomm.h"

// by Team Lilypod <http://www.projectlilypod.com>

// Main script to run Arduino's responsibilities: pH sensor, conductivity sensor,
// garage door, and trap door

// Created 22 Jan 2020
// global variables
const float EPSILON = 0.0001;
// Pin intializations start---------------------

// pH Sensor
const int pHSensorPin = A0;

// Pumps
const int motorPin1 = 24;
const int motorPin2 = 25;
const int motorEn = 2;

// Servo doors
const int servoGaragePin = 4;
const int garageLimSwitchTop = 8;
const int garageLimSwitchBottom = 9;
const int servoTrapPin = 5;  // untested
const int trapLimSwitchTop = 6; // untested
const int trapLimSwitchBottom = 7; // untested

// Sonar
const int trigPin = 12;
const int echoPin = 10;  // Not using 13 because 13 connects to onboard LED

// Pin intializations end---------------------

PhSensor phSensor(pHSensorPin);
Serialcomm serialcomm;

Motor pump;
ServoDoor garage;
ServoDoor trap;
Sonar garbageChecker;

bool checkequals(float a, float b){
    return (fabs(a - b) < EPSILON);
}

void setup(){
    Serial.begin(9600);
    pump.setupMotor(motorPin1, motorPin2, motorEn);
    garage.setupDoor(servoGaragePin, garageLimSwitchTop, garageLimSwitchBottom);
    trap.setupDoor(servoTrapPin, trapLimSwitchTop, trapLimSwitchBottom);
    garbageChecker.setupSonar(trigPin, echoPin);
}

void loop(){
    // phSensor.samplePh();
    // testMotor.testFunction();
    // garage.closeDoor();
    // serialcomm.runSerialComm();
    // bool garbageState = garbageChecker.isGarbageFull();

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
        pump.start((int) (pumpSpeed + 0.5), 1);  // 1 for forward
    }
    else{
        // Turn off pump
        pump.stop();
    }
    if (checkequals(garageState,1.0)) {
        // Move garage in direction = garageDir
        // update garageState to inform Rpi
        if (checkequals(garageDir, 1.0)){
            newGarageState = garage.openDoor();
        }
        else if (checkequals(garageState, 0.0)){
            newGarageState = garage.closeDoor();
        }
    }
    if (checkequals(trapState,1.0)){
        
        // Move trap in direction = trapDir
        // update trapState to inform Rpi
        if (checkequals(trapDir, 1.0)){
            newTrapState = trap.openDoor();
        }
        else if (checkequals(trapDir, 0.0)){
            newTrapState = trap.closeDoor();
        }
    }
    if (checkequals(phState,1.0)){
        // get new pH reading and store it in phValue
        phValue = phSensor.samplePh();
    }
    if (checkequals(condState,1.0)){
        // get new conductivity reading and store it in phValue
        condValue = 24.8;
    }
    if (checkequals(ussState,1.0)){
        // get new ultrasonic reading and store it in phValue
        ussValue = garbageChecker.isGarbageFull();
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
