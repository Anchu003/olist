import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

X_PARSE_APPLICATION_ID = os.getenv("X_PARSE_APPLICATION_ID")
X_PARSE_REST_API_KEY = os.getenv("X_PARSE_REST_API_KEY")

# Kiểm tra key có tồn tại không
if not X_PARSE_APPLICATION_ID or not X_PARSE_REST_API_KEY:
    raise ValueError("Thiếu X_PARSE_APPLICATION_ID hoặc X_PARSE_REST_API_KEY trong .env")

# Tham số API
LIMIT = 100
skip = 0

# Danh sách lưu dữ liệu
latitude = []
longitude = []
zip_code = []
city_name = []

while True:
    url = f"https://parseapi.back4app.com/classes/Worldzipcode_BR?skip={skip}&limit={LIMIT}&keys=geoPosition,placeName,postalCode"
    headers = {
        "X-Parse-Application-Id": X_PARSE_APPLICATION_ID,
        "X-Parse-REST-API-Key": X_PARSE_REST_API_KEY,
    }
    response = requests.get(url, headers=headers)

    # Kiểm tra response
    if response.status_code != 200:
        print(f"Lỗi API: {response.status_code}")
        break

    data = response.json()
    results = data.get("results", [])

    if not results:  # Nếu không còn dữ liệu, dừng loop
        break

    # Lưu dữ liệu
    for result in results:
        geo = result.get("geoPosition")
        latitude.append(geo.get("latitude") if geo else None)
        longitude.append(geo.get("longitude") if geo else None)
        zip_code.append(result.get("postalCode"))
        city_name.append(result.get("placeName"))

    skip += LIMIT

# Tạo dataframe
df = pd.DataFrame({
    "city_name": city_name,
    "latitude": latitude,
    "longitude": longitude,
    "zip_code": zip_code,
})

# Lưu ra CSV
df.to_csv("datasets/br_zip_code.csv", index=False)
print("Hoàn tất, dữ liệu đã lưu vào datasets/br_zip_code.csv")
