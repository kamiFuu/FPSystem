import pandas as pd

# Đọc dữ liệu từ file CSV
clickers_df = pd.read_csv('exports/clickers_data.csv')

# Chuyển đổi cột timestamp sang định dạng datetime
clickers_df['timestamp'] = pd.to_datetime(clickers_df['timestamp'])

# Chuyển đổi múi giờ cho lecture_start_time và lecture_end_time
lecture_start_time = pd.to_datetime('2024-06-04 13:40').tz_localize('Asia/Tokyo')
lecture_end_time = pd.to_datetime('2024-06-04 15:20').tz_localize('Asia/Tokyo')

# Lọc dữ liệu trong khoảng thời gian của buổi học
filtered_df = clickers_df[(clickers_df['timestamp'] >= lecture_start_time) & (clickers_df['timestamp'] <= lecture_end_time)]

# Kiểm tra dữ liệu đã lọc
print(filtered_df)

