## DỰ ÁN CUỐI KỲ - OLIST E-COMMERCE
## GIAI ĐOẠN 1

## HIỂU BIẾT VỀ TÌNH HUỐNG

## Olist là hệ sinh thái dịch vụ kỹ thuật số hỗ trợ bán hàng trực tuyến. Nhu cầu cốt lõi của người bán là tăng doanh số, cải thiện hiệu quả và thu hút khách hàng mới. Sứ mệnh của Olist là thúc đẩy thương mại bán lẻ số, loại bỏ rào cản và giúp nhà bán lẻ bán nhiều hơn bằng cách chuyển đổi hoạt động trực tiếp sang trực tuyến.
## Trong dự án này, nhóm được cung cấp dữ liệu từ Olist giai đoạn 2016-2018, bao gồm các phòng ban Bán hàng, Logistics và Marketing. Nhiệm vụ là tư vấn dựa trên phân tích dữ liệu để đưa ra giải pháp cải thiện hiệu quả kinh doanh.

## MỤC TIÊU DỰ ÁN

## Mục tiêu chung:

## Thực hiện quy trình ETL (Extract, Transform, Load) để xử lý dữ liệu kinh doanh.
## Xây dựng và phân tích KPI, chỉ số hỗ trợ ra quyết định.
## Triển khai mô hình Machine Learning cho phân tích dự đoán và gợi ý.

## Mục tiêu cụ thể:
## 1.1. Phân tích khám phá dữ liệu (EDA) toàn diện, thiết kế kiến trúc dữ liệu phù hợp, cung cấp đầu vào cho dashboard và mô hình ML.
## 1.2. Xây dựng dashboard trực quan để giám sát KPI, phát hiện mẫu và insight.
## 2.1. Phát triển hệ thống gợi ý sản phẩm dựa trên lịch sử và hành vi khách hàng tương đồng.
## 2.2. Xây dựng mô hình dự đoán doanh số dựa trên xu hướng lịch sử.

## PHẠM VI

## Dự án sử dụng bộ dữ liệu Marketplace e-commerce của Olist, tập trung phân tích khám phá bằng Python để đánh giá nội dung, chất lượng và tiềm năng của các đặc trưng.
## Dự án chia thành 4 giai đoạn:

## Giai đoạn 1: Xác định mục tiêu, phạm vi, thiết lập repo, đề xuất giải pháp, phân công vai trò, lập lịch trình.
## Giai đoạn 2: Data Engineering – ETL, thiết kế Data Warehouse, tự động hóa, tài liệu hóa.
## Giai đoạn 3: Data Analytics & ML – mockup dashboard, xây dựng mô hình, chuẩn bị storytelling.
## Giai đoạn 4: Hoàn thiện sản phẩm – dashboard, kiểm thử, cập nhật repo và tài liệu.


## PHÂN TÍCH DỮ LIỆU SƠ BỘ


## Dataset geolocation: Chứa tọa độ không thuộc Brazil, tên thành phố chưa chuẩn hóa → Giải pháp: thay thế bằng dữ liệu bưu chính chính thức.
## Dataset products: Có giá trị null nhưng thuộc các hàng trống hoàn toàn → Loại bỏ hàng.
## Dataset closed deals: Phát hiện outlier ở doanh số hàng tháng → Phân tích và xử lý để đảm bảo độ tin cậy.

## Kết luận: Phân tích sơ bộ giúp phát hiện vấn đề chất lượng dữ liệu, định hướng xử lý và xác định khu vực cần nghiên cứu sâu hơn.

## CÔNG NGHỆ SỬ DỤNG


## Nguồn dữ liệu: File .csv, hỗ trợ tải gia tăng.
## ETL & Tự động hóa: Apache Airflow (lập lịch, chạy song song, giám sát, cảnh báo lỗi).
## Data Warehouse: MySQL (tối ưu lưu trữ và truy vấn phân tích).
## Đầu ra: Dashboard (Power BI/Tableau), mô hình ML (Python).



## KPIKhu vựcMục tiêuCông thứcĐơn vịMục tiêu đề xuấtBiến động doanh số tháng (VVV)Bán hàngĐánh giá tăng giảm$VVV = \frac{V_{actual} - V_{anterior}}{V_{anterior}} \times ## 100$%10%Net Promoter Score (PN)Bán hàngĐo lường hài lòng$PN = \%\text{positive} - \%\text{negative}$%60%Tỷ lệ khách hàng quay lại (FC)Bán hàngĐo lường khách trung thành$FC = ## \frac{\text{Khách quay lại}}{\text{Tổng khách}} \times 100$%5%Tỷ lệ chuyển đổi (TC)MarketingĐo lường hiệu quả thu hút$TC = \frac{\text{Người bán gia nhập}}{\text{Người bán tiềm ## năng}} \times 100$%15%Giao hàng đúng hạn (PE)LogisticsĐo lường hiệu quả vận hành$PE = \frac{\text{Đơn đúng hạn}}{\text{Tổng đơn}} \times 100$%95%Tổng thời gian xử lý (TTP)## LogisticsTối ưu quy trình$TTP = \frac{1}{N} \sum (F_{nhận} - F_{mua})$ngày8 ngày

## LỊCH TRÌNH (dự kiến)


## Tuần 1-2: Giai đoạn 1 – Hoàn thiện đề xuất, phân công, thiết lập repo.
## Tuần 3-5: Giai đoạn 2 – ETL, Data Warehouse, tự động hóa.
## Tuần 6-8: Giai đoạn 3 – Dashboard, mô hình ML, storytelling.
## Tuần 9-10: Giai đoạn 4 – Hoàn thiện, kiểm thử, trình bày.

## GIẢI PHÁP ĐỀ XUẤT


## Kiến trúc tổng thể: Dữ liệu → Airflow (ETL) → MySQL → Dashboard & ML.
## Tự động hóa: Pipeline hàng ngày/tuần, kiểm tra chất lượng dữ liệu.
## Mô hình ML:
## Hệ thống gợi ý: Collaborative Filtering + Content-based.
## Dự đoán doanh số: Time Series (Prophet, LSTM).

## Dashboard: Theo dõi KPI theo thời gian thực, phân tích theo khu vực, danh mục.
## Báo cáo: Insight hàng quý, đề xuất hành động cho Bán hàng, Marketing, Logistics.