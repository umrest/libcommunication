using System;

using comm;

namespace comm
{
public abstract class IdentifierInterface : RESTPacket{
    public IdentifierInterface()
    {

    }

           // Variables
    protected byte _identifier = new byte();


    // Offsets
    protected int IDENTIFIER_OFFSET = 0;


    // Type
    public override CommunicationDefinitions.TYPE type(){ return CommunicationDefinitions.TYPE.IDENTIFIER; }
    
};
} // namespace comm