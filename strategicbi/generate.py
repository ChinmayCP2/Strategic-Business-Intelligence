import random
import uuid


def generate_random_places(n):
    keywords = ['shop', 'retail', 'mart', 'croma', 'outlet', 'store',
                 'food', 'restaurant', 'hotel', 'fastfood', 'Finance',
                   'solutions', 'consultant', 'planner', 'healthcare',
                     'medical', 'labs', 'hospital', 'clinic','education',
                       'school', 'college', 'university', 'institute']
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

    
    
