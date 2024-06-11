import django
import pytz
from django.utils import timezone
from FPapp.models import Clicker

# Định nghĩa múi giờ Tokyo
tokyo_tz = pytz.timezone('Asia/Tokyo')

# Lấy tất cả các bản ghi Clicker
clickers = Clicker.objects.all()

# Chuyển đổi thời gian cho từng bản ghi
for clicker in clickers:
    if clicker.timestamp:
        # Chuyển đổi múi giờ và loại bỏ microsecond
        clicker.timestamp = clicker.timestamp.astimezone(tokyo_tz).replace(microsecond=0)
        clicker.save()

print("Chuyển đổi múi giờ hoàn tất.")