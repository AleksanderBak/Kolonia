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
    path("badania_pomieszczenia", views.researchesRooms, name="researches_rooms"),
    path(
        "badania_pomieszczenia/new",
        views.researchesRoomsNew,
        name="researches_rooms_new",
    ),
    path(
        "badania_pomieszczenia/edit/<id>",
        views.researchesRoomsEdit,
        name="researches_rooms_edit",
    ),
    # Pojazdy
    path("pojazdy", views.vehicle, name="vehicle"),
    path("pojazdy/new", views.vehicleNew, name="vehicle_new"),
    path("pojazdy/edit/<id>", views.vehicleEdit, name="vehicle_edit"),
    # Badania + Pojazdy
    path("badania_pojazdy", views.researchesVehicles, name="researches_vehicles"),
    path(
        "badania_pojazdy/new",
        views.researchesVehiclesNew,
        name="researches_vehicles_new",
    ),
    path(
        "badania_pojazdy/edit/<id>",
        views.researchesVehiclesEdit,
        name="researches_vehicles_edit",
    ),
    # Wydarzenia
    path("wydarzenia", views.events, name="events"),
    path("wydarzenia/new", views.eventsNew, name="events_new"),
    path("wydarzenia/edit/<id>", views.eventsEdit, name="events_edit"),
    # Badania + Wydarzenia
    path("badania_wydarzenia", views.researchesEvents, name="researches_events"),
    path(
        "badania_wydarzenia/new",
        views.researchesEventsNew,
        name="researches_events_new",
    ),
    path(
        "badania_wydarzenia/edit/<id>",
        views.researchesEventsEdit,
        name="researches_events_edit",
    ),
    # Zadania
    path("zadania", views.tasks, name="tasks"),
    path("zadania/new", views.tasksNew, name="tasks_new"),
    path("zadania/edit/<id>", views.tasksEdit, name="tasks_edit"),
    # Zadania + Wydarzenia
    path("zadania_wydarzenia", views.tasksEvents, name="tasks_events"),
    path("zadania_wydarzenia/new", views.tasksEventsNew, name="tasks_events_new"),
    path(
        "zadania_wydarzenia/edit/<id>", views.tasksEventsEdit, name="tasks_events_edit"
    ),
    # Zadania + Pojazdy
    path("zadania_pojazdy", views.tasksVehicles, name="tasks_vehicles"),
    path("zadania_pojazdy/new", views.tasksVehiclesNew, name="tasks_vehicles_new"),
    path(
        "zadania_pojazdy/edit/<id>", views.tasksVehiclesEdit, name="tasks_vehicles_edit"
    ),
    # Zadania + Pomieszczenia
    path("zadania_pomieszczenia", views.tasksRooms, name="tasks_rooms"),
    path("zadania_pomieszczenia/new", views.tasksRoomsNew, name="tasks_rooms_new"),
    path(
        "zadania_pomieszczenia/edit/<id>",
        views.tasksRoomsEdit,
        name="tasks_rooms_edit",
    ),
    # Kolonizatorzy
    path("kolonizatorzy", views.people, name="people"),
    path("kolonizatorzy/new", views.peopleNew, name="people_new"),
    path("kolonizatorzy/edit/<id>", views.peopleEdit, name="people_edit"),
    # Kolonizatorzy + Badania
    path("kolonizatorzy_badania", views.peopleResearch, name="people_research"),
    path(
        "kolonizatorzy_badania/new", views.peopleResearchNew, name="people_research_new"
    ),
    path(
        "kolonizatorzy_badania/edit/<id>",
        views.peopleResearchEdit,
        name="people_research_edit",
    ),
    # Kolonizatorzy + Zadania
    path("kolonizatorzy_zadania", views.peopleTasks, name="people_tasks"),
    path("kolonizatorzy_zadania/new", views.peopleTasksNew, name="people_tasks_new"),
    path(
        "kolonizatorzy_zadania/edit/<id>",
        views.peopleTasksEdit,
        name="people_tasks_edit",
    ),
    # Specjalizacje
    path("specjalizacje", views.specs, name="specs"),
    path("specjalizacje/new", views.specsNew, name="specs_new"),
    path("specjalizacje/edit/<id>", views.specsEdit, name="specs_edit"),
    # Doświadczenia Kolonizatorów
    path("staż", views.exp, name="exp"),
    path("staż/new", views.expNew, name="exp_new"),
    path("staż/edit/<id>", views.expEdit, name="exp_edit"),
]
