#ifndef HEADER_MOTOR
#define HEADER_MOTOR


class Motor{
    public:
        int _pin1;
        int _pin2;
        int _pinEn;

        void setupMotor(int pin1, int pin2, int pinEn);
        void start(int speed, int direction);
        void stop();
        void testFunction();

    private:
        int _FORWARD = 1;
        int _BACKWARD = 0;
        void setDirection(int direction);
        void setSpeed(int dutyCycle);
        int getPwmOutput(int dutyCycle);

};

#endif