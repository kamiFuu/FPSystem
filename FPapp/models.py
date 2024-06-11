from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    course_description = models.CharField(max_length=500, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name

class Teacher(models.Model):
    name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Researcher(models.Model):
    account = models.CharField(max_length=255, unique=True)
    login = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.account

class Student(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    courses = models.ManyToManyField('Course', through='Enrollment')

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.course_name}"

class Lecture(models.Model):  # Thay đổi tên thành Lecture
    lecture_name = models.CharField(max_length=255)  # Thay đổi từ lesson_name
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)  # Thêm trường start_time
    end_time = models.DateTimeField(null=True, blank=True)    # Thêm trường end_time
    #activities = models.TextField()

    def __str__(self):
        return self.lecture_name  # Thay đổi từ lesson_name

class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}: {self.score} ({self.grade})"

class Clicker(models.Model):
    click_count = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)  # Thay đổi từ lesson
    timestamp = models.DateTimeField()
    activity = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.student.name} - {self.lecture.lecture_name}: {self.click_count} clicks"  # Thay đổi từ lesson

class Observation(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    observation_text = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.lecture.lecture_name} - {self.observation_text}"
    
class Interview(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE)  # Thay đổi từ lesson
    focus_loss_time = models.DateTimeField()
    factors = models.TextField()
    researcher = models.ForeignKey('Researcher', on_delete=models.CASCADE)

    def __str__(self):
        return f"Interview with {self.student.name} by {self.researcher.account}"

class LectureStructure(models.Model):
    lecture = models.ForeignKey('Lecture', on_delete=models.CASCADE)  # Thay đổi từ lesson
    activity = models.CharField(max_length=500, blank=True, null=True)
    material = models.CharField(max_length=500, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.lecture.lecture_name} - {self.activity}"  # Thay đổi từ lesson
