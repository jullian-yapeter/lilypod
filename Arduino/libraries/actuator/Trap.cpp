/*
  Trap.h - library for trap door motor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

// include this library's description file
#include "Trap.h"

// Constructor /////////////////////////////////////////////////////////////////

Trap::Trap()
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
bool Trap::openTrap()
{
    digitalWrite(in_1,HIGH);
    digitalWrite(in_2,LOW);
    analogWrite(pwm,255);

    if (Garage::waitForTopSwitch() == true){
        Garage::brakeTrap();
        return true;
    }

    return false;
}

bool Trap::closeTrap()
{
    digitalWrite(in_1,LOW) ;
    digitalWrite(in_2,HIGH) ;
    analogWrite(pwm,255) ;

    if (Garage::waitForBottomSwitch() == true){
        Garage::brakeTrap();
        return true;
    }

    return false;
}

bool Trap::brakeTrap()
{
    digitalWrite(in_1,HIGH);
    digitalWrite(in_2,HIGH);
    delay(1000);

    return true;
}

bool Trap::waitForTopSwitch()
{
    while(digitalRead(limitSwitchPinTop)==LOW){};
    return true;
}

bool Trap::waitForBottomSwitch()
{
    while(digitalRead(limitSwitchPinBottom)==LOW){};
    return true;
}