from http import HTTPStatus
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, Http404
from .models import URL
from .utils import create_short_url, is_valid_url, rate_limiter
from .constants import BASE_URL, API_RATE_LIMIT
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@ratelimit(key=rate_limiter, rate=API_RATE_LIMIT)
@csrf_exempt
def shorten_url(request):
    if request.method == "POST":
        user = request.headers.get("user", "")
        if user == "" or user is None:
            return JsonResponse(data={"message": "Request is not authenticated"}, status=HTTPStatus.BAD_REQUEST)
        # check if the url already exists
        original_url = request.POST.get("url")
        # vaidate if this is a valid url
        if (not original_url) or (original_url is None) or (not is_valid_url(original_url)):
            return JsonResponse(data={"message": "Invalid URL"}, status=HTTPStatus.BAD_REQUEST)
        # check if url already exists in the database
        try:
            url = get_object_or_404(URL, original_url=original_url, user_email=user)
            slug = url.shortened_url
            status = HTTPStatus.OK
        except (URL.DoesNotExist, Http404):
            slug = create_short_url()
            URL.objects.create(original_url=original_url, shortened_url=slug, user_email=user)
            status = HTTPStatus.CREATED
        url = f"{BASE_URL}/{slug}"
        return JsonResponse(data={"url": url}, status=status)
    return JsonResponse(data={"message": "Only POST request allowed"}, status=HTTPStatus.BAD_REQUEST)


@ratelimit(key="ip", rate=API_RATE_LIMIT)
def redirect_to_url(request):
    if request.method == "GET":
        slug = request.get_full_path().split("/")[-1]
        url = get_object_or_404(URL, shortened_url=slug)
        url.view_count += 1
        url.save()
        return redirect(url.original_url)
    return JsonResponse(data={"message": "Only GET request allowed"}, status=HTTPStatus.BAD_REQUEST)


@ratelimit(key=rate_limiter, rate=API_RATE_LIMIT)
def fetch_analytics(request):
    if request.method == "GET":
        user = request.headers.get("user", "")
        if user == "" or user is None:
            return JsonResponse(data={"message": "Request is not authenticated"}, status=HTTPStatus.BAD_REQUEST)
        data = URL.objects.filter(user_email=user)
        res = []
        for datum in data:
            res.append(
                {
                    "id": datum.id,
                    "url": datum.original_url,
                    "created_at": datum.created_at,
                    "num_views:": datum.view_count,
                }
            )
        return JsonResponse(data={"data": res}, status=HTTPStatus.OK)
    return JsonResponse(data={"message": "Only GET request allowed"}, status=HTTPStatus.BAD_REQUEST)
