from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("generate/", views.generate_timetable_view, name="generate_timetable"),
]