#include "Arduino.h"
#include "Motor.h"


void Motor::setupMotor(int pin1, int pin2, int pinEn){
    _pin1 = pin1;
    _pin2 = pin2;
    _pinEn = pinEn;

    // Set up all the pins for output. Create pin vars for other funcs
    pinMode(_pin1, OUTPUT);
    pinMode(_pin2, OUTPUT);
    pinMode(_pinEn, OUTPUT);
    // Serial.println("Motor setup complete");
}

void Motor::start(int speed, int direction){
    // Serial.println("Running pump");
    setDirection(direction);
    setSpeed(speed);
}

void Motor::stop(){
    // Serial.println("Stopping pump");
    setSpeed(0);
    digitalWrite(_pin1, LOW);
    digitalWrite(_pin2, LOW);

}

void Motor::setDirection(int direction){
    // direction == 1 is forward, 0 is backward
    if (direction == _FORWARD){
        digitalWrite(_pin1, HIGH);
        digitalWrite(_pin2, LOW);
    }else if (direction == _BACKWARD){
        digitalWrite(_pin1, LOW);
        digitalWrite(_pin2, HIGH);
    }
}

void Motor::setSpeed(int speed){
    int pwmOutput = getPwmOutput(speed);
    // Serial.print("pwmOutput: ");
    // Serial.print(pwmOutput);
    // Serial.print("\n");
    analogWrite(_pinEn, (int) pwmOutput);  // Send PWM signal to L298N Enable pin
}

int Motor::getPwmOutput(int dutyCycle){
  // int pwmOutput = map(dutyCycle, 0, 100, 0 , 255);
  return (((double)dutyCycle)/100.0) * 255.0;
}

void Motor::testFunction(){
    start(100, _FORWARD);
    // Serial.println("Moving Forward at 100");
    delay(5000);
    // start(60, _FORWARD);
    // // Serial.println("Moving Forward at 60");
    delay(5000);
    stop();
    // Serial.println("Stopped");
    delay(5000);
    start(100, _BACKWARD);
    // Serial.println("Moving Backward at 100");
    delay(5000);
    // start(60, _BACKWARD);
    // // Serial.println("Moving Backward at 60");
    delay(5000);
    stop();
    // Serial.println("Stopped");
    delay(5000);
    // Serial.println("Test complete.");
    // Serial.println("");
}