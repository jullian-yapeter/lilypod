/*
  PhSensor.h - library for pH sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

// include this library's description file
#include "PhSensor.h"

// Constructor /////////////////////////////////////////////////////////////////

PhSensor::PhSensor(int pHSensorPin){
  _phSensorPin = pHSensorPin;

}

// Public Methods //////////////////////////////////////////////////////////////

float PhSensor::samplePh(void){
    float avgValue = readAvgAnalogValue();
    float pHValue = convertAnalogtoPh(avgValue);
    Serial.print('pH Value: ');
    Serial.print(pHValue);
    Serial.print('\n');
    return pHValue;
}

// Private Methods /////////////////////////////////////////////////////////////
float PhSensor::readAvgAnalogValue(void){
    //Get 10 sample value from the sensor for smooth the value 
    unsigned long int avgValue;
    for(int i = 0; i < 10; i++){
        _buf[i] = analogRead(_phSensorPin);
        delay(10);
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
    for(int i=2; i<8; i++){ //take the average value of 6 center sample
        avgValue += _buf[i];
    }
    avgValue /= 6;
    return avgValue;
}

float PhSensor::convertAnalogtoPh(float avgValue){
    float phValue=(float) avgValue*5.0/1024; //convert the analog into millivolt
    phValue = 3.5 * phValue;
    return phValue;
}
