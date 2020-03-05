/*
  Conductivity.h - library for conductivity sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

// include this library's description file
#include "Conductivity.h"
#include "Arduino.h"

void Conductivity::setupConductivity(int probePin){
    _probePin = probePin;
}

float Conductivity::sampleConductivity(){
    unsigned long int condVal;

    //Get 10 sample value from the sensor for smooth the value 
    for(int i = 0; i < 10; i++){
        _buf[i] = analogRead(_probePin);
        delay(20);
    }
    //sort the analog from small to large
    for(int i=0;i<9;i++){
        for(int j=i+1; j<10; j++){
            if(_buf[i] > _buf[j])
            {
                _temp = _buf[i];
                _buf[i] = _buf[j];
                _buf[j] = _temp;
            }
        }
    }
    condVal = 0;
    for(int i=2; i<8; i++){ //take the average value of 6 center sample
        condVal += _buf[i];
    }
    condVal /= 6;
    float adjustedCondVal = condVal*(1.0/500.0);
    // Serial.print("conductivity: ");
    // Serial.print(adjustedCondVal);
    // Serial.print("\n");
    return adjustedCondVal;
}