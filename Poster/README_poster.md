# Poster hội nghị Xác suất & Thống kê

## Tệp trong thư mục

| Tệp | Nội dung |
|:---|:---|
| `main_poster_VN.tex` / `.pdf` | Poster tiếng Việt, khổ A0 dọc, 3 cột (lớp `baposter` theo template hội thảo) |
| `main_poster_ENG.tex` / `.pdf` | Bản tiếng Anh, cùng bố cục |
| `make_figures.py` | Sinh toàn bộ biểu đồ từ `../Data/Data_tong_hop.csv` |
| `figs_vn/` , `figs_en/` | Hình đã sinh (PNG, 300 dpi) |
| `baposter.cls`, `Logo Đơn.png`, `LOGO KHOA - ĐỨNG - KHÔNG NỀN.png` | Lớp và logo của template |

## Biên dịch

```bash
pdflatex main_poster_VN.tex
```

Chạy hai lần để baposter đặt đúng vị trí các hộp. File dùng `iftex` nên cũng biên dịch
được bằng `xelatex` / `lualatex` (nhánh `fontspec`, phông TeX Gyre Pagella tương thích
metric với Palatino).

## Hình dùng làm minh chứng trong `Ket_qua.md`

Bản tiếng Việt của 12 hình được sao vào `../image/poster/` và nhúng vào `Ket_qua.md`
ngay dưới bảng tương ứng (Hình M1–M3 ở mục Phương pháp; Hình 3.17a, 3.17b, 3.18, 3.25,
3.3–3.8; Hình PS1, A, E, F ở mục Phân tích sâu). Sau khi sửa biểu đồ, chạy lại:

```bash
python Poster/make_figures.py vn && cp Poster/figs_vn/*.png image/poster/ && rm -f image/poster/f0_pipeline_tall.png
```

## Sinh lại biểu đồ

```bash
python make_figures.py vn en
```

Script đọc `../Data/Data_tong_hop.csv` (93 ca) và tính lại mọi con số, không chép tay.
Khi chạy xong, script in ra các số liệu chính để đối chiếu với phần chữ trên poster.

## Mười hình được sinh ra

| Tệp | Nội dung | Dùng trên poster |
|:---|:---|:---|
| `f0_pipeline.png` | Sơ đồ quy trình 6 bước, bố cục ngang (1×6) | ✓ poster VN |
| `f0_pipeline_tall.png` | Cùng nội dung, bố cục rắn trườn 3×2 cho cột hẹp | ✓ poster ENG |
| `f00_study_design.png` | Sơ đồ thiết kế nghiên cứu kiểu CONSORT (dòng chảy bệnh nhân) | ✓ poster ENG |
| `f1_distribution.png` | Histogram + Q–Q plot, kiểm định KS–Lilliefors | ✓ Kết quả 1 |
| `f2_severity_profile.png` | Tỉ lệ dấu hiệu nguy cơ theo độ nặng | dự phòng |
| `f3_forest_univariate.png` | Forest plot OR đơn biến (12 yếu tố) | ✓ Kết quả 1 |
| `f4_forest_multivariable.png` | Forest plot OR hiệu chỉnh, 2 mô hình logistic | ✓ Kết quả 2 |
| `f5_paired_tg.png` | Slopegraph TG trước–sau + violin tỉ lệ giảm | ✓ Kết quả 2 |
| `f6_scores_dumbbell.png` | Dumbbell APACHE II / SOFA / BISAP trước–sau | dự phòng |
| `f7_reduction_compare.png` | Tỉ lệ giảm TG + KTC của hiệu số qua 3 mốc | dự phòng |
| `f8_adjusted.png` | Hiệu chỉnh gây nhiễu, 3 mô hình log-tuyến tính | ✓ Kết quả 3 |
| `f9_pvalue_strip.png` | 33 giá trị p theo nhóm biến, ngưỡng BH và Bonferroni | ✓ Kết quả 3 |
| `f10_sensitivity.png` | 11 kịch bản độ vững | ✓ hộp Độ vững |

Ba hình dự phòng (`f2`, `f6`, `f7`) không đặt trên poster vì hết chỗ; có thể thay vào
nếu muốn đổi trọng tâm — chỉ cần sửa tên hình trong `\includegraphics`.

## Khác biệt giữa hai bản

Bản **ENG** đã được làm lại theo hướng khác bản VN:

- Hàng đầu chia thành **ba hộp**: *Clinical background and objective* (chữ) |
  *Study design* (sơ đồ `f00_study_design.png`) | *Statistical analysis pipeline*
  (sơ đồ `f0_pipeline_tall.png`). Hai hộp sau **chỉ có hình** và một dòng chú thích.
- Đặc điểm nền, phơi nhiễm và điều trị đi kèm không còn viết thành chữ mà **thể hiện bằng
  sơ đồ dòng chảy bệnh nhân**.
