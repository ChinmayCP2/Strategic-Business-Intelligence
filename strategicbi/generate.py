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
        print(display_name)
        for primary_type, keywords in type_mapping.items():
            if any(keyword in display_name for keyword in keywords):
                place['primaryType'] = primary_type    
                display_name_changed = True
                break

    # If no match is found, set primaryType to 'other'
    if not display_name_changed:
        place['primaryType'] = 'other'

    
    
