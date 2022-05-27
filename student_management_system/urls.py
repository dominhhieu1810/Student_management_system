"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from student_management_application import views, AdminView, TeacherView, StudentView
from student_management_system import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.ShowLoginPage, name='showLoginPage'),
    path('doLogin', views.DoLogin, name="doLogin"),
    path('getUserDetails', views.GetUserDetails),
    path('logout', views.DoLogOut, name="logout"),
    # admin
    path('adminHome', AdminView.AdminHome, name="adminHome"),
    path('addTeacher', AdminView.AddTeacher, name="addTeacher"),
    path('saveTeacher', AdminView.saveTeacher, name="saveTeacher"),
    path('manageTeacher', AdminView.ManageTeacher, name="manageTeacher"),
    path('editTeacher/<str:teacherID>', AdminView.EditTeacher, name="editTeacher"),
    path('saveTeacherEdit', AdminView.saveTeacherEdit, name="saveTeacherEdit"),
    path('addCourse', AdminView.AddCourse, name="addCourse"),
    path('saveCourse', AdminView.saveCourse, name="saveCourse"),
    path('manageCourse', AdminView.ManageCourse, name="manageCourse"),
    path('editCourse/<str:courseID>', AdminView.EditCourse, name="editCourse"),
    path('saveCourseEdit', AdminView.saveCourseEdit, name="saveCourseEdit"),
    path('saveSubjectEdit', AdminView.saveSubjectEdit, name="saveSubjectEdit"),
    path('addStudent', AdminView.AddStudent, name="addStudent"),
    path('saveStudent', AdminView.saveStudent, name="saveStudent"),
    path('manageStudent', AdminView.ManageStudent, name="manageStudent"),
    path('editStudent/<str:studentID>', AdminView.EditStudent, name="editStudent"),
    path('saveStudentEdit', AdminView.saveStudentEdit, name="saveStudentEdit"),
    path('addSubject', AdminView.AddSubject, name="addSubject"),
    path('saveSubject', AdminView.saveSubject, name="saveSubject"),
    path('manageSubject', AdminView.ManageSubject, name="manageSubject"),
    path('editSubject/<str:subjectID>', AdminView.EditSubject, name="editSubject"),
    path('saveSubjectEdit', AdminView.saveSubjectEdit, name="saveSubjectEdit"),
    path('manageSession', AdminView.manageSession, name="manageSession"),
    path('addSessionSave', AdminView.addSessionSave, name="addSessionSave"),

    # teacher
    path('teacherHome', TeacherView.TeacherHome, name="teacherHome"),
    path('teacherTakeAttendance', TeacherView.teacherTakeAttendance, name="teacherTakeAttendance"),
    path('getStudents', TeacherView.getStudents, name="getStudents"),
    path('saveAttendanceData', TeacherView.saveAttendanceData, name="saveAttendanceData"),
    path('updateAttendance', TeacherView.updateAttendance, name="updateAttendance"),
    path('getAttendanceDate', TeacherView.getAttendanceDate, name="getAttendanceDate"),
    path('getAttendanceStudent', TeacherView.getAttendanceStudent, name="getAttendanceStudent"),
    path('saveUpdateAttendance', TeacherView.saveUpdateAttendance, name="saveUpdateAttendance"),
    path('addResult', TeacherView.addResult, name="addResult"),
    path('saveStudentResult', TeacherView.saveStudentResult, name="saveStudentResult"),



    # student
    path('studentHome', StudentView.StudentHome, name="studentHome"),
    path('viewAttendance', StudentView.viewAttendance, name="viewAttendance"),
    path('viewAttendancePost', StudentView.viewAttendancePost, name="viewAttendancePost"),
    path('viewMark', StudentView.viewMark, name="viewMark"),




    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
