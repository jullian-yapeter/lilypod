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
    bytestream.DATAPACKET[7] = bytestream.STARTBYTE;
    Serial.write(bytestream.DATAPACKET,8);
}