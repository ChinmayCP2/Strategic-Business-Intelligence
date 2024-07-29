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
        'hospital': ['hospital'],
        'retail': ['shop', 'retail', 'mart'],
        'food': ['food', 'restaurant', 'hotel'],
        'finance': ['Finance', 'solutions'],
        'healthcare': ['healthcare', 'medical']
    }
    display_name_changed = False
    if 'displayName' in place and 'text' in place['displayName']:
        display_name = str(place['displayName']['text']).lower()
        # Iterate over the type mapping
        for catagory, keywords in type_mapping.items():
            for keyword in keywords:
                if keyword.lower() in display_name:  # Convert keyword to lowercase for case-insensitive match
                    place['catagory'] = catagory
                    place['primaryType'] = keyword
                    display_name_changed = True
                    break


    # If no match is found, set primaryType to 'other'
    if not display_name_changed:
        place['catagory'] = 'other'
        place['primaryType'] = 'other'

    
    
