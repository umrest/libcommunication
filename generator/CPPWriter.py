import os

from helpers import *

class CPPFieldAccessorWriter:
    def __init__(self, message):
        self.message = message
    
    def accessor_type(self, field):
        if field.accessor:
            if field.accessor.type == "float":
                return "float"
        return field.type
    
    def get_getter2(self, field):
        if field.accessor.type == "bit":
            return f"_{field.bit_array.name}.GetBit({field.idx});"
        if field.accessor.type == "float":
            return f"return other / {field.accessor.scale};"
        return f"_{field.name} = other;"
    
    def get_getter(self, field):
        if field.accessor.type == "bits":
            ret = ""
            for bit in field.accessor.bits:
                ret += self.get_getter(bit)
            return ret
        
        return f"""{self.accessor_type(field)} get_{field.name}(){{
                {self.get_getter2(field)}
            }};\n"""
    
    def get_setter2(self, field):
        if field.accessor.type == "bit":
            return f"_{field.name}.SetBit({field.idx}, other);"
        if field.accessor.type == "float":
            return f"_{field.name} = other * {field.accessor.scale};"
        return f"_{field.name} = other;"
        
    def get_setter(self, field):
        if field.accessor.type == "bits":
            ret = ""
            for bit in field.accessor.bits:
                ret += self.get_setter(bit)
            return ret
        
        return f"""void set_{field.name}({self.accessor_type(field)} other){{
                {self.get_setter2(field)}
            }};\n"""

class CPPMessageWriter:
    def __init__(self, templates_dir, include_dir, src_dir, message, communication_definitions):
        self.templates_dir = templates_dir
        self.include_dir = include_dir
        self.src_dir = src_dir
        self.message = message
        self.communication_definitions = communication_definitions
    
    def get_requirements(self, interface = False):
        if interface:
            return f'#include "{self.message.name}Interface.h"\n'
        
        required_types = set()
        ret = ""
        for field in self.message.fields:
            if not is_primitive(field.type):
                required_types.add(field.type)
        for t in required_types:
            ret += f'#include "{t}.h"\n'
        return ret
    
    def get_accessors(self):
        ret = ""
        writer = CPPFieldAccessorWriter(self.message)
        for field in self.message.fields:
            ret += writer.get_getter(field)
        ret += "\n"
        for field in self.message.fields:
            ret += writer.get_setter(field)
        return ret
    
    def get_serializers(self):
        return ""
    
    def get_deserializers(self):
        return ""
    
    def get_variables(self):
        ret = ""
        for field in self.message.fields:
            ret += f'{field.type} _{field.name};\n'
        return ret
    
    def get_offsets(self):
        ret = ""
        offset = 0
        for field in self.message.fields:
            ret += f'int {field.name.upper()}_OFFSET = {offset};\n'
            offset += self.communication_definitions["PACKET_SIZES"][field.type.upper()]
        return ret
    
    def get_type(self):
        return f"CommunicationDefinitions::TYPE type(){{ return CommunicationDefinitions::TYPE::{self.message.name.upper()}; }}"

    def write(self):
        template = open(os.path.join(self.templates_dir, "Packet.Interface.Template.txt")).read()
        
        template = template.replace("[[InterfaceType]]", self.message.name + "Interface")
        template = template.replace("[[Requirements]]", self.get_requirements())
        template = template.replace("[[Variables]]", self.get_variables())
        template = template.replace("[[Offsets]]", self.get_offsets())

        template = template.replace("[[Type]]", self.get_type())
        open(os.path.join(self.include_dir, self.message.name + "Interface" + ".h"), "w").write(template)

        
        template = open(os.path.join(self.templates_dir, "Packet.Template.txt")).read()
        template = template.replace("[[InterfaceType]]", self.message.name + "Interface")
        template = template.replace("[[MessageType]]", self.message.name)
        template = template.replace("[[Requirements]]",self.get_requirements(True))
        template = template.replace("[[Accessors]]", self.get_accessors())

        template = template.replace("[[Serializers]]", self.get_serializers() + self.get_deserializers())

        open(os.path.join(self.include_dir, self.message.name + ".h"), "w").write(template)
        


class CPPCommunicationDefinitionsWriter:
    def __init__(self, templates_dir, include_dir, src_dir):
        self.templates_dir = templates_dir
        self.include_dir = include_dir
        self.src_dir = src_dir

    
    def get_enum_header2(self, enum):
        ret = ""
        for key, value in enum.items():
            ret += f"{key} = {value};\n"

        return ret

    def get_enum_header(self, enum, name):
        ret = f"""enum class {name}
                {{
                    {self.get_enum_header2(enum)}
                }}"""
        return ret
    
    def get_map_header(self, map, name):
        return f"""
                """

    def get_map_source2(self, map):
        ret = ""
        for key, value in map.items():
            if (not is_primitive(key)):
                ret += f"{{TYPE::{key}, {value}}},\n"

        return ret

    def get_map_source(self, map, name):
        return f"""
        const std::map<CommunicationDefinitions::TYPE, int> CommunicationDefinitions::PACKET_SIZES = {{
            {self.get_map_source2(map)}
        }};
                """
    
    def write(self, communication_definitions):
        template = open(os.path.join(self.templates_dir, "CommunicationDefinitions.Template.h")).read()
        template = template.replace("[[ENUMS]]", self.get_enum_header(communication_definitions["TYPES"], "TYPE") + "\n" + self.get_enum_header(communication_definitions["IDENTIFIERS"], "IDENTIFIER"))
        template = template.replace("[[MAPS]]", self.get_map_header(communication_definitions["PACKET_SIZES"], "PACKET_SIZES"))
        open(os.path.join(self.include_dir, "CommunicationDefinitions.h"), "w").write(template)

        template = open(os.path.join(self.templates_dir, "CommunicationDefinitions.Template.cpp")).read()
        template = template.replace("[[MAPS]]", self.get_map_source(communication_definitions["PACKET_SIZES"], "PACKET_SIZES"))
        open(os.path.join(self.src_dir, "CommunicationDefinitions.cpp"), "w").write(template)


class CPPWriter:
    def __init__(self, cpp_dir):
        self.include_dir = os.path.join(cpp_dir, "autogenerated/include")
        self.src_dir = os.path.join(cpp_dir, "autogenerated/src")
        self.templates_dir = os.path.join(cpp_dir, "templates")

    def run(self, messages, communication_definitions):
        for message in messages:
            CPPMessageWriter(self.templates_dir, self.include_dir, self.src_dir, message, communication_definitions).write()
        
        CPPCommunicationDefinitionsWriter(self.templates_dir, self.include_dir, self.src_dir).write(communication_definitions)    