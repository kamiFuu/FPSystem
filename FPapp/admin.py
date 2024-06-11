from django.contrib import admin
from .models import Course, Teacher, Researcher, Student, Enrollment, Lecture, Grade, Clicker, Observation, Interview, LectureStructure
import pytz

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass

@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Lecture)  # Thay đổi từ Lesson
class LectureAdmin(admin.ModelAdmin):  # Thay đổi từ LessonAdmin
    pass

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass

@admin.register(Clicker)
class ClickerAdmin(admin.ModelAdmin):
    list_display = ('student', 'lecture', 'click_count', 'timestamp', 'activity')  # Thay đổi từ lesson
    list_filter = ('lecture',)
    search_fields = ('student__name', 'lecture__lecture_name', 'activity')
    ordering = ('lecture',)
    list_per_page = 50  # Số mục trên mỗi trang

    list_editable = ('click_count', 'activity')
    list_display_links = ('student', 'lecture', 'timestamp')
    fields = ('student', 'lecture', 'click_count', 'timestamp', 'activity')  # Thay đổi từ lesson

    def save_model(self, request, obj, form, change):
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        if obj.timestamp:
            # Loại bỏ microsecond
            obj.timestamp = obj.timestamp.astimezone(tokyo_tz).replace(microsecond=0)
        super().save_model(request, obj, form, change)
@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    pass

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    pass

@admin.register(LectureStructure)
class LectureStructureAdmin(admin.ModelAdmin):
    pass
