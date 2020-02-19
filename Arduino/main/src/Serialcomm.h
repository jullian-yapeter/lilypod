/*
  Serialcomm.h - library for conductivity sensor interfacing
  Copyright (c) 2020 Team Lilypod.  All right reserved.
*/

#ifndef Serialcomm_h
#define Serialcomm_h

const int numDataBytes = 8;
const int numCommandBytes = 8;

struct Bytestream_t
{
    byte STARTBYTE;
    byte ENDBYTE;
    byte DATAPACKET[numDataBytes];
    byte COMMANDSPACKET[numCommandBytes];
};
// library interface description
class Serialcomm
{
  // user-accessible "public" interface
  public:
    Serialcomm();
    byte* getDataPacket();
    bool setDataPacket(int idx, byte* data);
    byte* serializeData(float rawdata);
    bool sendDataPacket();
    byte* readCommandsPacket();
  // library-accessible "private" interface
  private:
    Bytestream_t bytestream;
};


#endif
