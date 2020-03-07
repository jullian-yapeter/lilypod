#ifndef HEADER_LED_STRIP
#define HEADER_LED_STRIP


class LedStrip{
    public:
        int _pinRed;
        int _pinGreen;
        int _pinBlue;

        void setupStrip(int pinRed, int pinGreen, int PinBlue);
        float shineRed();
        float shineGreen();
        float shineBlue();
        float shineWhite();
        float turnOff();
        void testFunction();

    private:
        // const int _maxRed = 255;
        // const int _maxGreen = 90;
        // const int _maxBlue = 100;
        const int _maxRed = 255;
        const int _maxGreen = 255;
        const int _maxBlue = 255;
        const int _newOffState = 4.0;
        const int _newRstate = 3.0;
        const int _newWState = 2.0;
        const int _newGState = 1.0;
        const int _newBState = 0.0;

};

#endif