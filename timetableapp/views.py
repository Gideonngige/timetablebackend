from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from .utils import generate_timetable
from .models import Student, ClassRoom
import pyrebase
import cloudinary.uploader
import json
# Create your views here.

config = {
    "apiKey": "AIzaSyCvXvn5T3gvhw4b0DHgowI5KHGgbmkvh1M",
    "authDomain": "g-tech-6fc99.firebaseapp.com",
    "databaseURL": "https://g-tech-6fc99-default-rtdb.firebaseio.com",
    "projectId": "g-tech-6fc99",
    "storageBucket": "g-tech-6fc99.firebasestorage.app",
    "messagingSenderId": "522681202970",
   " appId": "1:522681202970:web:739853a260bc26e85f54a3",
   " measurementId": "G-RE0JC4BJ93"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth() 
database = firebase.database()

def index(request):
    return HttpResponse("Hello, world. You're at the timetable index.")


#start of signin api
@csrf_exempt
@api_view(['POST'])
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"message": "Email and password are required"}, status=400)

            student = authe.sign_in_with_email_and_password(email, password)
            
            if Student.objects.filter(email=email).exists():
                session_id = student['idToken']
                request.session['uid'] = str(session_id)
                get_student = Student.objects.filter(email=email).first()
                student_id = get_student.id
                return JsonResponse({"message": "Successfully logged in", "token":session_id, "student_id":student_id}, status=200)
            else:
                return JsonResponse({"message": "No user found with this email, please register"}, status=404)

        except Exception as e:
            print("Error:", str(e))  # Optional logging
            return JsonResponse({"message": "Invalid credentials. Please check your email and password."}, status=401)

    return JsonResponse({"message": "Invalid request method"}, status=405)
#end of signin api


#start of register api
@csrf_exempt
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            full_name = data.get("full_name")
            admission_no = data.get("admission_no")
            classroom = data.get("classroom")
            email = data.get("email")
            password = data.get("password")
            profile_image = data.get("profile_image")  # this is a URL

            # Check for missing fields
            if not all([full_name, admission_no, classroom, email, password, profile_image]):
                return JsonResponse({"message": "Missing required fields"}, status=400)

            # Check if email already exists
            if Student.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email already exists"}, status=400)

            # Create user in Firebase
            user = authe.create_user_with_email_and_password(email, password)
            uid = user['localId']

            # Find classroom
            classroom_obj = ClassRoom.objects.filter(name=classroom).first()

            # Save user in your database
            student = Student(
                full_name=full_name,
                admission_no=admission_no,
                classroom=classroom_obj,
                email=email,
                profile_image=profile_image,  # already a Cloudinary URL
                password=uid
            )
            student.save()

            return JsonResponse({"message": "Successfully signed up"}, status=201)

        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({"message": "Signup failed", "error": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method"}, status=405)

#end of register api


def generate_timetable_view(request):
    classes = [f"Class {i}" for i in range(1, 9)]  # Class 1 to 8
    timetable = generate_timetable(classes)
    return JsonResponse(timetable, safe=False)
