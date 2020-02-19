/*
  Trap.h - library for trap door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef Trap_h
#define Trap_h

// library interface description
class Trap
{
  // user-accessible "public" interface
  public:
    Trap();
    bool openTrap();
    bool closeTrap();
    
  // library-accessible "private" interface
  private:
    int pwmPin;	//initializing pin 2 as pwm
    int in1;
    int in2;
    int limitSwitchPinTop;
    int limitSwitchPinBottom;
    bool brakeTrap();
    bool waitForTopSwitch();
    bool waitForBottomSwitch();

};

#endif