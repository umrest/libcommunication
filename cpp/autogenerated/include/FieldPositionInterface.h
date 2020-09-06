#pragma once

// Requirements
#include "RESTPacket.h"
#include "CommunicationDefinitions.h"
#include "int16.h"
#include "int16.h"
#include "int16.h"


namespace comm
{
class FieldPositionInterface : public RESTPacket{
    public :
        FieldPositionInterface()
    {

    }
    // Variables
    int16 _yaw;
int16 _x;
int16 _y;


    // Offsets
    int YAW_OFFSET = 0;
int X_OFFSET = 1;
int Y_OFFSET = 2;


    // Type
    int16 _yaw;
int16 _x;
int16 _y;

};
} // namespace comm
