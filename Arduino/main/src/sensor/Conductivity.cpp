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
    int condVal = analogRead(_probePin);
    float voltage = condVal*(5.0/1023.0);
    delay(50);
    Serial.print("conductivity: ");
    Serial.print(voltage);
    Serial.print("\n");
    return voltage;
}