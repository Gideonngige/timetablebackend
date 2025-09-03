from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .utils import generate_timetable
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the timetable index.")

def generate_timetable_view(request):
    classes = [f"Class {i}" for i in range(1, 9)]  # Class 1 to 8
    timetable = generate_timetable(classes)
    return JsonResponse(timetable, safe=False)
