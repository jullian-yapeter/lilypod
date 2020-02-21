/*
  Serialcomm.h - library for conductivity sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef Serialcomm_h
#define Serialcomm_h
#include "Arduino.h"

union FLOATUNION_T{
    float val;
    byte b[4];
};

class Serialcomm
{
  // user-accessible "public" interface
  public:
    static const int messageLength = 10;
    Serialcomm();
    float cvt_b2f(byte* b, int startidx);
    bool cvt_bytes2floats(float* buf, byte* b);
    bool cvt_floats2bytes(byte* buf, float* vals);
    bool sendDataPacket();
    bool receiveCommandsData();
    bool setSensorData(float* data);
    bool sendSensorData();
    bool processCommandsData();
    bool getCommandsData(float* buf);
    bool mirrorReceiveData();
    bool runSerialComm();

  // library-accessible "private" interface
  private:
    float sensorData[messageLength];
    byte sensorBytesData[messageLength*4+2];
    float commandsData[messageLength];
};


#endif