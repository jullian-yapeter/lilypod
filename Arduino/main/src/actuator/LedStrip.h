#ifndef HEADER_LED_STRIP
#define HEADER_LED_STRIP


class LedStrip{
    public:
        int _pinRed;
        int _pinGreen;
        int _pinBlue;

        void setupStrip(int pinRed, int pinGreen, int PinBlue);
        void shineRed();
        void shineGreen();
        void shineBlue();
        void shineWhite();
        void turnOff();
        void testFunction();

    private:
        const int _maxRed = 255;
        const int _maxGreen = 90;
        const int _maxBlue = 100;

};

#endif