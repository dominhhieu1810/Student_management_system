from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()


class CustomUser(AbstractUser):
    userTypeData = ((1, "Admin"), (2, "Teacher"), (3, "Student"))
    userType = models.CharField(default=1, choices=userTypeData, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    objects = models.Manager()


class Teachers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    objects = models.Manager()


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    courseName = models.CharField(max_length=255)
    objects = models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subjectName = models.CharField(max_length=255)
    courseID = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    teacherID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=255)
    profilePicture = models.FileField()
    address = models.TextField()
    courseID = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    objects = models.Manager()


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subjectID = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendanceDate = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    objects = models.Manager()


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendanceID = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    studentId = models.ForeignKey(Students, on_delete=models.CASCADE, null=True)
    leaveDate = models.CharField(max_length=255)
    leaveMessage = models.TextField()
    leaveStatus = models.BooleanField(default=False)
    objects = models.Manager()


class LeaveReportTeacher(models.Model):
    id = models.AutoField(primary_key=True)
    teacherID = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    leaveDate = models.CharField(max_length=255)
    leaveMessage = models.TextField()
    leaveStatus = models.BooleanField(default=False)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedbackReply = models.TextField()
    objects = models.Manager()


class FeedBackTeachers(models.Model):
    id = models.AutoField(primary_key=True)
    teacherID = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedbackReply = models.TextField()
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    objects = models.Manager()


class NotificationTeachers(models.Model):
    id = models.AutoField(primary_key=True)
    teacherID = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    message = models.TextField()
    objects = models.Manager()

class StudentMarks(models.Model):
    id = models.AutoField(primary_key=True)
    studentID = models.ForeignKey(Students, on_delete=models.CASCADE)
    subjectID = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    subjectExamMarks=models.FloatField(default=0)
    subjectMidtermMarks=models.FloatField(default=0)
    objects = models.Manager()



@receiver(post_save, sender=CustomUser)
def CreateUserProfile(sender, instance, created, **kwargs):
    if created:
        if instance.userType == 1:
            Admin.objects.create(admin=instance)
        if instance.userType == 2:
            Teachers.objects.create(admin=instance, address="")
        if instance.userType == 3:
            Students.objects.create(admin=instance, address="", gender="",
                                    session_year_id=SessionYearModel.objects.get(id=1),
                                    courseID=Courses.objects.get(id=1),
                                    profilePicture="")


@receiver(post_save, sender=CustomUser)
def SaveUserProfile(sender, instance, **kwargs):
    if instance.userType == 1:
        instance.admin.save()
    if instance.userType == 2:
        instance.teachers.save()
    if instance.userType == 3:
        instance.students.save()
