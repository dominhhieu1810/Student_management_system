from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheck(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        print(modulename)
        user = request.user
        if user.is_authenticated:
            if user.userType == "1":
                if modulename == "student_management_application.AdminView":
                    pass
                elif modulename == "student_management_application.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("adminHome"))
            elif user.userType == "2":
                if modulename == "student_management_application.TeacherView":
                    pass
                elif modulename == "student_management_application.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("teacherHome"))
            elif user.userType == "3":
                if modulename == "student_management_application.StudentView" or modulename == "django.views.static":
                    pass
                elif modulename == "student_management_application.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("studentHome"))
            else:
                return HttpResponseRedirect(reverse("showLoginPage"))

        else:
            if request.path == reverse("showLoginPage") or request.path == reverse("doLogin"):
                pass
            else:
                return HttpResponseRedirect(reverse("showLoginPage"))
