#include "Arduino.h"
#include "Sonar.h"


void Sonar::setupSonar(int trigPin1, int echoPin1){

    // Ultrasonic Sensor HC-SR04
    pinMode(trigPin1, OUTPUT);
    pinMode(echoPin1, INPUT);

    _trigPin = trigPin1;
    _echoPin = echoPin1;

    Serial.println( "Sonar Setup Complete" );
}

long Sonar::findGarbageCapacity(){
    // Clears the trigPin
    digitalWrite(_trigPin, LOW);
    delayMicroseconds(2);

    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(_trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(_trigPin, LOW);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    unsigned duration = pulseIn(_echoPin, HIGH);

    // Calculating the distance
    unsigned distance = duration*0.034/2.0;
    // Serial.print("Sonar: ");
    // Serial.print(distance);
    // Serial.print("\n");

    return distance;
}

bool Sonar::isGarbageFull(){
    unsigned capacity = findGarbageCapacity();
    bool isFull = false;
    if (capacity <= _garbageThreshold){
        isFull = true;
        Serial.println("Garbage is full");
    }else{
        Serial.print("Garbage capacity: ");
        Serial.print(capacity);
        Serial.print("\n");
    }

    return isFull;
}