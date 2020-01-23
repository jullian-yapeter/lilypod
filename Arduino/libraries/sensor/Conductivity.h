/*
  Conductivity.h - library for conductivity sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef Conductivity_h
#define Conductivity_h

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
