from django.urls import path
from . import views

app_name = "broker"

urlpatterns = [
    path("", views.list_brokers, name="list-brokers"),
    path("broker_detail/<int:id>/", views.broker_detail, name="broker_detail"),
    path("add/", views.add_broker, name="broker_add"),
    path("add_review/<int:broker_id>/", views.add_review, name="add_review"),
]
