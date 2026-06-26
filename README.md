# 🛒 Olist E-Commerce Data Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.2+-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.17-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.2-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-Object%20Storage-C72E49?style=for-the-badge&logo=minio&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Nền tảng phân tích dữ liệu end-to-end cho sàn thương mại điện tử Olist (Brazil)**  
*ETL Pipeline · Data Warehouse · Analytics Dashboard · Machine Learning*

</div>

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Tính năng](#-tính-năng)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt)
- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [Các dịch vụ](#-các-dịch-vụ)
- [Dashboard](#-dashboard)
- [Machine Learning](#-machine-learning)

---

## 🎯 Giới thiệu

Dự án này xây dựng một **nền tảng dữ liệu toàn diện** cho bộ dữ liệu thương mại điện tử [Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — một trong những marketplace lớn nhất Brazil. Hệ thống bao gồm toàn bộ vòng đời dữ liệu từ **ingest → transform → store → analyze → predict**.

### 🌟 Điểm nổi bật

- ✅ **ETL Pipeline tự động** với Apache Airflow (cả initial load và incremental load)
- ✅ **Data Warehouse** trên MySQL với schema star/snowflake
- ✅ **Data Lake** lưu trữ raw data trên MinIO (S3-compatible)
- ✅ **Analytics Dashboard** với Streamlit — KPIs, delivery metrics, marketing
- ✅ **Machine Learning** — Forecast doanh thu, gợi ý sản phẩm, dự đoán thời gian giao hàng
- ✅ **Containerized hoàn toàn** với Docker Compose — chạy 1 lệnh là xong

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                             │
│              Olist Brazilian E-Commerce Dataset                 │
│         (Orders, Customers, Products, Sellers, Reviews)         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAKE (MinIO)                           │
│                 Raw CSV files stored as objects                  │
│                    Port: 9000 / Console: 9090                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ETL PIPELINE (Apache Airflow)                  │
│   ┌─────────────────┐       ┌──────────────────────────────┐   │
│   │  carga_inicial  │       │    carga_incremental          │   │
│   │  (Initial Load) │       │    (Incremental Load)         │   │
│   └────────┬────────┘       └──────────────┬───────────────┘   │
│            └──────────────┬────────────────┘                   │
│                           │  DAG Orchestration                  │
│                    Port: 8080                                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DATA WAREHOUSE (MySQL 8.2)                     │
│              Database: data_warehouse_olist                      │
│    Tables: orders, customers, products, sellers, payments...    │
│                    Port: 3308                                   │
└──────────────────┬──────────────────────────┬───────────────────┘
                   │                          │
          ┌────────▼──────────┐   ┌───────────▼──────────────┐
          │  ANALYTICS DASH   │   │   MACHINE LEARNING        │
          │  (Streamlit)      │   │   (Streamlit)             │
          │  Port: 5050       │   │   Port: 5000              │
          │                   │   │                           │
          │  • KPIs           │   │  • Revenue Forecast       │
          │  • General Panel  │   │  • Product Recommend      │
          │  • Delivery Metrics│  │  • Delivery Time Predict  │
          │  • Marketing      │   │                           │
          └───────────────────┘   └───────────────────────────┘
```

---

## ✨ Tính năng

### 📊 Analytics Dashboard (Port 5050)
| Trang | Mô tả |
|-------|--------|
| 🏠 Home | Tổng quan dự án và chỉ số tóm tắt |
| 🧮 KPIs | Các chỉ số hiệu suất quan trọng: doanh thu, đơn hàng, khách hàng |
| 📊 Panel General | Phân tích tổng quan theo thời gian, danh mục, khu vực địa lý |
| 📦 Method Delivery | Phân tích phương thức và hiệu quả giao hàng |
| 💵 Marketing & Reviews | Phân tích marketing, đánh giá khách hàng, tỷ lệ chuyển đổi |

### 🤖 Machine Learning Dashboard (Port 5000)
| Trang | Mô tả |
|-------|--------|
| 🏠 Home | Tổng quan và giới thiệu các mô hình ML |
| 📈 Forecast Models | Dự báo doanh thu tương lai bằng Prophet |
| 🤝 Recommendation Models | Gợi ý sản phẩm theo collaborative filtering & content-based |
| ⏳ Delivery Time Model | Dự đoán thời gian giao hàng bằng XGBoost |

### 🔄 ETL Pipeline (Apache Airflow - Port 8080)
- **DAG carga_inicial**: Nạp toàn bộ dữ liệu lần đầu từ MinIO → MySQL
- **DAG carga_incremental**: Cập nhật dữ liệu mới theo lịch, xử lý 10 loại entity khác nhau

---

## 📁 Cấu trúc dự án

```
olist/
├── 📄 docker-compose.yml          # Orchestration toàn bộ services
├── 📄 .env                        # Biến môi trường (AIRFLOW_UID)
│
├── 📂 data_warehouse/             # ETL & Data Warehouse
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── 📂 apache_airflow/
│   │   └── 📂 dags/
│   │       ├── carga_inicial.py   # DAG: Initial data load
│   │       └── carga_incremental.py # DAG: Incremental load
│   ├── 📂 etl_module/             # ETL logic theo từng entity
│   │   ├── customer.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── order_payment.py
│   │   ├── order_review.py
│   │   ├── product.py
│   │   ├── seller.py
│   │   ├── geolocation.py
│   │   ├── closed_deal.py
│   │   └── marketing_qualified_lead.py
│   ├── 📂 datasets/               # Dữ liệu gốc (CSV)
│   └── 📂 datasets_incremental/   # Dữ liệu incremental
│
├── 📂 dashboard/                  # Analytics Dashboard
│   ├── Dockerfile
│   ├── requirements.txt
│   └── 📂 app/
│       ├── 1_🏠_Home.py
│       └── 📂 pages/
│           ├── 2_🧮_KPIs.py
│           ├── 3_📊_Panel_General.py
│           ├── 4_📦_Method_Delivery.py
│           └── 5_💵_Marketing_Reviews.py
│
├── 📂 machine_learning/           # Machine Learning Dashboard
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── 📂 models/                 # Pre-trained models (.pkl)
│   │   ├── model_prophet.pkl      # Dự báo doanh thu
│   │   ├── recomendacion_producto.pkl
│   │   ├── recomendacion_colaborativa.pkl
│   │   └── dias_espera.pkl        # Dự đoán thời gian giao
│   └── 📂 app/
│       ├── 1_🏠_Home.py
│       └── 📂 pages/
│           ├── 2_📈_Forecast_Models.py
│           ├── 3_🤝_Recomendation_Models.py
│           └── 4_⏳_Delivery_Time_Model.py
│
└── 📂 etapas_del_proyecto/        # Tài liệu các giai đoạn dự án
    └── 📂 eda_reports/
```

---

## 💻 Yêu cầu hệ thống

| Thành phần | Phiên bản tối thiểu |
|-----------|---------------------|
| Docker Desktop | 20.10+ |
| Docker Compose | 2.0+ |
| RAM | **≥ 8 GB** (khuyến nghị 12 GB+) |
| CPU | ≥ 4 cores |
| Disk | ≥ 15 GB trống |

> ⚠️ **Lưu ý**: Apache Airflow yêu cầu tối thiểu 4 GB RAM. Đảm bảo Docker Desktop được cấu hình đủ tài nguyên.

---

## 🚀 Hướng dẫn cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/Anchu003/olist.git
cd olist
```

### Bước 2: Tạo file `.env`

```bash
# Linux/macOS
echo "AIRFLOW_UID=$(id -u)" > .env

# Windows (PowerShell)
echo "AIRFLOW_UID=50000" > .env
```

### Bước 3: Khởi động toàn bộ hệ thống

```bash
docker compose up -d
```

> 🕐 Lần đầu chạy sẽ mất **5–10 phút** để build images và khởi tạo Airflow database.

### Bước 4: Kiểm tra trạng thái

```bash
docker compose ps
```

Tất cả services phải ở trạng thái `healthy` hoặc `running`.

---

## 📖 Hướng dẫn sử dụng

### 1. Upload dữ liệu lên MinIO

1. Truy cập **MinIO Console**: [http://localhost:9090](http://localhost:9090)
2. Đăng nhập: `root` / `password`
3. Tạo bucket tên `olist`
4. Upload các file CSV từ thư mục `data_warehouse/datasets/`

### 2. Chạy ETL Pipeline

1. Truy cập **Airflow**: [http://localhost:8080](http://localhost:8080)
2. Đăng nhập: `root` / `password`
3. Kích hoạt DAG `carga_inicial` để nạp dữ liệu lần đầu
4. Sau đó bật DAG `carga_incremental` để cập nhật tự động

### 3. Xem Analytics Dashboard

Truy cập: [http://localhost:5050](http://localhost:5050)

### 4. Xem Machine Learning Dashboard

Truy cập: [http://localhost:5000](http://localhost:5000)

---

## 🔧 Các dịch vụ

| Service | URL | Thông tin đăng nhập |
|---------|-----|---------------------|
| 🌀 Apache Airflow | [http://localhost:8080](http://localhost:8080) | `root` / `password` |
| 🗄️ MinIO Console | [http://localhost:9090](http://localhost:9090) | `root` / `password` |
| 📊 Analytics Dashboard | [http://localhost:5050](http://localhost:5050) | — |
| 🤖 ML Dashboard | [http://localhost:5000](http://localhost:5000) | — |
| 🐬 MySQL | `localhost:3308` | `root` / `password` |
| 🐘 PostgreSQL (Airflow DB) | `localhost:5432` | `airflow` / `airflow` |

---

## 📊 Dashboard

### Analytics Dashboard
Cung cấp cái nhìn toàn diện về hoạt động kinh doanh:
- **KPIs**: Tổng doanh thu, số đơn hàng, số khách hàng mới, rating trung bình
- **Phân tích địa lý**: Bản đồ phân phối khách hàng và người bán theo bang
- **Xu hướng thời gian**: Doanh thu và đơn hàng theo tuần/tháng/quý
- **Hiệu suất giao hàng**: Tỷ lệ giao đúng hạn, thời gian giao trung bình
- **Marketing**: Phân tích leads, tỷ lệ chuyển đổi, review sentiment

---

## 🤖 Machine Learning

### Các mô hình được triển khai

| Mô hình | Thuật toán | Mục đích |
|---------|-----------|----------|
| **Revenue Forecast** | Facebook Prophet | Dự báo doanh thu 30/60/90 ngày tới |
| **Product Recommendation** | Content-Based Filtering | Gợi ý sản phẩm tương tự |
| **Collaborative Filtering** | Matrix Factorization | Gợi ý dựa trên hành vi người dùng |
| **Delivery Time Prediction** | XGBoost Regressor | Ước tính ngày giao hàng |

---

## 📦 Dữ liệu nguồn

Dataset: **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**

| File | Mô tả |
|------|--------|
| `olist_orders_dataset.csv` | Thông tin đơn hàng |
| `olist_customers_dataset.csv` | Thông tin khách hàng |
| `olist_order_items_dataset.csv` | Chi tiết sản phẩm trong đơn |
| `olist_order_payments_dataset.csv` | Thông tin thanh toán |
| `olist_order_reviews_dataset.csv` | Đánh giá của khách hàng |
| `olist_products_dataset.csv` | Danh mục sản phẩm |
| `olist_sellers_dataset.csv` | Thông tin người bán |
| `olist_geolocation_dataset.csv` | Dữ liệu địa lý |
| `olist_closed_deals_dataset.csv` | Deals đã chốt |
| `olist_marketing_qualified_leads_dataset.csv` | Marketing leads |

---

## 🛑 Dừng hệ thống

```bash
# Dừng tất cả containers (giữ lại data)
docker compose stop

# Dừng và xóa containers (giữ lại volumes)
docker compose down

# Xóa hoàn toàn bao gồm volumes (⚠️ mất dữ liệu)
docker compose down -v
```

---

## 📄 License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.  
Dataset nguồn: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) © Olist

---

<div align="center">
Made with ❤️ | Olist Data Platform
</div>
