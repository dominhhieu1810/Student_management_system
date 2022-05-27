import json

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from student_management_application.models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, \
    StudentMarks


def TeacherHome(request):
    return render(request, 'teacherViewTemplate/contentHome.html')


def teacherTakeAttendance(request):
    subjects = Subjects.objects.filter(teacherID=request.user.id)
    sessionYears = SessionYearModel.objects.all()
    return render(request, "teacherViewTemplate/teacherTakeAttendance.html",
                  {"subjects": subjects, "sessionYears": sessionYears})


@csrf_exempt
def getStudents(request):
    subjectID = request.POST.get("subject")
    sessionYear = request.POST.get("sessionYear")

    subject = Subjects.objects.get(id=subjectID)
    sessionModel = SessionYearModel.objects.get(id=sessionYear)
    students = Students.objects.filter(courseID=subject.courseID, session_year_id=sessionModel)
    studentData = serializers.serialize("python", students)
    listData = []

    for student in students:
        smallData = {"id": student.admin.id, "name": student.admin.first_name + "" + student.admin.last_name}
        listData.append(smallData)
    return JsonResponse(json.dumps(listData), content_type="application/json", safe=False)
    # return HttpResponse(students)


@csrf_exempt
def saveAttendanceData(request):
    studentIDs = request.POST.get("studentIDs")
    subjectID = request.POST.get("subjectID")
    attendanceDate = request.POST.get("attendanceDate")
    session_year_id = request.POST.get("session_year_id")

    # print(studentIDs)
    subjectModel = Subjects.objects.get(id=subjectID)
    sessionModel = SessionYearModel.objects.get(id=session_year_id)
    jsonStudent = json.loads(studentIDs)
    # print(data[0]['id'])

    try:
        attendance = Attendance(subjectID=subjectModel, attendanceDate=attendanceDate, session_year_id=sessionModel)
        attendance.save()

        for stu in jsonStudent:
            student = Students.objects.get(admin=stu['id'])
            attendanceReport = AttendanceReport(studentID=student, attendanceID=attendance, status=stu['status'])
            attendanceReport.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Lỗi")


def updateAttendance(request):
    subjects = Subjects.objects.filter(teacherID=request.user.id)
    session_year_id = SessionYearModel.objects.all()
    return render(request, "teacherViewTemplate/updateAttendance.html",
                  {"subjects": subjects, "session_year_id": session_year_id})


@csrf_exempt
def getAttendanceDate(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subjectObj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subjectID=subjectObj, session_year_id=session_year_obj)
    attendanceObj = []
    for attendanceSingle in attendance:
        data = {"id": attendanceSingle.id, "attendanceDate": str(attendanceSingle.attendanceDate),
                "session_year_id": attendanceSingle.session_year_id.id}
        attendanceObj.append(data)

    return JsonResponse(json.dumps(attendanceObj), safe=False)

@csrf_exempt
def getAttendanceStudent(request):
    attendanceDate = request.POST.get("attendanceDate")

    attendance = Attendance.objects.get(id=attendanceDate)

    attendanceData = AttendanceReport.objects.filter(attendanceID=attendance)

    listData = []

    for student in attendanceData:
        smallData = {"id": student.studentID.admin.id,
                     "name": student.studentID.admin.first_name + "" + student.studentID.admin.last_name,
                     "status": student.status}
        listData.append(smallData)
    return JsonResponse(json.dumps(listData), content_type="application/json", safe=False)

@csrf_exempt
def saveUpdateAttendance(request):
    studentIDs = request.POST.get("studentIDs")

    attendanceDate = request.POST.get("attendanceDate")
    attendance=Attendance.objects.get(id=attendanceDate)
    jsonStudent = json.loads(studentIDs)

    try:

        for stu in jsonStudent:
            student = Students.objects.get(admin=stu['id'])
            attendanceReport = AttendanceReport.objects.get(studentID=student, attendanceID=attendance)
            attendanceReport.status=stu['status']
            attendanceReport.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Lỗi")

def addResult(request):
    subjects=Subjects.objects.filter(teacherID=request.user.id)
    sessionYears=SessionYearModel.objects.all()
    return render(request,"teacherViewTemplate/addResult.html",{"subjects":subjects,"sessionYears":sessionYears})

def saveStudentResult(request):
    if request.method != 'POST':
        return HttpResponseRedirect('addResult')
    studentAdminID=request.POST.get('studentList')
    midtermMarks=request.POST.get('midtermMarks')
    examMarks=request.POST.get('exemMarks')
    subjectID= request.POST.get('subject')

    studentObj= Students.objects.get(admin=studentAdminID)
    subjectObj= Subjects.objects.get(id=subjectID)

    try:
        checkExist = StudentMarks.objects.filter(subjectID=subjectObj, studentID=studentObj).exists()
        if checkExist :
            result = StudentMarks(studentID=studentObj, subjectID=subjectObj, subjectExamMarks=examMarks,
                          subjectMidtermMarks=midtermMarks)
            result.save()
            messages.success(request, "Thêm điểm thành công")
            return HttpResponseRedirect(reverse("addResult"))

        else:
            result=StudentMarks(studentID=studentObj,subjectID=subjectObj,subjectExamMarks=examMarks,subjectMidtermMarks=midtermMarks)
            result.save()
            messages.success(request, "Thêm điểm thành công")
            return HttpResponseRedirect(reverse("addResult"))
    except:
        messages.error(request, "Thêm thất bại")
        return HttpResponseRedirect(reverse("addResult"))


