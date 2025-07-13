from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from properties.utils import get_all_properties
from .models import Property

# Cache this view for 15 minutes (60 * 15 seconds)
@cache_page(60 * 15)
def property_list(request):
    """Fetches a list of properties and returns them as JSON.
    Caches the result for 15 minutes."""
    properties = get_all_properties()
    if not properties:
        return JsonResponse({'error': 'No properties found'}, status=404)
    return JsonResponse({
        'properties': list(properties)
    })
