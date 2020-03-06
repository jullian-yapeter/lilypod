#include "Arduino.h"
#include "LightBulb.h"


void LightBulb::setupLightBulb(int pinIn){
    _pinIn = pinIn;

    // Set up all the pins for output. Create pin vars for other funcs
    pinMode(_pinIn, OUTPUT);
    // Serial.println("Light Bulb setup complete");
}

void LightBulb::turnOn(){
    digitalWrite(_pinIn, HIGH);
}

void LightBulb::turnOff(){
    digitalWrite(_pinIn, LOW);
}

void LightBulb::testFunction(){
    // Serial.println("Lightbulb on");
    turnOn();
    delay(2000);
    // Serial.println("Lightbulb off");
    turnOff();
    delay(2000);
}


