'''to generate unique id'''
from uuid import uuid4

def generate_id(place:object):
    '''generating unique ID for each place'''
    place['id'] = uuid4()
    

def assign_catagory(place: object):
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

import uuid
import random

import random
import uuid

def generate_random_places(n):
    keywords = ['shop', 'retail', 'mart', 'croma', 'outlet', 'store', 'food', 'restaurant', 'hotel', 'fastfood', 'Finance', 'solutions', 'consultant', 'planner', 'healthcare', 'medical', 'labs', 'hospital', 'clinic']
    places = []

    for i in range(n):
        displayName = f"{random.choice(keywords)}{i + 1}"
        place = {
            'displayName': displayName,
            'formattedAddress': f"{random.randint(100, 999)} Main St, City, Country",
            'location': {'lat': round(random.uniform(-90, 90), 6), 'lng': round(random.uniform(-180, 180), 6)},
            'rating': round(random.uniform(1, 5), 1),
            'googleMapsUri': f"maplink/{displayName}",
            'businessStatus': random.choice(['OPERATIONAL', 'CLOSED_TEMPORARILY', 'CLOSED_PERMANENTLY']),
            'userRatingCount': random.randint(1, 1000),
            'uuid': str(uuid.uuid4())
        }
        places.append(place)
    
    return places

    
    
