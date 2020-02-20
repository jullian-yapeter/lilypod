/*
  Garage.h - library for garage door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef HEADER_GARAGE
#define HEADER_GARAGE

#include <Servo.h>

// library interface description
class Garage
{
  // user-accessible "public" interface
  public:
    int _servoPin;
    int _limSwitchTop;
    int _limSwitchBottom;
    int _topFlag = 0;
    int _bottomFlag = 0;
    Servo _servo;
    void setupGarage(int servoPin, int limSwitchTop, int limSwitchBottom);
    void openGarage();
    void closeGarage();
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