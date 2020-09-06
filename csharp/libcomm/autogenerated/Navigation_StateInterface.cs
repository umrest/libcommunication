using System;

using comm;

namespace comm
{
public abstract class Navigation_StateInterface : RESTPacket{
    public Navigation_StateInterface()
    {

    }

           // Variables
    protected Field_Position _field_position = new Field_Position();


    // Offsets
    protected int FIELD_POSITION_OFFSET = 0;


    // Type
    CommunicationDefinitions.TYPE type(){ return CommunicationDefinitions.TYPE.NAVIGATION_STATE; }
    
};
} // namespace comm