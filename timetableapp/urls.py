from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("generate/", views.generate_timetable_view, name="generate_timetable"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
]