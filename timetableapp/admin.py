from django.contrib import admin
from .models import ClassRoom, Subject, Student, Announcement, Grade

# Register your models here.
admin.site.register([ClassRoom, Subject, Student, Announcement, Grade])
