#include "Arduino.h"
#include "LightBulb.h"


void LightBulb::setupLightBulb(int pinIn){
    _pinIn = pinIn;

    // Set up all the pins for output. Create pin vars for other funcs
    pinMode(_pinIn, OUTPUT);
    // Serial.println("Light Bulb setup complete");
}

float LightBulb::turnOn(){
    digitalWrite(_pinIn, HIGH);
    return 1.0;
}

float LightBulb::turnOff(){
    digitalWrite(_pinIn, LOW);
    return 0.0;
}

void LightBulb::testFunction(){
    turnOn();
    delay(2000);
    turnOff();
    delay(2000);
}


