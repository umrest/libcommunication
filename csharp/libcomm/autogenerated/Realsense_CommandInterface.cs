using comm;

namespace comm
{
class Realsense_CommandInterface : RESTPacket{
    public Realsense_CommandInterface()
    {

    }

           // Variables
    protected byte _command;


    // Offsets
    protected int COMMAND_OFFSET = 0;


    // Type
    CommunicationDefinitions.TYPE type(){ return CommunicationDefinitions.TYPE.REALSENSE_COMMAND; }
    
};
} // namespace comm