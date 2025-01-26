import importlib

props_asset_detail_1_list = ["CHR", "TBL", "LMP", "WIN"]
props_asset_detail_2_list = ["S", "M", "L"]

weapons_asset_detail_1_list = ["SWD", "BOW", "RFL", "EXP"]
weapons_asset_detail_2_list = ["COM", "RAR", "EPC"]

characters_asset_detail_1_list = ["PLR", "ENM", "CIV"]
characters_asset_detail_2_list = ["ML", "FL"]

def validate_name_props(asset_type_acronym, asset_type_detail_1, asset_type_detail_2,):
    is_validation_passed = None
    if asset_type_acronym != "PROP":
        is_validation_passed = False
    elif asset_type_detail_1 not in props_asset_detail_1_list:
        is_validation_passed = False
    elif asset_type_detail_2 not in props_asset_detail_2_list:
        is_validation_passed = False
    else: 
        is_validation_passed = True
    return is_validation_passed

def validate_name_weapons(asset_type_acronym, asset_type_detail_1, asset_type_detail_2,):
    is_validation_passed = None
    if asset_type_acronym != "WPN":
        is_validation_passed = False
    elif asset_type_detail_1 not in weapons_asset_detail_1_list:
        is_validation_passed = False
    elif asset_type_detail_2 not in weapons_asset_detail_2_list:
        is_validation_passed = False
    else: 
        is_validation_passed = True
    return is_validation_passed

def validate_name_characters(asset_type_acronym, asset_type_detail_1, asset_type_detail_2,):
    is_validation_passed = None
    if asset_type_acronym != "CHAR":
        is_validation_passed = False
    elif asset_type_detail_1 not in characters_asset_detail_1_list:
        is_validation_passed = False
    elif asset_type_detail_2 not in characters_asset_detail_2_list:
        is_validation_passed = False
    else: 
        is_validation_passed = True
    return is_validation_passed

def validate_name(asset_type, texture_set_name: str):
    texture_Set_name_acronyms = texture_set_name.split("_")
    # Template validation
    if len(texture_Set_name_acronyms) != 4: #Does not accept ANY more or less names than 4
        return False
    
    asset_type_acronym, asset_type_detail_1, asset_type_detail_2, asset_id = texture_Set_name_acronyms

    #Asset ID validation
    if (len(asset_id) != 2) or (not asset_id.isdigit()): #Does not accept ANY more or less digits than 2 or if the ID is not a number
        return False
    
    if asset_type == "Props":
        return validate_name_props(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    elif asset_type == "Weapons":
        return validate_name_weapons(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    elif asset_type == "Characters":
        return validate_name_characters(asset_type_acronym, asset_type_detail_1, asset_type_detail_2)
    
    return False
# importlib.reload(module_validation_name)
# texture_set_name = split("MyTextureSet") # splits the string into individual components
# asset_id.isdigit() #ensures that it is a number and not a string or any other format

