"""Max allowed resolution for each asset type:
Props: 1024 x 1024
Weapons: 2048 x 2048
Characters: 4096 x 4096
Lower resolution is allowed."""

#Substance Painter API import
import substance_painter.logging
# Default Utils imports
from typing import Tuple

res_requirements = {
    "Props" : [1024, 1024],
    "Weapons" : [2048, 2048],
    "Characters" : [4096, 4096]
}

def get_required_res_from_asset_type(asset_type:str) -> Tuple[int, int]:
    """ Retrieves the required texture budget for the currently selected asset type. """
    required_res = res_requirements.get(asset_type)
    if required_res is None:
        strict_res_values = min(res_requirements.values(), key=sum) #Iteratively moves through the dictionary, adds their sums together and compares those sums to find the lowest value
        required_res_width, required_res_height = strict_res_values
        substance_painter.logging.log(severity = substance_painter.logging.WARNING, 
                                      channel = "Custom Exporter", 
                                      message = f"There is no resolution budget for the asset type {asset_type}. \
                                      Fallback to the default {required_res_width} x {required_res_height} resolution.")
    else:
        required_res_width, required_res_height = required_res
    return required_res_width, required_res_height

def validate_res(asset_type:str, current_texture_set_res:str) -> Tuple[bool, str]:
    """ Sub-validation function used for specific rules check applied to Texture Set resolutions. """
    is_validation_passed = None
    validation_details = None

    required_res_width, required_res_height = get_required_res_from_asset_type(asset_type)
    if current_texture_set_res.width > required_res_width or current_texture_set_res.height > required_res_height:
        is_validation_passed = False
        validation_details = f"Current resolution for Texture set is {current_texture_set_res.width} x {current_texture_set_res.height}, \
                            \nwhich is bigger than max allowed for current Asset Type ({asset_type}): \
                            \n{required_res_width} x {required_res_height}"
    else:
        is_validation_passed = True
        validation_details = "All validation checks passed!"
    return is_validation_passed, validation_details