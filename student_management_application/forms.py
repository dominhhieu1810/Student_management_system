from django import forms
from django.forms import DateInput

from student_management_application.models import Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    username = forms.CharField(label="Tên tài khoản", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Mật khẩu", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    firstName = forms.CharField(label="Họ", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    lastName = forms.CharField(label="Tên", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Địa chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    courseList = []
    try:
        courses = Courses.objects.all()

        for course in courses:
            smallCourse = (course.id, course.courseName)
            courseList.append(smallCourse)

    except:
        courseList = []

    sessionList = []
    try:
        sessions = SessionYearModel.objects.all()

        for ses in sessions:
            smallSes = (ses.id, str(ses.session_start_year) + "-->" + str(ses.session_end_year))
            sessionList.append(smallSes)
    except:
        sessionList = []

    gender_choice = (
        ("Nam", "Nam"),
        ("Nu", "Nu")
    )

    course = forms.ChoiceField(label="Chứng chỉ", choices=courseList,
                               widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Giới tính", choices=gender_choice,
                               widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Năm học", choices=sessionList,
                                        widget=forms.Select(attrs={"class": "form-control"}))

    profilePicture = forms.FileField(label="Ảnh đại diện", max_length=50,
                                     widget=forms.FileInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    username = forms.CharField(label="Tên tài khoản", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    firstName = forms.CharField(label="Họ", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    lastName = forms.CharField(label="Tên", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Địa chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    courseList = []
    try:
        courses = Courses.objects.all()

        for course in courses:
            smallCourse = (course.id, course.courseName)
            courseList.append(smallCourse)
    except:
        courseList = []

    sessionList = []
    try:
        sessions = SessionYearModel.objects.all()

        for ses in sessions:
            smallSes = (ses.id, str(ses.session_start_year) + "-->" + str(ses.session_end_year))
            sessionList.append(smallSes)
    except:
        sessionList = []

    gender_choice = (
        ("Nam", "Nam"),
        ("Nu", "Nu")
    )

    course = forms.ChoiceField(label="Chứng chỉ", choices=courseList,
                               widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Giới tính", choices=gender_choice,
                               widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Năm học", choices=sessionList,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    profilePicture = forms.FileField(label="Ảnh đại diện", max_length=50,
                                     widget=forms.FileInput(attrs={"class": "form-control"}), required=False)


class AddTeacherForm(forms.Form):
    username = forms.CharField(label="Tên tài khoản", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Mật khẩu", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    firstName = forms.CharField(label="Họ", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    lastName = forms.CharField(label="Tên", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Địa chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class EditTeacherForm(forms.Form):
    username = forms.CharField(label="Tên tài khoản", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    firstName = forms.CharField(label="Họ", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    lastName = forms.CharField(label="Tên", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Địa chỉ", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))


class AddCourseForm(forms.Form):
    courseName = forms.CharField(label="Tên chứng chỉ", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))


class EditCourseForm(forms.Form):
    courseName = forms.CharField(label="Tên chứng chỉ", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
