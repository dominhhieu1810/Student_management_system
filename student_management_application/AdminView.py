from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_application.forms import AddStudentForm, EditStudentForm, AddTeacherForm, EditTeacherForm, \
    AddCourseForm
from student_management_application.models import CustomUser, Courses, Subjects, Teachers, Students, SessionYearModel


def AdminHome(request):
    return render(request, "adminViewTemplate/contentHome.html")


def AddTeacher(request):
    form = AddTeacherForm()
    return render(request, "adminViewTemplate/addTeacher.html", {"form": form})


def saveTeacher(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ")
    else:
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name,
                                                      first_name=first_name, userType=2)
                user.teachers.address = address
                user.save()
                messages.success(request, "Thêm thành công")
                return HttpResponseRedirect(reverse("addTeacher"))
            except:
                messages.error(request, "Thêm thất bại, vui lòng thử lại")
                return HttpResponseRedirect(reverse("addTeacher"))
        else:
            form = AddTeacherForm(request.POST)
            return render(request, "adminViewTemplate/addTeacher.html", {"form": form})


def ManageTeacher(request):
    teachers = Teachers.objects.all()
    return render(request, 'adminViewTemplate/manageTeacher.html', {"teachers": teachers})


def EditTeacher(request, teacherID):
    request.session['teacherID'] = teacherID
    teacher = Teachers.objects.get(admin=teacherID)
    form = EditStudentForm()
    form.fields['email'].initial = teacher.admin.email
    form.fields['username'].initial = teacher.admin.username
    form.fields['firstName'].initial = teacher.admin.first_name
    form.fields['lastName'].initial = teacher.admin.last_name
    form.fields['address'].initial = teacher.address
    return render(request, 'adminViewTemplate/editStudent.html',
                  {"form": form, "id": teacherID, "last_name": teacher.admin.last_name})


