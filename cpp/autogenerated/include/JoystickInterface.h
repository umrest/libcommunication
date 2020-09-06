#pragma once

// Requirements
#include "RESTPacket.h"
#include "CommunicationDefinitions.h"
#include "BitArray8.h"


namespace comm
{
class JoystickInterface : public RESTPacket{
    public :
        JoystickInterface()
    {

    }
    // Variables
    BitArray8 _buttons_1;
BitArray8 _buttons_2;
int8 _lj_x;
int8 _lj_y;
int8 _rj_x;
int8 _rj_y;
int8 _lt;
int8 _rt;


    // Offsets
    int BUTTONS_1_OFFSET = 0;
int BUTTONS_2_OFFSET = 1;
int LJ_X_OFFSET = 2;
int LJ_Y_OFFSET = 3;
int RJ_X_OFFSET = 4;
int RJ_Y_OFFSET = 5;
int LT_OFFSET = 6;
int RT_OFFSET = 7;


    // Type
    CommunicationDefinitions::TYPE type(){ return CommunicationDefinitions::TYPE::JOYSTICK; }
};
} // namespace comm
