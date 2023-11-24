from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_win, name="appeals-form"),
    path("dashboard", views.dashboard, name="dashboard"),
]
