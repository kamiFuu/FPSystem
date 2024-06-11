import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Đọc dữ liệu từ CSV
clickers_df = pd.read_csv('exports/clickers_data.csv')

# Chuyển đổi timestamp
clickers_df['timestamp'] = pd.to_datetime(clickers_df['timestamp'])
clickers_df['hour'] = clickers_df['timestamp'].dt.hour + clickers_df['timestamp'].dt.minute / 60.0

# Thêm jitter vào giờ để tránh trùng lặp điểm
clickers_df['hour'] = clickers_df['hour'] + np.random.normal(0, 0.1, size=len(clickers_df))

# Tạo thư mục để lưu biểu đồ
import os
if not os.path.exists('static/lectures'):
    os.makedirs('static/lectures')

# Lặp qua từng buổi học và tạo biểu đồ
lectures = clickers_df['lecture__lecture_name'].unique()
for lecture in lectures:
    lecture_df = clickers_df[clickers_df['lecture__lecture_name'] == lecture]
    
    plt.figure(figsize=(10, 6))
    # Biểu đồ tán xạ với jitter
    sns.scatterplot(x=lecture_df['hour'], y=lecture_df['click_count'], label='Số lần mất tập trung', s=50, alpha=0.7)
    
    # Thêm đường hồi quy bậc hai
    sns.regplot(x=lecture_df['hour'], y=lecture_df['click_count'], scatter=False, label='Hồi quy bậc hai', order=2, color='red')
    
    # Thêm đường trung bình di động
    lecture_df = lecture_df.sort_values(by='hour')
    lecture_df['rolling_mean'] = lecture_df['click_count'].rolling(window=5).mean()
    plt.plot(lecture_df['hour'], lecture_df['rolling_mean'], label='Trung bình di động', color='green')
    
    # Đặt tiêu đề và nhãn
    plt.axvline(x=8, color='red', linestyle='-', label='Quá khứ/Tương lai')
    plt.title(f'Biểu đồ phân tích sự tập trung của sinh viên - {lecture}')
    plt.xlabel('Thời gian')
    plt.ylabel('Số lần mất tập trung')
    plt.legend()
    plt.savefig(f'static/lectures/{lecture}_focus_plot.png')
    plt.close()
