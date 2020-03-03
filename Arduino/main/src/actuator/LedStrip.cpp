#include "Arduino.h"
#include "LedStrip.h"


void LedStrip::setupStrip(int pinRed, int pinGreen, int PinBlue){
    _pinRed = pinRed;
    _pinGreen = pinGreen;
    _pinBlue = PinBlue;

    // Set up all the pins for output. Create pin vars for other funcs
    pinMode(_pinRed, OUTPUT);
    pinMode(_pinGreen, OUTPUT);
    pinMode(_pinBlue, OUTPUT);
    // Serial.println("LED Strip setup complete");
}

void LedStrip::shineRed(){
    analogWrite(_pinRed, _maxRed);
    analogWrite(_pinGreen, 0);
    analogWrite(_pinBlue, 0);
}

void LedStrip::shineGreen(){
    analogWrite(_pinRed, 0);
    analogWrite(_pinGreen, _maxGreen);
    analogWrite(_pinBlue, 0);
}

void LedStrip::shineBlue(){
    analogWrite(_pinRed, 0);
    analogWrite(_pinGreen, 0);
    analogWrite(_pinBlue, _maxBlue);
}

void LedStrip::shineWhite(){
    analogWrite(_pinRed, _maxRed);
    analogWrite(_pinGreen, _maxGreen);
    analogWrite(_pinBlue, _maxBlue);
}

void LedStrip::turnOff(){
    analogWrite(_pinRed, 0);
    analogWrite(_pinGreen, 0);
    analogWrite(_pinBlue, 0);
}

void LedStrip::testFunction(){
    shineRed();
    delay(2000);
    shineGreen();
    delay(2000);
    shineBlue();
    delay(2000);
    shineWhite();
    delay(2000);
    turnOff();
    delay(1000);
    shineWhite();
    delay(2000);
    turnOff();
    delay(1000);

}


