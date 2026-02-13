from django.db import connections
from django.conf import settings
import redis

def check_database_status():
    try:
        connections['default'].cursor()
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

def check_redis_status():        
    try:
        r = redis.Redis(host=settings.REDIS_HOST, 
                        port=settings.REDIS_PORT, 
                        username=settings.REDIS_USER, 
                        password=settings.REDIS_PASSWORD,
                        socket_connect_timeout=2,
                        socket_timeout=2)
        
        r.ping()

        return True  # Redis is up and responding
    except Exception as e:
        print(f"Redis connection error: {e}")
        return False  # Redis is not responding or connection error occurred
