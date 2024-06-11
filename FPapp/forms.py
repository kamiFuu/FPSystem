from django import forms
from .models import Course, Lecture

class TimeIntervalForm(forms.Form):
    statistics_type = forms.ChoiceField(choices=[
        ('course', 'Course'),
        ('lecture', 'Lecture')
    ])
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    lecture = forms.ModelChoiceField(queryset=Lecture.objects.all(), required=False)
