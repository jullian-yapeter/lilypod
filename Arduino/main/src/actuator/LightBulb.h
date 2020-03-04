#ifndef HEADER_LIGHT_BULB
#define HEADER_LIGHT_BULB


class LightBulb{
    public:
        int _pinIn;

        void setupLightBulb(int pinIn);
        void turnOn();
        void turnOff();
        void testFunction();
};

#endif