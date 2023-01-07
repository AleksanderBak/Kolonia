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
    path("pojazdy", views.vehicle, name="vehicle"),
    path("pojazdy/new", views.vehicleNew, name="vehicle_new"),
    path("pojazdy/edit/<id>", views.vehicleEdit, name="vehicle_edit"),
    # Badania + Pojazdy
    # Wydarzenia
    path("wydarzenia", views.events, name="events"),
    path("wydarzenia/new", views.eventsNew, name="events_new"),
    path("wydarzenia/edit/<id>", views.eventsEdit, name="events_edit"),
    # Badania + Wydarzenia
    # Zadania
    path("zadania", views.tasks, name="tasks"),
    path("zadania/new", views.tasksNew, name="tasks_new"),
    path("zadania/edit/<id>", views.tasksEdit, name="tasks_edit"),
    # Zadania + Wydarzenia
    # Zadania + Pojazdy
    # Zadania + Pomieszczenia
    # Kolonizatorzy
    path("kolonizatorzy", views.people, name="people"),
    path("kolonizatorzy/new", views.peopleNew, name="people_new"),
    path("kolonizatorzy/edit/<id>", views.peopleEdit, name="people_edit"),
    # Kolonizatorzy + Badania
    # Kolonizatorzy + Zadania
    # Specjalizacje
    path("specjalizacje", views.specs, name="specs"),
    path("specjalizacje/new", views.specsNew, name="specs_new"),
    path("specjalizacje/edit/<id>", views.specsEdit, name="specs_edit"),
    # Doświadczenia Kolonizatorów
    path("staż", views.exp, name="exp"),
    path("staż/new", views.expNew, name="exp_new"),
    path("staż/edit/<id>", views.expEdit, name="exp_edit"),
]
