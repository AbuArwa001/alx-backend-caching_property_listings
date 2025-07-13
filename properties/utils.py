from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get the cached queryset
    properties = cache.get('all_properties')
    
    if properties is None:
        print("Cache miss: Fetching from database")
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, timeout=3600)
    else:
        print("Cache hit: Returning cached data")

    return properties
