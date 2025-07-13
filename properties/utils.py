from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging
logger = logging.getLogger(__name__)

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


def get_redis_cache_metrics():
    try:
        # Get a Redis connection from the default cache
        redis_conn = get_redis_connection("default")
        
        # Fetch Redis info stats
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses

        # Calculate hit ratio
        hit_ratio = (hits / total) if total > 0 else 0.0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 4),
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis cache metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0.0,
            "error": str(e)
        }
