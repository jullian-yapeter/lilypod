#ifndef HEADER_LIGHT_BULB
#define HEADER_LIGHT_BULB


class LightBulb{
    public:
        int _pinIn;

        void setupLightBulb(int pinIn);
        float turnOn();
        float turnOff();
        void testFunction();
};

#endif