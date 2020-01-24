/*
  Garage.h - library for garage door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef Garage_h
#define Garage_h

// library interface description
class Conductivity
{
  // user-accessible "public" interface
  public:
    Conductivity();
    void doSomething(void);
  // library-accessible "private" interface
  private:
    int value;
    void doSomethingSecret(void);
};

#endif