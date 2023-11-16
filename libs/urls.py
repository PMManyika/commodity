from django.urls import path
from . import views

urlpatterns = [
    path("subscribe/", views.subscribe_to_newsletter, name="subscribe"),
    # Add other URL patterns as needed
]
