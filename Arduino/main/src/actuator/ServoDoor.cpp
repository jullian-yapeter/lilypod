/*
  ServoDoor.h - library for garage door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

// include this library's description file
#include "Arduino.h"
#include "ServoDoor.h"
#include <Servo.h>


// Constructor /////////////////////////////////////////////////////////////////)

/*
void ServoDoor::setupDoor(int servoPin, int limSwitchTop, int limSwitchBottom){
    Servo servo;

    _servo = servo;
    _servoPin = servoPin;
    _limSwitchTop = limSwitchTop;
    _limSwitchBottom = limSwitchBottom;

    _servo.attach(_servoPin);
    pinMode(_limSwitchTop, INPUT);
    pinMode(_limSwitchBottom, INPUT);
}
*/

void ServoDoor::setupTrapDoor(int servoPin, int limSwitch, int closeAngle){
    Servo servo;

    _servo = servo;
    _servoPin = servoPin;
    _limSwitch = limSwitch;
    _closeAngle = closeAngle;
    _useLimSwitch = true;

    _servo.attach(_servoPin);
    pinMode(_limSwitch, INPUT);
}

void ServoDoor::setupGarageDoor(int servoPin, int openAngle, int closeAngle){
    Servo servo;

    _servo = servo;
    _servoPin = servoPin;
    _openAngle = openAngle;
    _closeAngle = closeAngle;
    _useLimSwitch = false;

    _servo.attach(_servoPin);
    _servo.write(_openAngle);
    int startAngle = _servo.read();
    // Serial.print("Angle: ");
    // Serial.println(startAngle);
    // Serial.print("\n");
}

// Public Methods //////////////////////////////////////////////////////////////
// Assume opening the garage requires CW rotation
float ServoDoor::openDoor(){
    // If top limit switch open, keep servo moving in a direction.
    if (!_useLimSwitch){
        changeToServoAngle(_openAngle);
        return 1.0;
    }else{
        int startTime = millis();
        int currTime = millis();
        while(!isLimSwitchClosed()){
            changeServoAngle(_FORWARD);
            currTime  = millis();
            if (currTime - startTime > _TIMEOUT*1000){
                // Serial.println("Time out on trap door open");
                return 2.0;
            }
        }
        return 1.0;
    }
    // Serial.println("Door opened");
    return 1.0;
    
}

float ServoDoor::closeDoor(){
    changeToServoAngle(_closeAngle);
    return 0.0;
}

/*
bool ServoDoor::isTopSwitchClosed(){
    bool isClosed = false;
    if ((digitalRead(_limSwitchTop) == LOW) && (_topFlag == 0)){
        // Serial.println("Garage door completely closed");
        _topFlag = 1;
        delay(20);
    }
    if((digitalRead(_limSwitchTop) == HIGH) && (_topFlag == 1)){
        // Serial.println("Garage door not completely closed");
        _topFlag = 0;
        delay(20);
    }
    digitalWrite(_limSwitchTop, HIGH);

    if (digitalRead(_limSwitchTop) == LOW){
        isClosed = true;
    }else if (digitalRead(_limSwitchTop) == HIGH){
        isClosed = false;
    }
    return isClosed;
}

bool ServoDoor::isBottomSwitchClosed(){
    bool isClosed = false;
    if ((digitalRead(_limSwitchBottom) == LOW) && (_bottomFlag == 0)){
        // Serial.println("Garage door completely open");
        _bottomFlag = 1;
        delay(20);
    }
    if((digitalRead(_limSwitchBottom) == HIGH) && (_bottomFlag == 1)){
        // Serial.println("Garage door not completely open");
        _bottomFlag = 0;
        delay(20);
    }
    digitalWrite(_limSwitchBottom, HIGH);
    if (digitalRead(_limSwitchBottom) == LOW){
        isClosed = true;
    }else if (digitalRead(_limSwitchBottom) == HIGH){
        isClosed = false;
    }
    return isClosed;
}

*/

bool ServoDoor::isLimSwitchClosed(){
    bool isClosed = false;
    if ((digitalRead(_limSwitch) == LOW) && (_bottomFlag == 0)){
        // Serial.println("Garage door completely open");
        _bottomFlag = 1;
        delay(20);
    }
    if((digitalRead(_limSwitch) == HIGH) && (_bottomFlag == 1)){
        // Serial.println("Garage door not completely open");
        _bottomFlag = 0;
        delay(20);
    }
    digitalWrite(_limSwitch, HIGH);
    if (digitalRead(_limSwitch) == LOW){
        isClosed = true;
    }else if (digitalRead(_limSwitch) == HIGH){
        isClosed = false;
    }
    return isClosed;
}

void ServoDoor::changeServoAngle(int direction){
    int newAngle = 0;
    int currAngle = 0;
    currAngle = _servo.read();
    if (direction == _FORWARD){
        newAngle = currAngle + 10;
    } else if (direction == _BACKWARD){
        newAngle = currAngle - 10;
    }
    if (newAngle >= _maxAngle){
        // // Serial.println("Max angle reached");
        newAngle = _maxAngle;
    } else if (newAngle <= _minAngle){
        newAngle = _minAngle;
    }
    // // Serial.print("New Angle: ");
    // // Serial.print(newAngle);
    // // Serial.print("\n");
    _servo.write(newAngle);
    delay(200);
}

void ServoDoor::changeToServoAngle(int newAngle){
    int currAngle = 0;
    currAngle = _servo.read();
    if (newAngle > currAngle){
        while (currAngle < newAngle){
            _servo.write(currAngle + _increment);
            currAngle = _servo.read();
            delay(_DELAY);
        }
    }
    if (newAngle < currAngle){
        while (currAngle > newAngle){
            _servo.write(currAngle - _increment);
            currAngle = _servo.read();
            delay(_DELAY);
        }
    }
    
}

void ServoDoor::testFunction(){
    // Make servo go to 0 degrees 
    // Serial.println("In test function");
    _servo.write(0);
    // Serial.println("moved 0");
    delay(2000); 
    // Make servo go to 90 degrees 
    _servo.write(90);
    // Serial.println("moved 90");
    delay(2000); 
    // Make servo go to 180 degrees 
    _servo.write(-90); 
    // Serial.println("moved -90");
    delay(2000);
    _servo.write(0);
    // Serial.println("moved 0");
    delay(2000);
    // Serial.println("Exiting test function");
}


void ServoDoor::testFunctionGarage(){
    closeDoor();
    // Serial.print("Closing Servo door. ");
    // Serial.print("Moving to ");
    // Serial.print(_closeAngle);
    // Serial.print("\n");
    delay(5000);
    openDoor();
    // Serial.print("Opening Servo door. ");
    // Serial.print("moving to ");
    // Serial.print(_openAngle);
    // Serial.print("\n");
    delay(5000);
}