"""
Produces orcaflex .yml (text) files
Each file is an alteration of the number of supports, friction coefficient and support size
filenames formatted to indicate variable differences
friction_coefficient_number-of-supports_support-size.yml
0.3_5_25.yml
"""

import math

ORIGINAL_NUMBER_OF_SUPPORTS = 5
FRICTION_COEFFICIENTS = [0.3, 0.4, 0.5]
NUMBER_OF_SUPPORTS = [5, 6, 7]
SUPPORT_SIZE = [25, 30, 35]

def calculate_octagon_side_length():
    # 2.414 = (1 + math.sqrt(2))
    return (SIZE / 2.414) / 1000 # divide by 1000 to convert from millimetre to metre

def get_user_support_length_text():
    """Example Text Format:
    SupportTypes:
        main_support:
            UserSupportLength[1]: 0.014497474683058327
            UserSupportLength[2]: 0.014497474683058327
            UserSupportLength[3]: 0.014497474683058327
            UserSupportLength[4]: 0.014497474683058327
            UserSupportLength[5]: 0.014497474683058327
    """
    user_support_length_text = """"""

    octagon_side_length = calculate_octagon_side_length()

    for z in range(5): # model defined 'main support' has 5 support segments
        user_support_length_text += f'    UserSupportLength[{z+1}]: {octagon_side_length}\n' # spacing required for correct indentation
    return user_support_length_text.rstrip('\n') 

def get_support_arclengths():
    """Calculates a list of x-axis positions for a given number of supports"""
    
    support_arclengths = [0]

    arclength = 4 / (NUMBER - 1)

    for y in range(NUMBER-1):
        gap_distance = support_arclengths[y] + arclength

        support_arclengths.append(gap_distance)
    
    return support_arclengths

def get_support_text_part1(support_arclengths, z_offset):
    """Example Text Format:
    NumberOfSupports: 5
    SupportArcLength[1]: 0 
    SupportzOffset[1]: -0.0175
    SupportArcLength[2]: 1.0 
    SupportzOffset[2]: -0.0175
    SupportArcLength[3]: 2.0 
    SupportzOffset[3]: -0.0175
    SupportArcLength[4]: 3.0 
    SupportzOffset[4]: -0.0175
    SupportArcLength[5]: 4.0 
    SupportzOffset[5]: -0.0175 
    """
    support_text_part1 = f"""NumberOfSupports: {NUMBER}\n"""

    for x in range(ORIGINAL_NUMBER_OF_SUPPORTS):
        support_number = x + 1 # OrcaFlex indexing starts at 1
        
        support_text_part1 += f"""    SupportArcLength[{support_number}]: {support_arclengths[x]}
    SupportzOffset[{support_number}]: {z_offset}\n""" # spacing required for correct indentation
    
    return support_text_part1, x # index required for correct listing convention in get_support_text_part2()

def get_support_text_part2(x, support_arclengths, z_offset, support_text_part1):
    """Example Text Format:
    SupportType[6]: main_support
    SupportArcLength[6]: 3.333333333333333
    SupportzOffset[6]: -0.0175
    SupportType[7]: main_support
    SupportArcLength[7]: 3.9999999999999996
    SupportzOffset[7]: -0.0175 
    """
    support_text = support_text_part1

    if NUMBER > ORIGINAL_NUMBER_OF_SUPPORTS: # parent model has 5 supports, additional supports required additional syntax
        x += 1

        while x < NUMBER:
            support_number = x + 1 

            support_text += f"""    SupportType[{support_number}]: main_support
    SupportArcLength[{support_number}]: {support_arclengths[x]}
    SupportzOffset[{support_number}]: {z_offset}\n""" # spacing required for correct indentation
            
            x += 1

    return support_text

def get_support_text():
    """Example Text Format:
    6DBuoys:
        supports:
            NumberOfSupports: 6
            SupportArcLength[1]: 0 
            SupportzOffset[1]: -0.015
            SupportArcLength[2]: 0.8 
            SupportzOffset[2]: -0.015
            SupportArcLength[3]: 1.6 
            SupportzOffset[3]: -0.015
            SupportArcLength[4]: 2.4000000000000004 
            SupportzOffset[4]: -0.015
            SupportArcLength[5]: 3.2 
            SupportzOffset[5]: -0.015
            SupportType[6]: main_support
            SupportArcLength[6]: 4.0
            SupportzOffset[6]: -0.015 
    """
    support_arclengths = get_support_arclengths()

    z_offset = -(SIZE/2000)

    support_text_part1, x = get_support_text_part1(support_arclengths, z_offset)

    support_text = get_support_text_part2(x, support_arclengths, z_offset, support_text_part1)
    
    return support_text.rstrip('\n')

def format_text():
    
    content = f"""%YAML 1.1
# Type: Model
# Program: OrcaFlex 11.3d
---
BaseFile: 0_initial_model.dat
SupportTypes:
  main_support:
{get_user_support_length_text()}
6DBuoys:
  supports:
    {get_support_text()} 
FrictionCoefficients:
  SupportTypeLateralCoefficient[1]: {COEFFICIENT}
...
"""
    return content

for COEFFICIENT in FRICTION_COEFFICIENTS:
    for NUMBER in NUMBER_OF_SUPPORTS:
        for SIZE in SUPPORT_SIZE:

            FILENAME = f"{COEFFICIENT}_{NUMBER}_{SIZE}.yml"

            content = format_text()

            with open(FILENAME, 'w') as f:
                f.write(content)
