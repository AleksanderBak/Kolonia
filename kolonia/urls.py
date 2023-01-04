from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("pomieszczenia", views.rooms, name="rooms"),
    path("pomieszczenia/new", views.roomsNew, name="rooms_new"),
    path("pomieszczenia/<id>", views.roomsEdit, name="rooms_edit"),
]
