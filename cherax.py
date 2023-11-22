import json
import re
from time import time
from datetime import datetime

with open("natives.json") as f:
    json_object = f.read()
    f.close()

data = json.loads(json_object)

native_file = open('natives.lua', "w")

func_match = {
    "void": "InvokeVoid",
    "int": "InvokeInt",
    "float": "InvokeFloat",
    "BOOL": "InvokeBool",
    "Vector3": "InvokeV3",
    "const char*": "InvokeString"
}


formats = """
Natives[\"{}\"][\"{}\"] = function ({})
    {} Natives.{}({}{})
end
"""
def parse_function_arguments(params):
    argument_names = [param["name"] if param["name"] not in {"end", "repeat"} else f"_{param['name']}" for param in params]
    return ", ".join(argument_names)


def capitalize_after_underscore(s):
	split_str = s.split('_')
	split_str = [word.capitalize() for word in split_str]
	return '_'.join(split_str)

def fivem_format(m_str):
	return re.sub("\_", "", capitalize_after_underscore(m_str.lower()))

start_time = time()
native_file.write('-- Generated @ {}\n'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
for section_name, section_data in data.items():
    formatted_section = fivem_format(section_name)
    native_file.write(f"Natives[\"{formatted_section}\"] = {{}}\n")
    for hash, entry in section_data.items():
        params = parse_function_arguments(entry["params"]) if entry["params"] else ""
        m_hash = f"{hash}, " if params else hash
        m_comment = entry["comment"]
        if(m_comment != ""):
            native_file.write('-- ' + '\n-- '.join(m_comment.splitlines()))
        native_file.write( 
            formats.format(
                formatted_section,
                fivem_format(entry["name"]), 
                params, 
                "" if entry["return_type"] == "void" else "return" + " ", 
                func_match.get(entry["return_type"], "InvokeInt"), 
                m_hash,
                params
            )
        )
native_file.close()
end_time = time()
print("Done! Generated native.lua in {:.2f} seconds".format(end_time - start_time))
