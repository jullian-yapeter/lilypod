/*
  ServoDoor.h - library for servo door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef HEADER_SERVO_DOOR
#define HEADER_SERVO_DOOR

#include <Servo.h>

// library interface description
class ServoDoor{
  // user-accessible "public" interface
  public:
    int _servoPin;
    int _limSwitchTop;
    int _limSwitchBottom;
    int _topFlag = 0;
    int _bottomFlag = 0;
    Servo _servo;
    void setupDoor(int servoPin, int limSwitchTop, int limSwitchBottom);
    void openDoor();
    void closeDoor();
    void testFunction();
    
    
  // library-accessible "private" interface
  private:
    const int _FORWARD = 1;
    const int _BACKWARD = 0;
    const int _maxAngle = 180;
    const int _minAngle = 0;
    void changeServoAngle(int direction);
    bool isTopSwitchClosed();
    bool isBottomSwitchClosed();

};

#endif