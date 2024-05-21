import string
import random
import re

def create_short_url():
    characters = string.ascii_letters + string.digits
    short_url = "".join(random.choice(characters) for _ in range(6))
    return short_url

def is_valid_url(url: str) -> bool:
    if not isinstance(url, string):
        return False
    pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
    return bool(re.match(pattern, url))

def rate_limiter(group, request):
    return request.headers.get("user", "")