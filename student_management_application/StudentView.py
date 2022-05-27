import datetime

from django.http import HttpResponse
from django.shortcuts import render

from student_management_application.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, \
    StudentMarks


def StudentHome(request):
    return render(request, 'studentViewTemplate/contentHome.html')


def viewAttendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.courseID
    subjects = Subjects.objects.filter(courseID=course)
    return render(request, 'studentViewTemplate/viewAttendance.html', {"subjects": subjects})


def viewAttendancePost(request):
    subjectID = request.POST.get("subject")
    startDate = request.POST.get("startDate")
    endDate = request.POST.get("endDate")

    startDataParse = datetime.datetime.strptime(startDate, "%Y-%m-%d").date()
    endDataParse = datetime.datetime.strptime(endDate, "%Y-%m-%d").date()
    subjectObj = Subjects.objects.get(id=subjectID)
    userObject = CustomUser.objects.get(id=request.user.id)
    stuObj = Students.objects.get(admin=userObject)
    attendance = Attendance.objects.filter(attendanceDate__range=(startDataParse, endDataParse), subjectID=subjectObj)
    attendanceReports = AttendanceReport.objects.filter(attendanceID__in=attendance, studentID=stuObj)

    return render(request, 'studentViewTemplate/attendanceData.html', {"attendanceReports": attendanceReports})

def viewMark(request):
    student=Students.objects.get(admin=request.user.id)
    studentMarks=StudentMarks.objects.filter(studentID=student.id)

    return render(request,'studentViewTemplate/studentMark.html',{"studentMarks":studentMarks})

