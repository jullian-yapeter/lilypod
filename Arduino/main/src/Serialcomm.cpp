/*
  Serialcomm.h - library for pH sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

// include this library's description file
#include "Serialcomm.h"

using namespace std;
// Constructor /////////////////////////////////////////////////////////////////

Serialcomm::Serialcomm()
{
    bytestream.STARTBYTE = 0xFF;
    bytestream.ENDBYTE = 0xFE;
}

// Public Methods //////////////////////////////////////////////////////////////
//
byte* Serialcomm::getDataPacket()
{
    return bytestream.DATAPACKET;
    return true;
}

bool Serialcomm::setDataPacket(int idx, byte* data)
{
    try {
        bytestream.DATAPACKET[idx] = *data;
    } catch (const exception& e) {
        cout << e.what();
        return false;
    }
    return true;
}

byte* Serialcomm::serializeData(float rawdata)
{
    byte* b = (byte*)&rawdata;
    return b;
}

bool Serialcomm::sendDataPacket()
{
    bytestream.DATAPACKET[0] = bytestream.STARTBYTE;
    bytestream.DATAPACKET[7] = bytestream.ENDBYTE;
    Serial.write(bytestream.DATAPACKET, numDataBytes);
}

byte* Serialcomm::readCommandsPacket()
{
    static byte index=0;
    
    if (Serial.available() > 0 ) {
        char inChar = Serial.read();
        
        if (inChar==bytestream.STARTBYTE) { // If start byte is received
            index=0; // then reset buffer and start fresh
        } else if (inChar==bytestream.ENDBYTE) { // If stop byte is received
            bytestream.COMMANDSPACKET[index] = '\0'; // then null terminate
            index=0; // this isn't necessary, but helps limit overflow
        } else { // otherwise
            bytestream.COMMANDSPACKET[index] = inChar; // put the character into our array
            index++; // and move to the next key in the array
        }
        
        /* Overflow occurs when there are more than 5 characters in between
            * the start and stop bytes. This has to do with having limited space
            * in our array. We chose to limit our array to 5 (+1 for null terminator)
            * because an int will never be above 5 characters */
        if (index >= numCommandBytes) {
            index=0;
            Serial.println("Overflow occured, next value is unreliable");
        }
}
