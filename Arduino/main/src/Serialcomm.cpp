/*
  Serialcomm.h - library for pH sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

// include this library's description file
#include "Serialcomm.h"
#include "Arduino.h"

using namespace std;
// Constructor /////////////////////////////////////////////////////////////////

Serialcomm::Serialcomm(){

}

// Public Methods //////////////////////////////////////////////////////////////
//
float Serialcomm::cvt_b2f(byte* b, int startidx){
    FLOATUNION_T tempvar;
    for (int i=0; i<4; i++){
        tempvar.b[i] = b[startidx*4+i];
    }
    return tempvar.val;
}

bool Serialcomm::cvt_bytes2floats(float* buf, byte* b){
    for (int i = 0; i<messageLength; i++){
        buf[i] = cvt_b2f(b,i);
    }
    return true;
}

bool Serialcomm::cvt_floats2bytes(byte* buf, float* vals){
    buf[0] = 0xFE;
    for (int i = 0; i < messageLength; i++){
        FLOATUNION_T tempvar;
        tempvar.val = vals[i];
        for (int j = 0; j < 4; j++){
            buf[i*4+j+1]  = tempvar.b[j];
        }
    }
    buf[messageLength*4+2-1] = 0xFF;
    return true;
}

bool Serialcomm::receiveCommandsData(){
    while(!Serial.available()){}
    if(Serial.available()){
        byte rawCommandsData[messageLength*4+1] = {};
        byte startbyte = Serial.read();
        while (Serial.read() != 0xFA) {};
        int length = Serial.readBytes(rawCommandsData, messageLength*4+1);
        if (rawCommandsData[messageLength*4] == 0xFB){
            cvt_bytes2floats(commandsData, rawCommandsData);
        }
    }
  return true;
}

bool Serialcomm::setSensorData(float* data){
  for (int i = 0; i < messageLength; i++){
    sensorData[i] = data[i];
  }
  return true;
}

bool Serialcomm::sendSensorData(){
  cvt_floats2bytes(sensorBytesData, sensorData);
  Serial.write(sensorBytesData,messageLength*4+2);
}

bool Serialcomm::processCommandsData(){
  float sensorDataPrep[10] = {};
  for (int i = 0; i < messageLength; i++){
    // Process Data
    sensorDataPrep[i] = commandsData[i]+1;
  }
  setSensorData(sensorDataPrep);
  return true;
}

bool Serialcomm::getCommandsData(float* buf){
  for (int i = 0; i < messageLength; i++){
    buf[i] = commandsData[i];
  }
  return true;
}

bool Serialcomm::mirrorReceiveData(){
  receiveCommandsData();
  setSensorData(commandsData);
  sendSensorData();
  return true;
}

bool Serialcomm::runSerialComm(){
  receiveCommandsData();
  processCommandsData();
  sendSensorData();
  return true;
}