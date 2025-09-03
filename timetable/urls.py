
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('timetableapp.urls')),
    path('admin/', admin.site.urls),
]
