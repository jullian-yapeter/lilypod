/*
  Garage.h - library for garage door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef Garage_h
#define Garage_h

// library interface description
class Garage
{
  // user-accessible "public" interface
  public:
    Garage();
    bool openGarage();
    bool closeGarage();
    
  // library-accessible "private" interface
  private:
    int pwmPin;	//initializing pin 2 as pwm
    int in1;
    int in2;
    int limitSwitchPinTop;
    int limitSwitchPinBottom;
    bool brakeGarage();
    bool waitForTopSwitch();
    bool waitForBottomSwitch();

};

#endif