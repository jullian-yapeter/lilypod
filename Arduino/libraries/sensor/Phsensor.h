/*
  Phsensor.h - library for pH sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef Phsensor_h
#define Phsensor_h

// library interface description
class Phsensor
{
  // user-accessible "public" interface
  public:
    Phsensor();
    void doSomething(void);
  // library-accessible "private" interface
  private:
    int value;
    void doSomethingSecret(void);
};

#endif
