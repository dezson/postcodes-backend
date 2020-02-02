import math


def distance(origin, destination):
    """Haversine formula implementation"""
    lat1, lon1 = origin
    lat2, lon2 = destination
    earth_radius = 6371

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) * math.sin(d_lon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist = earth_radius * c
    return dist


def check_distance(lat1, long1, lat2, long2, radius):
    """Checking the radius between two given coordinates"""
    if None not in [lat1, long1, lat2, long2] and 0 <= float(radius) < 1000:
        dist = distance((lat1, long1), (lat2, long2))
        if dist <= radius:
            return True
    return False
