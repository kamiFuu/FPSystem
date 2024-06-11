import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _ #cho translate
from django.utils import timezone
import os
import pytz

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from .models import Course, Lecture, Student, Clicker, LectureStructure, Observation
from .forms import TimeIntervalForm

def focus_distribution_view(request):
    form = TimeIntervalForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # Đặt cố định khoảng thời gian là 5 phút
        time_interval = '5min'
        statistics_type = form.cleaned_data['statistics_type']
        course = form.cleaned_data['course']
        lecture = form.cleaned_data['lecture']

        # Đọc dữ liệu từ CSV
        clickers_df = pd.read_csv('exports/clickers_data.csv')
        clickers_df['timestamp'] = pd.to_datetime(clickers_df['timestamp']).dt.tz_convert('Asia/Tokyo')

        if statistics_type == 'lecture' and lecture:
            clickers_df = clickers_df[clickers_df['lecture__lecture_name'] == lecture.lecture_name]

        # Chuyển timestamp về index và nhóm theo khoảng thời gian đã chọn
        clickers_df = clickers_df.set_index('timestamp').resample(time_interval).sum().reset_index()

        # Sử dụng thời gian bắt đầu và kết thúc của lecture từ database
        lecture_start_time = lecture.start_time
        lecture_end_time = lecture.end_time

        # Lọc dữ liệu trong khoảng thời gian của buổi học
        filtered_df = clickers_df[(clickers_df['timestamp'] >= lecture_start_time) & (clickers_df['timestamp'] <= lecture_end_time)]

        if not filtered_df.empty:
            # Tạo thư mục để lưu biểu đồ
            if not os.path.exists('static/lectures'):
                os.makedirs('static/lectures')

            # Tạo biểu đồ
            plt.figure(figsize=(12, 8))
            sns.lineplot(x='timestamp', y='click_count', data=filtered_df, marker='o', label='Actual')

            # Dữ liệu cho mô hình
            X = np.array(range(len(filtered_df))).reshape(-1, 1)
            y = filtered_df['click_count'].values

            # Polynomial Regression (bậc 2)
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            poly_model = LinearRegression()
            poly_model.fit(X_poly, y)
            y_poly_pred = poly_model.predict(X_poly)
            sns.lineplot(x=filtered_df['timestamp'], y=y_poly_pred, color='red', label='Polynomial Regression (Degree 2)')

            # Random Forest
            rf_model = RandomForestRegressor(n_estimators=100)
            rf_model.fit(X, y)
            y_rf_pred = rf_model.predict(X)
            sns.lineplot(x=filtered_df['timestamp'], y=y_rf_pred, color='green', label='Random Forest')

            # Gradient Boosting
            gb_model = GradientBoostingRegressor(n_estimators=100)
            gb_model.fit(X, y)
            y_gb_pred = gb_model.predict(X)
            sns.lineplot(x=filtered_df['timestamp'], y=y_gb_pred, color='blue', label='Gradient Boosting')

            # Đặt tiêu đề và nhãn
            plt.title(f'Biểu đồ phân tích sự tập trung của sinh viên - {lecture.lecture_name}')
            plt.xlabel('Thời gian')
            plt.ylabel('Số lần mất tập trung')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'static/lectures/{lecture.lecture_name}_focus_plot.png')
            plt.close()
        else:
            print("Không có dữ liệu trong khoảng thời gian này.")

    # Lấy danh sách các file hình ảnh trong thư mục static/lectures
    lecture_images = os.listdir('static/lectures')
    return render(request, 'focus_distribution.html', {'form': form, 'lecture_images': lecture_images})

def export_data(request):
    clickers = Clicker.objects.all().values('click_count', 'student__name', 'lecture__lecture_name', 'timestamp', 'activity')
    clickers_df = pd.DataFrame(clickers)
    clickers_df.to_csv('exports/clickers_data.csv', index=False)
    return HttpResponse("Data exported successfully!") 

def clicker_view(request):
    courses = Course.objects.all()
    students = Student.objects.all()

    context = {
        'courses': courses,
        'students': students,
    }
    return render(request, 'clicker.html', context)

def get_lectures(request, course_id):
    lectures = Lecture.objects.filter(course_id=course_id).values('id', 'lecture_name')
    return JsonResponse(list(lectures), safe=False)

def get_lecture_structures(request, lecture_id):
    lecture_structures = LectureStructure.objects.filter(lecture_id=lecture_id).values('id', 'activity', 'start_time', 'end_time')
    return JsonResponse(list(lecture_structures), safe=False)

def get_observations(request, lecture_id):
    observations = Observation.objects.filter(lecture_id=lecture_id).values('id', 'observation_text', 'start_time', 'end_time')
    return JsonResponse(list(observations), safe=False)

def record_click(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        lecture_id = request.POST.get('lecture_id')
        if student_id and lecture_id:
            student = get_object_or_404(Student, id=student_id)
            lecture = get_object_or_404(Lecture, id=lecture_id)
            tokyo_tz = pytz.timezone('Asia/Tokyo')
            current_time = timezone.now().astimezone(tokyo_tz).replace(microsecond=0)
            clicker = Clicker.objects.create(
                student=student,
                lecture=lecture,
                click_count=1,
                timestamp=current_time,
                activity='Observed'
            )
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})
def add_lecture_structure(request):
    if request.method == 'POST':
        lecture_id = request.POST.get('lecture_id')
        activity = request.POST.get('activity')
        material = request.POST.get('materials')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if lecture_id and activity and start_time and material and end_time:
            lecture = get_object_or_404(Lecture, id=lecture_id)
            LectureStructure.objects.create(
                lecture=lecture,
                activity=activity,
                material=material,
                start_time=start_time,
                end_time=end_time
            )
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})

def add_observation(request):
    if request.method == 'POST':
        lecture_id = request.POST.get('lecture_id')
        observation_text = request.POST.get('observation_text')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        lecture = get_object_or_404(Lecture, id=lecture_id)
        Observation.objects.create(
            lecture=lecture,
            observation_text=observation_text,
            start_time=start_time,
            end_time=end_time
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid data'})
