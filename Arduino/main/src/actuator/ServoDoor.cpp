/*
  ServoDoor.h - library for garage door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

// include this library's description file
#include "Arduino.h"
#include "ServoDoor.h"
#include <Servo.h>


// Constructor /////////////////////////////////////////////////////////////////)

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

// Public Methods //////////////////////////////////////////////////////////////
// Assume opening the garage requires CW rotation
void ServoDoor::openDoor(){
    // If top limit switch open, keep servo moving in a direction.
    while(!isTopSwitchClosed()){
        changeServoAngle(_FORWARD);
    }
}

void ServoDoor::closeDoor(){
    while(!isBottomSwitchClosed()){
        changeServoAngle(_BACKWARD);
    }
}

bool ServoDoor::isTopSwitchClosed(){
    bool isClosed = false;
    if ((digitalRead(_limSwitchTop) == LOW) && (_topFlag == 0)){
        Serial.println("Garage door completely closed");
        _topFlag = 1;
        delay(20);
    }
    if((digitalRead(_limSwitchTop) == HIGH) && (_topFlag == 1)){
        Serial.println("Garage door not completely closed");
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
        Serial.println("Garage door completely open");
        _bottomFlag = 1;
        delay(20);
    }
    if((digitalRead(_limSwitchBottom) == HIGH) && (_bottomFlag == 1)){
        Serial.println("Garage door not completely open");
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

void ServoDoor::changeServoAngle(int direction){
    int newAngle = 0;
    int currAngle = 0;
    currAngle = _servo.read();
    if (direction == _FORWARD){
        newAngle = currAngle + 5;
    } else if (direction == _BACKWARD){
        newAngle = currAngle - 5;
    }
    if (newAngle >= _maxAngle){
        // Serial.println("Max angle reached");
        newAngle = _maxAngle;
    } else if (newAngle <= _minAngle){
        newAngle = _minAngle;
    }
    Serial.print("New Angle: ");
    Serial.print(newAngle);
    Serial.print("\n");
    _servo.write(newAngle);
    delay(200);
}

void ServoDoor::testFunction(){
    // Make servo go to 0 degrees 
    Serial.println("In test function");
    _servo.write(0);
    Serial.println("moved 0");
    delay(2000); 
    // Make servo go to 90 degrees 
    _servo.write(90);
    Serial.println("moved 90");
    delay(2000); 
    // Make servo go to 180 degrees 
    _servo.write(-90); 
    Serial.println("moved -90");
    delay(2000);
    _servo.write(0);
    Serial.println("moved 0");
    delay(2000);
    Serial.println("Exiting test function");
}