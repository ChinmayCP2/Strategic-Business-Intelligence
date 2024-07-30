'''to generate unique id'''
from uuid import uuid4

def generate_id(place:object):
    '''generating unique ID for each place'''
    place['id'] = uuid4()
    

def generate_primary_type(place: object):
    """
    Generate primary type for each place
    """
    # dictionary mapping
    type_mapping = {
        'retail': ['shop', 'retail', 'mart', 'croma', 'oulet', 'store'],
        'food': ['food', 'restaurant', 'hotel', 'fastfood', ],
        'finance': ['Finance', 'solutions', 'consultant', 'planner'],
        'healthcare': ['healthcare', 'medical', 'labs', 'hospital','clinic']
    }
    display_name_changed = False
    if 'displayName' in place and 'text' in place['displayName']:
        display_name = str(place['displayName']['text']).lower()
        # Iterate over the type mapping
        for catagory, keywords in type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in display_name:
                    # print(catagory, keyword)  # Convert keyword to lowercase for case-insensitive match
                    place['catagory'] = catagory
                    place['keyword'] = keyword
                    display_name_changed = True
                    break


    # If no match is found, set primaryType to 'other'
    if not display_name_changed:
        place['catagory'] = 'other'
        place['primaryType'] = 'other'

    
    