def saveTeacherEdit(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ")
    else:
        teacherID = request.session.get("teacherID")
        if teacherID == None:
            return HttpResponseRedirect(reverse("manageTeacher"))
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            teacherID = form.cleaned_data['teacherID']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(id=teacherID)
                user.first_name = firstName
                user.last_name = lastName
                user.email = email
                user.save()

                teacher = Teachers.objects.get(admin=teacherID)
                teacher.address = address
                teacher.save()
                del request.session['teacherID']
                messages.success(request, "Sửa thành công")
                return HttpResponseRedirect(reverse("addTeacher", kwargs={"teacherID": teacherID}))
            except:
                messages.error(request, "Sửa thất bại, vui lòng thử lại")
                return HttpResponseRedirect(reverse("addTeacher", kwargs={"teacherID": teacherID}))
        else:
            form = EditTeacherForm(request.POST)
            teacher = Students.objects.get(admin=teacherID)
            return render(request, "adminViewTemplate/editStudent.html",
                          {"form": form, "id": teacherID, "last_name": teacher.admin.last_name})


def AddCourse(request):
    form = AddCourseForm()
    return render(request, "adminViewTemplate/addCourse.html", {"form": form})


def saveCourse(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ")
    else:
        form = AddCourseForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['courseName']
            try:
                courseModel = Courses(courseName=course)
                courseModel.save()
                messages.success(request, "Thêm thành công")
                return HttpResponseRedirect(reverse("addCourse"))
            except:
                messages.error(request, "Thêm thất bại, vui lòng thử lại")
                return HttpResponseRedirect(reverse("addCourse"))
        else:
            form = AddCourseForm(request.POST)
            return render(request, "adminViewTemplate/addCourse.html", {"form": form})


def ManageCourse(request):
    courses = Courses.objects.all()
    return render(request, 'adminViewTemplate/manageCourse.html', {"courses": courses})


def EditCourse(request, courseID):
    request.session['courseID'] = courseID
    course = Courses.objects.get(id=courseID)
    form = AddCourseForm()
    form.fields['courseName'].initial = course.courseName
    return render(request, 'adminViewTemplate/editCourse.html', {"form": form, "id": courseID})


def saveCourseEdit(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ")
    else:
        courseID = request.session.get("courseID")
        form = AddCourseForm(request.POST)
        if form.is_valid():
            courseName = form.cleaned_data['courseName']
            try:
                course = Courses.objects.get(id=courseID)
                course.courseName = courseName
                course.save()
                del request.session['courseID']
                messages.success(request, "Thêm thành công")
                return HttpResponseRedirect(reverse("editCourse", kwargs={"courseID": courseID}))
            except:
                messages.error(request, "Thêm thất bại, vui lòng thử lại")
                return HttpResponseRedirect(reverse("editCourse", kwargs={"courseID": courseID}))
        else:
            form = EditStudentForm(request.POST)
            course = Courses.objects.get(id=courseID)
            return render(request, "adminViewTemplate/editCourse.html",
                          {"form": form, "id": courseID})


def AddStudent(request):
    courses = Courses.objects.all()
    form = AddStudentForm()
    return render(request, "adminViewTemplate/addStudent.html", {"courses": courses, "form": form})


def saveStudent(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            course_id = form.cleaned_data['course']
            session_year_id = form.cleaned_data['session_year_id']
            profile_picture = request.FILES['profilePicture']
            filestorage = FileSystemStorage()
            filename = filestorage.save(profile_picture.name, profile_picture)
            profile_picture_url = filestorage.url(filename)
            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name,
                                                      first_name=first_name, userType=3)
                user.students.address = address
                user.students.gender = gender
                session_year = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.courseID = Courses.objects.get(id=course_id)

                user.students.profilePicture = profile_picture_url
                user.save()
                messages.success(request, "Thêm thành công")
                return HttpResponseRedirect(reverse("addStudent"))
            except:
                messages.error(request, "Thêm thất bại, vui lòng thử lại")
                return HttpResponseRedirect(reverse("addStudent"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, "adminViewTemplate/addStudent.html", {"form": form})


def ManageStudent(request):
    students = Students.objects.all()
    return render(request, "adminViewTemplate/manageStudent.html", {"students": students})


def EditStudent(request, studentID):
    request.session['studentID'] = studentID
    student = Students.objects.get(admin=studentID)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['firstName'].initial = student.admin.first_name
    form.fields['lastName'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.courseID.id
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id
    #form.fields['sessionEndYear'].initial = student.sessionEndYear
    return render(request, 'adminViewTemplate/editStudent.html',
                  {"form": form, "id": studentID, "last_name": student.admin.last_name})


def saveStudentEdit(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ")
    else:
        studentID = request.session.get("studentID")
        if studentID == None:
            return HttpResponseRedirect(reverse("manageStudent"))
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            courseID = form.cleaned_data['course']
            session_year_id = form.cleaned_data['session_year_id']
            if request.FILES.get('profilePicture', False):
                profile_picture = request.FILES['profilePicture']
                filestorage = FileSystemStorage()
                filename = filestorage.save(profile_picture.name, profile_picture)
                profile_picture_url = filestorage.url(filename)
            else:
                profile_picture_url = None
            try:
                user = CustomUser.objects.get(id=studentID)
                user.first_name = firstName
                user.last_name = lastName
                user.email = email
                user.save()

                student = Students.objects.get(admin=studentID)
                student.gender = gender
                student.address = address
                session_year = SessionYearModel.objects.get(id=session_year_id)
                student.session_year_id = session_year
                course = Courses.objects.get(id=courseID)
                student.courseID = course
                if profile_picture_url != None:
                    student.profilePicture = profile_picture_url
                student.save()
                del request.session['studentID']
                messages.success(request, "Sửa thành công")
                return HttpResponseRedirect(reverse("editStudent", kwargs={"studentID": studentID}))
            except:
                messages.error(request, "Sửa thất bại, vui lòng thử lại")
                return HttpResponseRedirect(reverse("editStudent", kwargs={"studentID": studentID}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=studentID)
            return render(request, "adminViewTemplate/editStudent.html",
                          {"form": form, "id": studentID, "last_name": student.admin.last_name})


def AddSubject(request):
    courses = Courses.objects.all()
    teachers = CustomUser.objects.filter(userType=2)
    return render(request, "adminViewTemplate/addSubject.html", {"courses": courses, "teachers": teachers})


def saveSubject(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ")
    else:
        subjectName = request.POST.get("subjectName")
        courseID = request.POST.get("course")
        course = Courses.objects.get(id=courseID)
        teacherID = request.POST.get("teacher")
        teacher = CustomUser.objects.get(id=teacherID)
        try:
            subject = Subjects(subjectName=subjectName, courseID=course, teacherID=teacher)
            subject.save()
            messages.success(request, "Thêm thành công")
            return HttpResponseRedirect("/addSubject")
        except:
            messages.error(request, "Thêm thất bại, vui lòng thử lại")
            return HttpResponseRedirect(reverse("addSubject"))


def ManageSubject(request):
    subjects = Subjects.objects.all()
    return render(request, "adminViewTemplate/manageSubject.html", {"subjects": subjects})


def EditSubject(request, subjectID):
    subject = Subjects.objects.get(id=subjectID)
    courses = Courses.objects.all()
    teachers = CustomUser.objects.filter(userType=2)
    return render(request, 'adminViewTemplate/editSubject.html',
                  {"subject": subject, "teachers": teachers, "courses": courses, "id": subjectID})


def saveSubjectEdit(request):
    if request.method != "POST":
        return HttpResponse("Phương thức không hợp lệ")
    else:
        subjectID = request.POST.get("subjectID")
        subjectName = request.POST.get("subjectName")
        teacherID = request.POST.get("teacher")
        courseID = request.POST.get("course")
        try:
            subject = Subjects.objects.get(id=subjectID)
            subject.subjectName = subjectName
            teacher = CustomUser.objects.get(id=teacherID)
            subject.teacherID = teacher
            course = Courses.objects.get(id=courseID)
            subject.courseID = course
            subject.save()
            messages.success(request, "Thêm thành công")
            return HttpResponseRedirect(reverse("editSubject", kwargs={"subjectID": subjectID}))
        except:
            messages.error(request, "Thêm thất bại, vui lòng thử lại")
            return HttpResponseRedirect(reverse("editSubject", kwargs={"subjectID": subjectID}))


def manageSession(request):
    return render(request, "adminViewTemplate/manageSession.html")


def addSessionSave(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manageSession"))
    else:
        session_start_year = request.POST.get("sessionStart")
        session_end_year = request.POST.get("sessionEnd")

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Thêm thành công")
            return HttpResponseRedirect(reverse("manageSession"))
        except:
            messages.success(request, "Thêm thất bại, vui lòng thử lại")
            return HttpResponseRedirect(reverse("manageSession"))
