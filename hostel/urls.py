from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    #student
    path("students/", views.students, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/edit/<int:id>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:id>/", views.delete_student, name="delete_student"),
    #room
    path("rooms/", views.rooms, name="rooms"),
    path("rooms/add/", views.add_room, name="add_room"),
    path("rooms/edit/<int:id>/", views.edit_room, name="edit_room"),
    path("rooms/delete/<int:id>/", views.delete_room, name="delete_room"),
    #room allocation
    path("allocations/", views.allocations, name="allocations"),
    path("allocations/add/", views.add_allocation, name="add_allocation"),
    path("allocations/delete/<int:id>/", views.delete_allocation, name="delete_allocation"),
]