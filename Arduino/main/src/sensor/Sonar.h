#ifndef HEADER_SONAR
#define HEADER_SONAR

#include "Arduino.h"

class Sonar{    
    public:
        void setupSonar(int trigPin1, int echoPin1);
        long findGarbageCapacity();
        bool isGarbageFull();
        int _trigPin;
        int _echoPin;
        int _garbageThreshold = 15;

};

#endif