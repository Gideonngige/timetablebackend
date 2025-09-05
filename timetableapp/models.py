from django.db import models

# Create your models here.
class ClassRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Student(models.Model):
    full_name = models.CharField(max_length=150)
    admission_no = models.CharField(max_length=50, unique=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='students')
    email = models.CharField(max_length=200, default="johndoe@example.com")
    password = models.CharField(max_length=255)
    profile_image = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.admission_no}) ({self.classroom})"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    audience_class = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='announcements', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.audience_class.name}"

class Grade(models.Model):
    TERM_CHOICES = [
        ("Term 1","Term 1"),
        ("Term 2","Term 2"),
        ("Term 3","Term 3"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name} - {self.term}: {self.score} ({self.grade})"