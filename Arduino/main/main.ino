
#include <Servo.h>
#include "Arduino.h"
#include "src/sensor/Conductivity.h"
#include "src/sensor/PhSensor.h"
#include "src/sensor/Sonar.h"
#include "src/actuator/Motor.h"
#include "src/actuator/ServoDoor.h"
#include "src/actuator/LedStrip.h"
#include "src/actuator/LightBulb.h"
#include "src/Serialcomm.h"

// by Team Lilypod <http://www.projectlilypod.com>

// Main script to run Arduino's responsibilities: pH sensor, conductivity sensor,
// garage door, and trap door

// Created 22 Jan 2020
// global variables
const float EPSILON = 0.0001;
// Pin intializations start---------------------
/*
// Mega pins
// pH Sensor
const int pHSensorPin = A0;

// Pumps
const int motorPin1 = 26;  // 24
const int motorPin2 = 27;  // 25
const int motorEn = 2;

// Servo doors
const int servoGaragePin = 4;
// const int garageLimSwitchTop = 30;  //8
// const int garageLimSwitchBottom = 31;  //9
const int servoTrapPin = 5;  // untested
const int trapLimSwitch = 31; // untested
// const int trapLimSwitchBottom = 35; // untested

// Sonar
const int trigPin = 22;
const int echoPin = 23;  // Not using 13 because 13 connects to onboard LED

const int bulbPin = 36
// Mega pins end
*/

// UNO pins
// pH Sensor (1 analog)
const int pHSensorPin = A0;

// Pumps (1 pwm + 2 digital)
const int motorPin1 = 13;  // 24
const int motorPin2 = 12;  // 25
const int motorEn = 3;

// Servo doors (2 pwm + 1 digital)
const int servoGaragePin = 5;
const int servoTrapPin = 6;  // untested
const int trapLimSwitch = 4; // untested


// Sonar (digital)
const int trigPin = 7;
const int echoPin = 8;  // Not using 13 because 13 connects to onboard LED

// Spectrometer bulb (digital)
const int bulbPin = 2;

// LED Strips (3 PWM)
const int redPin = 9;
const int greenPin = 10;
const int bluePin = 11;

// Conductivity (1 analog)
const int conductPin = A1;


// Uno Pins stop

// Pin intializations end---------------------

float newGarageState = 0.0;
float newTrapState = 0.0;
float phValue = 0.0;
float condValue = 0.0;
float ussValue = 0.0;
float newBlulbState = 0.0;
float newLedState = 0.0;

int garageOpenAngle = 180;
int garageCloseAngle = 0;
int trapOpenAngle = 180;
int trapCloseAngle = 0;
int pumpSpeed = 100;
const int pumpDirection = 1;

Conductivity condSensor;
PhSensor phSensor(pHSensorPin);
Serialcomm serialcomm;

Motor pump;
ServoDoor garage;
ServoDoor trap;
Sonar garbageChecker;
LedStrip ledStrip;
LightBulb lightBulb;

bool checkequals(float a, float b){
    return (fabs(a - b) < EPSILON);
}

void setup(){
    Serial.begin(9600);
    pump.setupMotor(motorPin1, motorPin2, motorEn);
    garage.setupGarageDoor(servoGaragePin, garageOpenAngle, garageCloseAngle);
    trap.setupGarageDoor(servoTrapPin, trapOpenAngle, trapCloseAngle);
    garbageChecker.setupSonar(trigPin, echoPin);
    condSensor.setupConductivity(conductPin);
    ledStrip.setupStrip(redPin, greenPin, bluePin);
    lightBulb.setupLightBulb(bulbPin);
}

void loop(){
    // phSensor.samplePh();
    // testMotor.testFunction();
    // garage.testFunction();
    // garage.closeDoor();
    // trap.openDoor();
    // trap.closeDoor();
    garage.testFunctionGarage();
    // trap.testFunctionGarage();
    // serialcomm.runSerialComm();
    // bool garbageState = garbageChecker.isGarbageFull();
    // condSensor.sampleConductivity();
    // ledStrip.testFunction();
    // lightBulb.testFunction();
    // while(true){};
    //  runRoutine();
}


void runRoutine(){
    float commandsData[serialcomm.messageLength] = {0.0};
    serialcomm.receiveCommandsData();
    serialcomm.getCommandsData(commandsData);
    //[pumpState, bulbState, garageState, garageDir, trapState, trapDir, phState, condState, ussState, ledStrip]
    float pumpState = commandsData[0];
    float bulbState = commandsData[1];
    float garageState = commandsData[2];
    float garageDir = commandsData[3];
    float trapState = commandsData[4];
    float trapDir = commandsData[5];
    float phState = commandsData[6];
    float condState = commandsData[7];
    float ussState = commandsData[8];
    float ledState = commandsData[9];

    // Do stuff with commands: get sensor data and run actuators

    if (checkequals(pumpState, 1.0)){
        // Run pump with speed = pumpSpeed
        pump.start((int) (pumpSpeed + 0.5), 1);  // 1 for forward
    }
    else{
        // Turn off pump
        pump.stop();
    }
    if (checkequals(bulbState, 1.0)){
        //Turn on lightbulb
        // Serial.println("Turning on spectrometer light");
        newBlulbState = lightBulb.turnOn();
    }
    else{
        //Turn off lightbulb
        // Serial.println("Turning off spectrometer light");
        newBlulbState = lightBulb.turnOff();
    }
    if (checkequals(garageState, 1.0)) {
        // Move garage in direction = garageDir
        // update garageState to inform Rpi
        newGarageState = 2.0;
        if (checkequals(garageDir, 1.0)){
            newGarageState = garage.openDoor();
        }
        else if (checkequals(garageDir, 0.0)){
            newGarageState = garage.closeDoor();
        }
    }
    if (checkequals(trapState, 1.0)){
        newTrapState = 2.0;
        // Move trap in direction = trapDir
        // update trapState to inform Rpi
        if (checkequals(trapDir, 1.0)){
            newTrapState = trap.openDoor();
        }
        else if (checkequals(trapDir, 0.0)){
            newTrapState = trap.closeDoor();
        }
    }
    if (checkequals(phState, 1.0)){
        // get new pH reading and store it in phValue
        phValue = phSensor.samplePh();
    }
    if (checkequals(condState, 1.0)){
        // get new conductivity reading and store it in phValue
        condValue = condSensor.sampleConductivity();
    }
    if (checkequals(ussState, 1.0)){
        // get new ultrasonic reading and store it in phValue
        ussValue = garbageChecker.isGarbageFull();
    }
    if (checkequals(ledState, 0.0)){
        // shine blue
        newLedState = ledStrip.shineBlue();
    }
    else if (checkequals(ledState, 1.0)){
        // shine green
        newLedState = ledStrip.shineGreen();
    }
    else if (checkequals(ledState, 2.0)){
        // shine yellow
        newLedState = ledStrip.shineWhite();
    }
    else if (checkequals(ledState, 3.0)){
        // shine red
        newLedState = ledStrip.shineRed();
    }


    ////////////////////////////////////////////////////////////

    float sensorData[serialcomm.messageLength] = {0.0};
    sensorData[0] = newGarageState;
    sensorData[1] = newTrapState;
    sensorData[2] = phValue;
    sensorData[3] = condValue;
    sensorData[4] = ussValue;
    sensorData[5] = newBlulbState;
    sensorData[6] = newLedState;


    serialcomm.setSensorData(sensorData);
    serialcomm.sendSensorData();

    // If we want to check what the Arduino is receiving
    // serialcomm.mirrorReceiveData();
}
