/*
  Garage.h - library for garage door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

// include this library's description file
#include "Garage.h"

// Constructor /////////////////////////////////////////////////////////////////

Garage::Garage()
{
    pwmPin = 2;
    in1 = 8;
    in2 = 9;
    limitSwitchPinTop = 3;
    limitSwitchPinBottom = 4;

    pinMode(pwm,OUTPUT);  	//we have to set PWM pin as output
    pinMode(in_1,OUTPUT); 	//Logic pins are also set as output
    pinMode(in_2,OUTPUT);
    pinMode(limitSwitchPinTop,INPUT);
    pinMode(limitSwitchPinBottom,INPUT);
}

// Public Methods //////////////////////////////////////////////////////////////
// Assume opening the garage requires CW rotation
bool Garage::openGarage()
{
    digitalWrite(in_1,HIGH);
    digitalWrite(in_2,LOW);
    analogWrite(pwm,255);

    if (Garage::waitForTopSwitch() == true){
        Garage::brakeGarage();
        return true;
    }

    return false;
}

bool Garage::closeGarage()
{
    digitalWrite(in_1,LOW) ;
    digitalWrite(in_2,HIGH) ;
    analogWrite(pwm,255) ;

    if (Garage::waitForBottomSwitch() == true){
        Garage::brakeGarage();
        return true;
    }

    return false;
}

bool Garage::brakeGarage()
{
    digitalWrite(in_1,HIGH);
    digitalWrite(in_2,HIGH);
    delay(1000);

    return true;
}

bool Garage::waitForTopSwitch()
{
    while(digitalRead(limitSwitchPinTop)==LOW){};
    return true;
}

bool Garage::waitForBottomSwitch()
{
    while(digitalRead(limitSwitchPinBottom)==LOW){};
    return true;
}