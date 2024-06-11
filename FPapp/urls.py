from django.urls import path
from . import views

urlpatterns = [
    path('export-data/', views.export_data, name='export_data'),
    path('focus-distribution/', views.focus_distribution_view, name='focus_distribution'),
    path('clicker/', views.clicker_view, name='clicker'),
    path('clicker/get_lectures/<int:course_id>/', views.get_lectures, name='get_lectures'),
    path('clicker/get_lecture_structures/<int:lecture_id>/', views.get_lecture_structures, name='get_lecture_structures'),
    path('clicker/get_observations/<int:lecture_id>/', views.get_observations, name='get_observations'),
    path('clicker/add_lecture_structure/', views.add_lecture_structure, name='add_lecture_structure'),
    path('clicker/add_observation/', views.add_observation, name='add_observation'),
    path('clicker/record_click/', views.record_click, name='record_click'),
]
