from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path("redirect/*", views.redirect_to_url, name="redirect"),
    path("shorten", view=views.shorten_url, name="shorten"),
    path("analytics", view=views.fetch_analytics, name="analytics")
]