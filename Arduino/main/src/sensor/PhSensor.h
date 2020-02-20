/*
  PhSensor.h - library for pH sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef HEADER_PHSENSOR
#define HEADER_PHSENSOR

// library interface description
class PhSensor{
  // user-accessible "public" interface
  public:
    PhSensor(int PhSensorPin);
    float samplePh(void);
    unsigned long int _avgValue; 
    int _buf[10], _temp;
    int _PhSensorPin;

  // library-accessible "private" interface
  private:
    float readAvgAnalogValue(void);
    float convertAnalogtoPh(float avgValue);
    
};

#endif
