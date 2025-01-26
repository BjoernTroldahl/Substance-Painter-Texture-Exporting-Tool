# Substance Painter API import 
import substance_painter

# Default utils imports
from math import log2
from os import startfile

def get_export_preset_from_shader_type(shader_type):
    custom_export_presets = {
        "Basic" : "Custom_Basic",
        "Armament" : "Custom_Armament",
        "Morph" : "Custom_Morph",
        }

    export_preset_name = custom_export_presets.get(shader_type)
    if export_preset_name is None:
        substance_painter.logging.log(substance_painter.logging.ERROR, "Custom Exporter", f"There is no export preset for the specified shader type {shader_type}")
    return export_preset_name
                                                       

def build_export_config(texture_set_name, shader_type, export_path):
    texture_set = substance_painter.textureset.TextureSet.from_name(texture_set_name)
    texture_set_stack = texture_set.get_stack()

    export_preset_name = get_export_preset_from_shader_type(shader_type)

    export_preset_id = substance_painter.resource.ResourceID("custom_lib", export_preset_name)

    resolution = texture_set.get_resolution()
    resolution = [log2(resolution.width), log2(resolution.height)]

    export_config = {
    "exportShaderParams": False,
    "exportPath": export_path,
    "defaultExportPreset" : export_preset_id.url(),
    "exportList": [
        {
            "rootPath": str(texture_set_stack)
        }
        ],
    "exportParameters": [
        # No filters: those parameters apply to all exported maps
        {
            "parameters": {
                "paddingAlgorithm": "infinite",
                "sizeLog2": resolution
            }
        },
        ]
    }
    return export_config

def open_explorer_at_path(path):
    startfile(path)

def exporting(texture_set_name, shader_type, export_path):
    if not substance_painter.project.is_open():
        return
    
    export_config = build_export_config(texture_set_name, shader_type, export_path)
    
    substance_painter.logging.log(substance_painter.logging.INFO, "Custom Exporter", "Performing Texture Exporting!")
    export_result = substance_painter.export.export_project_textures(export_config) 

    # In case of error, display a human readable message: 
    if export_result.status == substance_painter.export.ExportStatus.Success: 
        open_explorer_at_path(export_path)
    else:
        substance_painter.logging.log(substance_painter.logging.WARNING, "Custom Exporter", export_result.message)
        print(export_result.message) 

    # Display the details of what was exported: 
    for k,v in export_result.textures.items(): 
        substance_painter.logging.log(substance_painter.logging.INFO, "Custom Exporter", f"Stack {k}:")
        for exported in v:
            substance_painter.logging.log(substance_painter.logging.INFO, "Custom Exporter", exported)

