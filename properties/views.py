from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from properties.utils import get_all_properties
from .models import Property

# Cache this view for 15 minutes (60 * 15 seconds)
@cache_page(60 * 15)
def property_list(request):
    """Fetches a list of properties and returns them as JSON.
    Caches the result for 15 minutes."""
    properties = get_all_properties()

    if properties:
        return JsonResponse(properties, safe=False)
    # Fetch all properties from the database

    properties = Property.objects.all().values(
        'id', 'title', 'description', 'price', 'location', 'created_at'
    )
    return JsonResponse(list(properties), safe=False)
