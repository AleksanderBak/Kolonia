from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Pomieszczenia
    path("pomieszczenia", views.rooms, name="rooms"),
    path("pomieszczenia/new", views.roomsNew, name="rooms_new"),
    path("pomieszczenia/<id>", views.roomsEdit, name="rooms_edit"),
    # Zasoby
    path("zasoby", views.resources, name="resources"),
    path("zasoby/new", views.resourcesNew, name="resources_new"),
    path("zasoby/<nazwa>", views.resourcesEdit, name="resources_edit"),
    # Pomieszczenia + Zasoby
    path("pomieszczenia_zasoby", views.roomRes, name="room_res"),
    path("pomieszczenia_zasoby/new", views.roomResNew, name="room_res_new"),
    path("pomieszczenia_zasoby/edit/<id>", views.roomResEdit, name="room_res_edit"),
    # Systemy
    path("systemy", views.systems, name="systems"),
    path("systemy/new", views.systemsNew, name="systems_new"),
    path("systemy/<id>", views.systemsEdit, name="systems_edit"),
    # Pomieszczenia + Systemy
    path("pomieszczenia_systemy", views.roomSys, name="room_sys"),
    path("pomieszczenia_systemy/new", views.roomSysNew, name="room_sys_new"),
    path("pomieszczenia_systemy/edit/<id>", views.roomSysEdit, name="room_sys_edit"),
    # Badania
    path("badania", views.research, name="research"),
    path("badania/new", views.researchNew, name="research_new"),
    path("badania/edit/<id>", views.researchEdit, name="research_edit"),
    # Badania + Pomieszczenia
    # Pojazdy
    # Badania + Pojazdy
    # Wydarzenia
    # Badania + Wydarzenia
    # Zadania
    # Zadania + Wydarzenia
    # Zadania + Pojazdy
    # Zadania + Pomieszczenia
    # Kolonizatorzy
    # Kolonizatorzy + Badania
    # Kolonizatorzy + Zadania
    # Specjalizacje
    # Doświadczenia Kolonizatorów
]
