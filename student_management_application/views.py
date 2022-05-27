from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
from django.urls import reverse

from student_management_application.EmailLogin import EmailBackEnd


def ShowLoginPage(request):
    return render(request,"loginPage.html")


def DoLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.userType == "1":
                return HttpResponseRedirect(reverse("adminHome"))
            elif user.userType == "2":
                return HttpResponseRedirect(reverse("teacherHome"))
            else:
                return HttpResponseRedirect(reverse("studentHome"))
        else:
            messages.error(request, "Tài khoản/mật khẩu không chính xác")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user is not None:
        return HttpResponse("User: " + request.user.email + "User Type: " + request.user.userType)
    else:
        return HttpResponse("please log in first")

def DoLogOut(request):
    logout(request)
    return HttpResponseRedirect("/")