- Bỏ cột "số liệu chính" và chú thích dưới mỗi hình để **phóng to chart** — mỗi hình rộng
  0,45–0,54 bề ngang poster thay vì 0,29–0,36 như bản VN (lớn hơn khoảng 50%).
- Mỗi hàng kết quả chỉ còn **một dòng diễn giải** thay cho chú thích từng hình.
- Rút còn **2 tài liệu tham khảo**, đặt luôn trong hộp Kết luận (bỏ hộp riêng).
- Hộp cuối đổi tên thành **Conclusion** và viết thành **một đoạn văn liền mạch**,
  không chia mục.

Muốn áp dụng cùng cách cho bản VN thì sao chép cấu trúc hộp từ `main_poster_ENG.tex`
và dịch lại phần chữ.

## Bảng màu

Màu được chọn theo bảng đã kiểm tra tương phản và khả năng phân biệt với người mù màu
(khoảng cách OKLab giữa các cặp màu kề nhau ≥ 8). Quy ước dùng xuyên suốt:

- Albumin 5% = xanh dương `#2a78d6` · FFP = cam `#eb6834`
- Trước TPE = tím `#4a3aa7` · Sau TPE = xanh ngọc `#1baf7a`
- Nặng = đỏ `#e34948` · Trung bình–nặng = xanh dương
- Có ý nghĩa thống kê = đỏ `#e34948` · Không ý nghĩa = xám

Mỗi hộp trên poster có một màu tiêu đề riêng (xanh dương, tím, xanh lục, cam, hồng sen,
xanh lá, xám) để phân tách các phần nội dung.

## Lưu ý về `fontscale`

Trong `baposter`, **giá trị `fontscale` càng lớn thì chữ càng nhỏ** (trang được đặt ở
`fontscale × khổ giấy` rồi phóng to lên). Template gốc dùng `0.30`; poster này dùng
`0.38` để chứa đủ 7 hình và 6 hộp nội dung trên một trang A0.

## Căn lề

Lớp `baposter` đặt lề mặc định `margin=1.5cm` cho cả bốn cạnh. Hai chỗ dễ phá lề:

- **Logo trong header** được canh theo đáy chứ không canh giữa, nên logo cao hơn vùng
  header sẽ **tràn lên trên**. Hai logo có tỉ lệ khác nhau, vì vậy cùng một `height=`
  vẫn cho chiều cao mực in khác nhau — phải chỉnh riêng từng logo.
- **Nội dung dài hơn `\textheight`** thì hộp cuối cùng chạy quá đáy trang, ăn hết lề
  dưới mà không báo lỗi.

Cách kiểm tra nhanh (đo hộp bao mực in trên ảnh render):

```bash
pdftoppm -png -r 72 -singlefile main_poster_ENG.pdf /tmp/p && python -c "
from PIL import Image; import numpy as np
a=np.array(Image.open('/tmp/p.png').convert('L')); ink=a<245; H,W=a.shape
r=np.where(ink.any(axis=1))[0]; c=np.where(ink.any(axis=0))[0]
f=lambda px: round(px/72*25.4,1)
print('tren',f(r.min()),'duoi',f(H-1-r.max()),'trai',f(c.min()),'phai',f(W-1-c.max()))"
```

Hiện tại (mực in; lề thật của lớp là 15 mm, chênh lệch do nét viền hộp bo tròn):

| | Trên | Dưới | Trái | Phải |
|:---|---:|---:|---:|---:|
| ENG | 14,8 | 13,4 | 13,8 | 13,8 |
| VN | 15,9 | 15,2 | 13,8 | 13,8 |

Một bẫy nữa: **dòng affiliation dài làm khối header cao thêm một dòng**, đẩy cả logo lẫn
tiêu đề trồi lên trên lề. Nếu đổi tên cơ quan mà lề trên tụt xuống, hãy rút dòng
affiliation về đúng một dòng trước khi nghĩ tới việc thu nhỏ logo.

## Tiêu đề hình

Tiêu đề mỗi hình được viết thành **câu khẳng định kết quả** chứ không mô tả nội dung —
ví dụ "No triglyceride-efficacy endpoint reaches p < 0.05" thay cho "Multiplicity and
sensitivity analysis". Khi sửa tiêu đề cần lưu ý hai điều:

- `bbox_inches="tight"` khiến **tỉ lệ khung hình đổi theo độ dài tiêu đề và phần chú thích
  ngoài trục**, kéo theo chiều cao hộp trên poster. Kiểm lại tỉ lệ sau mỗi lần sửa.
- Hình `f3` có hai cột số ở bên phải đặt theo toạ độ trục (`x = 1.04` và `1.44`); tiêu đề
  căn trái quá dài sẽ đè lên các cột này.
