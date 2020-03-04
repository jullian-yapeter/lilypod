/*
  Conductivity.h - library for conductivity sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef HEADER_CONDUCTIVITY
#define HEADER_CONDUCTIVITY

// library interface description
class Conductivity{
  // user-accessible "public" interface
  public:
    int _probePin;
    void setupConductivity(int probePin);
    float sampleConductivity();
  // library-accessible "private" interface
};

#endif
