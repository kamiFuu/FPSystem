# ProjectManager/views.py
from django.shortcuts import render, get_object_or_404
from .models import Project
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the ProjectManager app!")

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'ProjectManager/project_list.html', {'projects': projects})

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'ProjectManager/project_detail.html', {'project': project})

# Định nghĩa thêm hàm create_project nếu cần
def create_project(request):
    return HttpResponse("Create a new project here")
