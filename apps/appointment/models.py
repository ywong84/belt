from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re
emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')


class UserManager(models.Manager):
    def registration(self, request):
        error = False
        if request.POST["name"] == "":
            messages.warning(request, "Name is Required!")
            error = True

        elif len(request.POST["name"]) < 2:
            messages.warning(request, "Name must be greater than 2 characters")
            error = True
        elif any(char.isdigit() for char in request.POST["name"]) == True:
            messages.warning(request, "Name must be letters!")
            error = True

        if not emailRegex.match(request.POST["email"]):
            messages.warning(request, "Email is not valid!")
            error = True
        elif request.POST["email"] == "":
            messages.warning(request, "Email is required!")
            error = True
        elif User.userManager.filter(email=request.POST['email']):
            messages.warning(request, "This email already exists in our database.")
            error = True

        if request.POST["password"]== "":
            messages.warning(request, "Password is Required!")
            error = True
        elif len(request.POST["password"]) < 8:
            messages.warning(request, "Password must be greater than 8 characters long")
            error = True
        elif not passwordRegex.match(request.POST["password"]):
            messages.warning(request, "Password must must contain at least one lowercase letter, one uppercase letter, and one digit!")
            error = True

        if request.POST["confirmPassword"] == "":
            messages.warning(request, "Please confirm password!")
            error = True
        elif not request.POST['password'] == request.POST['confirmPassword']:
            messages.warning(request, "Password do not match, try again!")
            error = True
        if request.POST["birthday"] == "":
            messages.warning(request, "Birthday is Required!")
            error = True

        if error == False:
            request.session["email"] = request.POST["email"]
            hashed = bcrypt.hashpw(request.POST["password"].encode('utf-8'), bcrypt.gensalt())
            result = self.create(name=request.POST["name"], email=request.POST["email"], password=hashed, birthday=request.POST["birthday"])
            request.session['id'] = result.id
            return error


    def login(self, request):
        error = False
        if request.POST["email"] == "":
            messages.warning(request, "Email is required!")
            error = True
        elif not emailRegex.match(request.POST["email"]):
            messages.warning(request, "Email is not valid!")
            error = True

        if request.POST["password"]== "":
            messages.warning(request, "Password is Required!")
            error = True
        elif len(request.POST["password"]) < 8:
            messages.warning(request, "Password must be greater than 8 characters long")
            error = True
        if self.filter(email=request.POST['email']):
            hashed = self.get(email = request.POST['email']).password.encode('utf-8')
            if  bcrypt.hashpw(request.POST["password"].encode('utf-8'), hashed) == hashed:
                error = False
                request.session['id'] = result[0].id

        else:
            messages.warning(request, "Unsuccessful Login, Try Again!!!")
            error = True
            return error

class AppointmentsManager(models.Manager):
    def create_appointment(self, request):
        error = False
        if request.POST["dates"] == "":
            messages.warning(request, "Date is required!")
            error = True
        if request.POST["time"] == "":
            messages.warning(request, "Date is required!")
            error = True
        if request.POST["task"] == "":
            messages.warning(request, "Task is required!")
            error = True
        else:
            user = User.userManager.get(id=request.session['id'])
            my_appointments = Appointments.appointmentsManager.create(date=str(request.POST['dates']), task=str(request.POST['task']),time=str(request.POST['time']), add_user=user)
            error = False
        return error

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()

class Appointments(models.Model):
    date = models.DateField(null=True)
    task = models.CharField(max_length=100)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    Status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    add_user = models.ForeignKey('User', related_name='schedule')
    appointmentsManager = AppointmentsManager()
