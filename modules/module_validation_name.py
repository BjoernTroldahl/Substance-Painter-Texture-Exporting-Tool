"""
    Module to validate Texture Set name. 
    
    Rules:
    Name should be splitted with _
    Name should consist of acronyms: AssetType_AssetDetail1_AssetDetail2_AssetID
    
    For Props, details are Prop Type and Size/Scale:
        Prop Type could be: "CHR" (Chair), "TBL" (Table), LMP (Lamp), or WIN (Window).
        Prop Size/Scale could be: "S" (Small), "M" (Medium), or "L" (Large).
        Valid Texture Set names for Props:
            Prop_CHR_S_01
            Prop_BKL_M_02
    
    For Weapons, details are Weapon Type and Rarity:
        Weapon Type could be: "SWD: (Sword), "BOW" (Bow), "RFL" (Rifle), or "EXP" (Explosive).
        Weapon Rarity could be: "COM" (Common),  "RAR" (Rare), or "EPC" (Epic).
        Valid Texture Set names for Weapons:
            WPN_BOW_COM_01
            WPN_RLF_EPC_04
    
    For Character, details are Character Type and Gender
        Character Type could be: "PLR" (Player), "ENM" (Enemy), or "CIV" (Civilian).
        Character Gender could be: Male (ML), or Female (FL).
        Valid Texture Set names for Characters:
            CHAR_PLR_ML_01
            CHAR_CIV_FM_05

    Content:
        - validate_name
        - validate_name_props
        - validate_name_characters
        - validate_name_weapon

    Contributors:
        - Bjørn Troldahl, bjoerntrold@hotmail.com
"""

# Default Utils imports
from typing import Tuple

props_asset_detail_1_list = ["CHR", "TBL", "LMP", "WIN"]
props_asset_detail_2_list = ["S", "M", "L"]

weapons_asset_detail_1_list = ["SWD", "BOW", "RFL", "EXP"]
weapons_asset_detail_2_list = ["COM", "RAR", "EPC"]

characters_asset_detail_1_list = ["PLR", "ENM", "CIV"]
characters_asset_detail_2_list = ["ML", "FL"]

def validate_name_props(asset_type_acronym:str, asset_type_detail_1:str, asset_type_detail_2:str) -> Tuple[bool, str]:
    """ Sub-validation function used for specific rules check applied to Characters Texture sets. """
    is_validation_passed = None
    validation_details = None
    if asset_type_acronym != "PROP":
        is_validation_passed = False
        validation_details = f"First acronym is for Asset Type \
                                \nFor asset type 'Props' valid option is 'PROP' \
                                \nCurrent acronym is: {asset_type_acronym}"
    elif asset_type_detail_1 not in props_asset_detail_1_list:
        is_validation_passed = False
        validation_details = f"Second acronym is for Asset Detail #1 \
                                \nFor 'Props' valid options are {props_asset_detail_1_list} \
                                \nCurrent acronym is: {asset_type_detail_1}"
    elif asset_type_detail_2 not in props_asset_detail_2_list:
        is_validation_passed = False
        validation_details = f"Third acronym is for Asset Detail #2 \
                                \nFor 'Props' valid options are {props_asset_detail_2_list} \
                                \nCurrent acronym is: {asset_type_detail_2}"
    else: 
        is_validation_passed = True
        validation_details = "All validation checks passed!"
    return is_validation_passed, validation_details

def validate_name_weapons(asset_type_acronym:str, asset_type_detail_1:str, asset_type_detail_2:str) -> Tuple[bool, str]:
    """ Sub-validation function used for specific rules check applied to Weapons Texture sets. """
    is_validation_passed = None
    validation_details = None
    if asset_type_acronym != "WPN":
        is_validation_passed = False
        validation_details = f"First acronym is for Asset Type \
                                \nFor asset type 'Weapons' valid option is 'WPN' \
                                \nCurrent acronym is: {asset_type_acronym}"
    elif asset_type_detail_1 not in weapons_asset_detail_1_list:
        is_validation_passed = False
        validation_details = f"Second acronym is for Asset Detail #1 \
                                \nFor 'Weapons' valid options are {weapons_asset_detail_1_list} \
                                \nCurrent acronym is: {asset_type_detail_1}"
    elif asset_type_detail_2 not in weapons_asset_detail_2_list:
        is_validation_passed = False
        validation_details = f"Third acronym is for Asset Detail #2 \
                                \nFor 'Weapons' valid options are {weapons_asset_detail_2_list} \
                                \nCurrent acronym is: {asset_type_detail_2}"
    else: 
        is_validation_passed = True
        validation_details = "All validation checks passed!"
    return is_validation_passed, validation_details

def validate_name_characters(asset_type_acronym:str, asset_type_detail_1:str, asset_type_detail_2:str) -> Tuple[bool, str]:
    """ Sub-validation function used for specific rules check applied to Characters Texture sets. """
    is_validation_passed = None
    validation_details = None
    if asset_type_acronym != "CHAR":
        is_validation_passed = False
        validation_details = f"First acronym is for Asset Type \
                                \nFor asset type 'Characters' valid option is 'CHAR' \
                                \nCurrent acronym is: {asset_type_acronym}"
    elif asset_type_detail_1 not in characters_asset_detail_1_list:
        is_validation_passed = False
        validation_details = f"Second acronym is for Asset Detail #1 \
                                \nFor 'Characters' valid options are {characters_asset_detail_1_list} \
                                \nCurrent acronym is: {asset_type_detail_1}"
    elif asset_type_detail_2 not in characters_asset_detail_2_list:
        is_validation_passed = False
        validation_details = f"Third acronym is for Asset Detail #2 \
                                \nFor 'Characters' valid options are {characters_asset_detail_2_list} \
                                \nCurrent acronym is: {asset_type_detail_2}"
    else: 
        is_validation_passed = True
        validation_details = "All validation checks passed!"
    return is_validation_passed, validation_details

def validate_name(asset_type: str, texture_set_name: str) -> Tuple[bool, str]:
    """ 
    Core function to validate texture set name.
    Performs general rules validation and, if they are passed,
    triggers sub-validation functions for the specific asset type.
    """
    texture_set_name_acronyms = texture_set_name.split("_")
    # Template validation
    if len(texture_set_name_acronyms) != 4: #Does not accept ANY more or less names than 4
        return False, f"Texture Set name must consist of 4 acronyms separated by underscore symbol _ \
                        \nValid format: AssetType_AssetDetail1_AssetDetail2_AssetID \
                        \nCurrent number of acronyms: {len(texture_set_name_acronyms)}"
    
    asset_type_acronym, asset_type_detail_1, asset_type_detail_2, asset_id = texture_set_name_acronyms

    #Asset ID validation
    if (len(asset_id) != 2) or (not asset_id.isdigit()): #Does not accept ANY more or less digits than 2 or if the ID is not a number
        return False, f"Last acronym is used to specify Asset ID \
                        \nValid options are any numbers from rang 00 to 99. For example: 01, 55, 17 \
                        \nCurrent acronym is: {asset_id}"
    
    if asset_type == "Props":
        return validate_name_props(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    elif asset_type == "Weapons":
        return validate_name_weapons(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    elif asset_type == "Characters":
        return validate_name_characters(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    
    return False, f"General validation error. Asset type is not valid. \
                    \nThere is a mismatch between Asset Type in the Dropdown list of the widget and the strings in the validate_name function \
                    \nPlease contact a tool developer for further assistance"
