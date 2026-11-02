# Viêm tụy cấp do tăng triglyceride được thay huyết tương: từ điển dữ liệu

Từ điển này mô tả `Data_viem_tuy_cap.csv` (93 bệnh nhân, 190 cột) dùng cho luận án *thay huyết tương (TPE) trong viêm tụy cấp do tăng triglyceride*.

**Cỡ mẫu:** 93 bệnh nhân, 59 TPE bằng albumin 5% và 34 bằng FFP.

**Thiết kế (theo luận án):** quan sát, tiến cứu, 6/2018 – 6/2023, tại khoa Hồi sức cấp cứu BV Chợ Rẫy và khoa Hồi sức tích cực BV Đại học Y Dược TP.HCM.

**Tiêu chuẩn chọn:** ≥ 18 tuổi, TG nhập viện ≥ 1000 mg/dL, APACHE II ≥ 8, được TPE. Cả 93 bệnh nhân đều đạt ngưỡng TG và APACHE II trong CSV.

**Tiêu chuẩn loại:** đã TPE ở tuyến trước, hoặc bệnh nhân/gia đình không đồng ý TPE.

**Mốc thời gian:** hậu tố `_0` là lúc nhập viện hoặc trước TPE lần 1 (TG lấy lại nếu chờ TPE > 6 giờ, xét nghiệm khác nếu > 12 giờ). Hậu tố `_1` là sau TPE lần 1 và `_2` là sau TPE lần 2 (lấy trong vòng 1–2 giờ sau TPE).

**Các file:**

| File | Vai trò |
| :--- | :--- |
| `Data_tong_hop.csv` | **Bộ dữ liệu tổng hợp để phân tích:** 93 bệnh nhân, 359 cột, gồm toàn bộ CSV, các cột nhãn chữ và cột `bs_*` của 60 bệnh nhân ghép được |
| `Bo_sung_an_danh.csv` | Toàn bộ dữ liệu bổ sung đã ẩn danh: 93 bệnh nhân, 166 cột. Dùng cho thống kê chung của cả 93 ca |
| `Data_viem_tuy_cap.csv` | Bộ dữ liệu ban đầu; các mục 1–7 mô tả các cột của file này |
| `Data_viem_tuy_cap.xlsx` | Bản Excel của CSV |
| `Luận án 29.3.2025.final.pdf` | Định nghĩa biến, quy trình TPE, các bảng kết quả |

Các bảng dữ liệu này có thể không phải bản gốc đã dùng để viết luận án, nên chênh lệch với luận án ở [mục 8](#8-đối-chiếu-csv-với-luận-án) là điều cần lưu ý khi diễn giải.

**Ký hiệu cột "Nguồn":**

- **DL:** đã kiểm chứng trực tiếp trên dữ liệu, quy tắc đúng ở cả 93 bệnh nhân nếu không ghi chú khác.
- **Gốc:** giải mã từ bảng dữ liệu nguồn có tên cột và mã hóa dạng chữ. Bảng này chỉ khác CSV ở 3 ô (`billirubin_tp_0`, `billirubin_tt_0` ở STT 25; `apa_giam...187` ở STT 31) và CSV được giữ làm chuẩn.
- **LA:** theo định nghĩa trong luận án, chưa kiểm chứng được trên dữ liệu.
- **Suy luận:** suy ra từ khoảng giá trị.
- **Chưa rõ:** cần xác nhận với tác giả.

---

## Lưu ý quan trọng trước khi phân tích

1. **`mof_tim_*`, `mof_phoi_*`, `mof_than_*` không phải suy cơ quan.** Ba cột này khớp hoàn toàn với ngưỡng nhịp tim, nhịp thở và ure. Xem [mục 5](#5-thang-điểm-độ-nặng-và-hình-ảnh-học).
2. **`Atlanta_0`, `Atlanta_1` không phải độ nặng Atlanta 2012.** Chúng bằng đúng tổng ba cờ `mof_*` (93/93 bệnh nhân) nên có giá trị 0–3, và không thể dùng làm độ nặng.
3. **`sofa_0` thấp hơn SOFA trong luận án đúng 3 điểm.** Xem [mục 8](#8-đối-chiếu-csv-với-luận-án).
4. **Số tử vong:** CSV có 6 ca, luận án có 4 ca.
5. **`dich_bu` là giá trị tính ra, không phải thể tích dịch đo được:** `dich_bu = 0,048 × can_nang`.
6. **`tg_2`, `sofa_2`, `apache_ii_2` không phải đo lần 2 ở 80 bệnh nhân TPE 1 lần.** Chỉ phân tích `_2` ở 13 bệnh nhân có `so_lan_pex = 2`.
7. **`apa_giam...188` và `apa_giam...189` là mức giảm TG, không phải APACHE II.**
8. **Chỉ 60/93 bệnh nhân có dữ liệu bổ sung ghép được.** Cột `bs_*` trống ở 33 ca còn lại. Xem [mục 9](#9-dữ-liệu-bổ-sung-chưa-có-trong-csv).

---

## 1. Nhân khẩu học và thể trạng

| Biến | Loại | Đơn vị / Mã hóa | Định nghĩa | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| `Unnamed: 0` | Định danh | Số nguyên | Chỉ số dòng do xuất file, trùng `STT`; bỏ khi phân tích | DL |
| `STT` | Định danh | 1–93 | Số thứ tự nghiên cứu. Không trùng với `Số TT` trong file Bổ sung | DL |
| `Nam_sinh` | Định lượng | Năm | Năm sinh | Gốc |
| `tuoi` | Định lượng | Năm | `tuoi = 2023 − Nam_sinh` ở cả 93 ca. Luận án định nghĩa là năm vào viện − năm sinh, nên đây **không phải tuổi lúc nhập viện** | DL |
| `gioi_tinh` | Nhị giá | `0`: Nam; `1`: Nữ | 4 ca có thai đều ở nhóm `1`. Chú thích "1=nam, 2=nữ" trong file gốc đã lỗi thời | DL |
| `nghe_nghiep` | Danh định | `1`: Văn phòng; `2`: Buôn bán; `3`: Lao động | Nghề nghiệp | Gốc |
| `can_nang` | Định lượng | kg | Cân nặng. Có 1 ca 174 kg | Gốc |
| `chieu_cao` | Định lượng | cm | Chiều cao | Gốc |
| `bmi` | Định lượng | kg/m² | `can_nang / (chieu_cao/100)²` | DL |

**Nhóm BMI** không có cột trong CSV. Mốc tái lập được Bảng 3.3 là < 18,5 / 18,5–< 25 / 25–< 30 / ≥ 30 (2/49/31/11 ca). Bảng 2.1 của luận án lại ghi mốc châu Á – Thái Bình Dương (23 và 25), không khớp với kết quả đã báo cáo.

---

## 2. Tiền căn và bệnh kèm

| Biến | Loại | Đơn vị / Mã hóa | Định nghĩa | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| `dtd` | Nhị giá | `0`: Không; `1`: Có | Đái tháo đường theo ADA 2020: glucose đói ≥ 126 mg/dL, bất kỳ ≥ 200 mg/dL, nghiệm pháp dung nạp ≥ 200 mg/dL, hoặc HbA1c ≥ 6,5% | LA |
| `tha` | Nhị giá | `0`: Không; `1`: Có | Tăng huyết áp: HATT ≥ 140 và/hoặc HATTr ≥ 90 mmHg | LA |
| `rllm` | Nhị giá | `0`: Không; `1`: Có | Rối loạn lipid máu theo NCEP-ATP III | LA |
| `nghien_ruou` | Nhị giá | `0`: Không; `1`: Có | Có 1 trong 3 biểu hiện kéo dài 12 tháng: thèm buộc phải uống, không bỏ được, hội chứng cai | LA |
| `soi_mat` | Nhị giá | `0`: Không; `1`: Có | Sỏi mật | Gốc |
| `sd_tranhthai` | Nhị giá | `0`: Không; `1`: Có | Dùng thuốc tránh thai | Gốc |
| `tien_su_vtc` | Nhị giá | `0`: Không; `1`: Có | Từng bị viêm tụy cấp | Gốc |
| `so_lan_vtc` | Định lượng | Lần | Số lần viêm tụy cấp trước đây; `0` khi `tien_su_vtc = 0` | DL |
| `co_thai_1` | Nhị giá | `0`: Không; `1`: Có | Có thai. Là biến nền dù mang hậu tố `_1` | Gốc |

---

## 3. Lâm sàng lúc nhập viện

| Biến | Loại | Đơn vị / Mã hóa | Định nghĩa | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| `thoi_gian_nhap_vien` | Thời gian | Chữ / số serial | Thời điểm nhập viện, nhiều định dạng (`14h 9/6/2020`, `3h 1/2`, `20/2`...). 23 ô là số serial Excel. Nhiều ô thiếu năm, và năm thường không khớp `bs_nam_nv` ngay cả ở các ca ghép chắc chắn, nên cột này **không đáng tin** | DL |
| `gio_khoi_phat` | Thứ tự | `6`, `12`, `24`, `48`, `72` giờ | Khởi phát đến nhập viện **đã gộp nhóm**, chỉ có 5 giá trị. Số ca 2/21/32/26/12 khớp nhóm < 6 / 6–12 / 13–24 / 25–48 / > 48 giờ của Bảng 3.5, nên giá trị `6` tương ứng nhóm < 6 giờ | DL |
| `dau_bung_0` | Nhị giá | `0`: Không; `1`: Có | Đau bụng | Gốc |
| `noi_oi_0` | Nhị giá | `0`: Không; `1`: Có | Buồn nôn hoặc nôn | Gốc |
| `sot_0` | Nhị giá | `0`: Không; `1`: Có | Sốt > 38,3 °C. Khớp `nhiet_do_0` ở 87/93 ca | LA |
| `nhip_tim_0` | Định lượng | Lần/phút | Nhịp tim | Gốc |
| `sys_0` | Định lượng | mmHg | Huyết áp tâm thu | Gốc |
| `dia_0` | Định lượng | mmHg | Huyết áp tâm trương | Gốc |
| `map_0` | Định lượng | mmHg | `dia_0 + (sys_0 − dia_0)/3` | DL |
| `nhip_tho_0` | Định lượng | Lần/phút | Nhịp thở | Gốc |
| `nhiet_do_0` | Định lượng | °C | Thân nhiệt | Gốc |
| `glasgow_0` | Định lượng | Điểm, 3–15 | Điểm Glasgow | Gốc |
| `dich_bu` | Định lượng | Lít | **Giá trị tính ra:** `0,048 × can_nang`, tức 2 mL/kg/giờ × 24 giờ. Không phải dịch thực truyền | DL |

---

## 4. Xét nghiệm

Bảng dưới gộp các mốc đo của cùng một xét nghiệm. Số trong ngoặc là số bệnh nhân có giá trị ở mốc `_0`, nếu không đủ 93.

| Biến (`_0` / `_1` / `_2`) | Đơn vị | Nội dung | Nguồn |
| :--- | :--- | :--- | :--- |
| `wbc_0` / `wbc_1` / `wbc_2` | G/L | Bạch cầu | Gốc |
| `rbc_0` / `rbc_1` | T/L | Hồng cầu | Gốc |
| `hb_0` / `hb_1` / `hb_2` | **g/L** | Hemoglobin. Giá trị trung bình 167 nên là g/L, không phải g/dL như Bảng 2.1 | Suy luận |
| `hct_0` / `hct_1` / `hct_2` | % | Hematocrit | Gốc |
| `plt_0` / `plt_1` / `plt_2` | G/L | Tiểu cầu | Gốc |
| `pt_0` / `pt_1` / `pt_2` | Giây | Thời gian prothrombin | Gốc |
| `aptt_0` / `aptt_1` / `aptt_2` | Giây | aPTT | Gốc |
| `fibrinogen_0` (56) / `fibrinogen_1` / `fibrinogen_2` | g/L | Fibrinogen | Gốc |
| `crp_0` (44) / `crp_1` / `crp_2` | mg/L | CRP. Đơn vị theo Bảng 2.1; mốc "150 mg/dL" ở các bảng khác là lỗi đơn vị | LA |
| `procalcitonin_0` (10) | ng/mL | Procalcitonin | Gốc |
| `ldh_0` (9) / `ldh_1` | U/L | LDH | Gốc |
| `ast_0` (44) / `ast_1` | U/L | AST | Gốc |
| `alt_0` (44) / `alt_1` | U/L | ALT | Gốc |
| `ure_0` / `ure_1` / `ure_2` | mg/dL | Trung bình 24,9, trong khi BUN của luận án là 17,6. Trên 20 ca so sánh được, tỉ số so với BUN có trung vị 1,0 nhưng tứ phân vị trên 2,09, nên **có thể trộn lẫn ure và BUN** (BUN = ure ÷ 2,14) | Chưa rõ |
| `creatinin_0` / `creatinin_1` / `creatinin_2` | mg/dL | Creatinine | Gốc |
| `egfr_0` / `egfr_1` / `egfr_2` | mL/phút/1,73 m² | eGFR. Lệch nhiều so với CKD-EPI 2021 ở một số ca | Chưa rõ |
| `albumin_0` (16) / `albumin_1` | g/L | Albumin | Gốc |
| `billirubin_tp_0` (76) / `billirubin_tp_1` | **mg/dL** | Bilirubin toàn phần. Trung vị 0,86 nên là mg/dL, không phải µmol/L. `billirubin_tp_1` có giá trị 55 cần kiểm tra. `billirubin_tp_0` là chuỗi vì có khoảng trắng không ngắt | Suy luận |
| `billirubin_tt_0` (73) / `billirubin_tt_1` | **mg/dL** | Bilirubin trực tiếp | Suy luận |
| `na_0` / `na_1` / `na_2` | mmol/L | Natri. `na_0` trung bình 127,9; cộng hiệu chỉnh `tg_NV × 0,002` được 135,9; luận án ghi 132,8. Chưa xác định cột đã hiệu chỉnh hay chưa | Chưa rõ |
| `k_0` / `k_1` / `kali_2` | mmol/L | Kali. Tên cột mốc `_2` khác hai mốc trước | Gốc |
| `cl_0` / `cl_1` / `cl_2` | mmol/L | Clo | Gốc |
| `ca_0` (44) / `ca_1` | mmol/L | Canxi toàn phần. `ca_1` là chuỗi vì có khoảng trắng không ngắt | Gốc |
| `amylase_0` (43) / `amylase_1` / `amylase_2` | U/L | Amylase | Gốc |
| `lipase_0` (77) / `lipase_1` / `lipase_2` | U/L | Lipase | Gốc |
| `glucose_0` | mg/dL | Glucose. Có giá trị 18 cần kiểm tra | Gốc |
| `hba0c_0` (29) | % | HbA1c (tên cột gõ nhầm) | Gốc |
| `ceton_0` (29) | Chưa rõ | Ceton **định lượng**, 0–100, không phải nhị giá. Có thể trộn đơn vị máu và nước tiểu | Chưa rõ |
| `pH_mau_0` / `ph_mau_1` / `ph_2` | – | pH máu động mạch | Gốc |
| `paco2_0` (85) / `paco2_1` / `paco2_2` | mmHg | PaCO₂ | Gốc |
| `pao2_0` / `pao2_1` / `pao2_2` | mmHg | PaO₂ | Gốc |
| `hco3_0` / `hco3_1` / `hco3_2` | mmol/L | Bicarbonate | Gốc |
| `fio2_0` (63) / `fio2_1` / `fio2_2` | Thập phân | FiO₂. `fio2_1 = 32` ở STT 83 là lỗi nhập, gần như chắc là 0,32 | Gốc |
| `pao2/fio2_0` (86) / `pao2/fio2_1` / `pao2_fio2` | mmHg | PaO₂/FiO₂. `pao2_fio2` là mốc `_2` | Gốc |
| `lactate_0` (51) / `lactate_1` / `lactate_2` | mmol/L | Lactate. `lactate_0 = 63,32` cần kiểm tra | Gốc |

**Triglyceride**

| Biến | Đơn vị | Nội dung | Nguồn |
| :--- | :--- | :--- | :--- |
| `tg_NV` | mg/dL | TG **lúc nhập viện**. Đây là giá trị "trước TPE" dùng trong luận án (3987,3 ± 2918,3) | Gốc, DL |
| `TG_0` | mg/dL | TG **ngay trước TPE lần 1** (tên gốc `TG_truoc_pex`). Khác `tg_NV` ở 10 ca | Gốc |
| `tg_1` | mg/dL | TG sau TPE lần 1 | Gốc |
| `tg_2` | mg/dL | TG sau TPE lần 2. Ở 80 ca TPE 1 lần, cột này chép lại `tg_1` | DL |
| `tg_giam` | mg/dL | `tg_NV − tg_1` ở 89 ca. Bốn ca TPE 2 lần (STT 15, 27, 62, 66) dùng `tg_NV − tg_2`. **Không nhất quán:** 9 ca TPE 2 lần còn lại không tính đến lần 2 | DL |
| `%tg_giam` | **Tỉ lệ 0–1** | `tg_giam / tg_NV`; nhân 100 để ra % (trung bình 77,8%) | DL |
| `apa_giam...188` | mg/dL | TG giảm trong TPE lần 2: `tg_1 − tg_2`; 13 ca (tên gốc `apa2 giam`) | DL |
| `apa_giam...189` | Tỉ lệ 0–1 | `apa_giam...188 / tg_1`; 13 ca (tên gốc `%apa2 giam`) | DL |

---

## 5. Thang điểm, độ nặng và hình ảnh học

**Thang điểm đã kiểm chứng**

| Biến | Đơn vị | Định nghĩa | Nguồn |
| :--- | :--- | :--- | :--- |
| `apache_ii_0` / `apache_ii_1` | Điểm | APACHE II lúc nhập viện / sau TPE 1 | Gốc |
| `apache_ii_2` | Điểm | Sau TPE 2. Ở 80 ca TPE 1 lần, cột này chép lại `apache_ii_1` | DL |
| `mor_du_doan_0` / `mor_du_doan_1` | % | Tử vong dự đoán: `100 × e^L / (1 + e^L)`, `L = −3,517 + 0,146 × APACHE II` | DL |
| `Mor_du_doan_2` | % | Công thức trên với `apache_ii_2`; 13 ca | DL |
| `sofa_0` / `sofa_1` | Điểm | SOFA. `sofa_0` trung bình 4,2; **luận án 7,2** (xem [mục 8](#8-đối-chiếu-csv-với-luận-án)) | Gốc, DL |
| `sofa_2` | Điểm | Sau TPE 2. Ở TPE 1 lần thường chép lại `sofa_1`, nhưng khác ở 6 ca chưa rõ lý do (STT 25, 43, 60, 68, 82, 92) | DL |
| `ranson_0` | Điểm | Chỉ có giá trị 0–2, nên không phải Ranson đầy đủ 0–11 | Chưa rõ |
| `ctsi_0` | Điểm | CTSI (3–10). Chỉ 65/93 ca khớp công thức điểm viêm + điểm hoại tử; 17 ca `ctsi_0 ≥ 6` có `hoai_tu_0 = 0` | DL |
| `balthazar_0` | Thứ tự | Độ Balthazar: `3`: C; `4`: D; `5`: E. Là **độ**, không phải điểm | Gốc |
| `bisap_0` / `bisap_1` | Điểm, 0–5 | BISAP, bằng tổng năm thành phần bên dưới | DL |
| `bisap_giam` | Điểm | `bisap_0 − bisap_1` | DL |
| `apa_giam...187` | Điểm | `apache_ii_0 − apache_ii_2` (giảm APACHE II toàn đợt, tên gốc `apagiam`) | DL |

**Thành phần BISAP**

| Biến (`_0` / `_1`) | Quy tắc thực tế trong dữ liệu | Nguồn |
| :--- | :--- | :--- |
| `b_0` / `b_1` | `ure > 25` | DL |
| `i_0` / `i_1` | Glasgow **≤ 12**, không phải < 15 | DL |
| `s_0` / `s_1` | SIRS ≥ 2, chỉ dùng nhiệt độ, nhịp tim, nhịp thở và bạch cầu. Ở `s_0`, khớp 91/93 ca; STT 31 và 48 lệch ở mốc nhịp tim đúng bằng 90. Tổng 63 ca, luận án 56 ca | DL |
| `a_0` / `a_1` | `tuoi > 60`; hai cột giống hệt nhau | DL |
| `p_0` / `p_1` | Tràn dịch màng phổi; hai cột giống hệt nhau. 28 ca, luận án 46 ca | DL |

**Các cột `mof_*` và `Atlanta_*`: tên cột không đúng với nội dung**

| Biến (`_0` / `_1`) | Tên gợi ý | Quy tắc thực tế (100% khớp) | Nguồn |
| :--- | :--- | :--- | :--- |
| `mof_tim_0` / `mof_tim_1` | Suy tuần hoàn | `nhip_tim ≥ 90` | DL |
| `mof_phoi_0` / `mof_phoi_1` | Suy hô hấp | `nhip_tho > 20` | DL |
| `mof_than_0` / `mof_than_1` | Suy thận | `ure ≥ 28` | DL |
| `Atlanta_0` / `Atlanta_1` | Độ nặng Atlanta 2012 | `mof_tim + mof_phoi + mof_than`, giá trị 0–3 | DL |

Các ngưỡng trên được suy ra từ dữ liệu, chưa rõ ý nghĩa lâm sàng. Chúng không phải định nghĩa suy cơ quan Marshall (PaO₂/FiO₂, creatinine, huyết áp) và `Atlanta_0` không phân loại nhẹ / trung bình-nặng / nặng.

Bảng 3.4 của luận án báo cáo 78 ca trung bình-nặng và 15 ca nặng. Các con số này trùng với `Atlanta_0` thuộc {1, 2} và {0, 3}, nhưng nhóm {0, 3} gồm cả 3 ca không có cờ nào, nên khó có thể là định nghĩa thật của nhóm nặng. Hiện chưa có file nào cho biết độ nặng Atlanta thật của từng bệnh nhân.

**Hình ảnh học**

| Biến | Mã hóa | Định nghĩa | Nguồn |
| :--- | :--- | :--- | :--- |
| `hoai_tu_0` | `0`: Không; `1`: Có | Hoại tử. 20 ca; luận án 32 ca hoại tử tụy và 26 ca hoại tử quanh tụy trên CT | Gốc |
| `phu_ne_0` | `0`: Không; `1`: Có | Phù nề. 29 ca; luận án 86 ca trên CT | Gốc |
| `tu_dich_0` | `0`: Không; `1`: Có | Tụ dịch. 27 ca; luận án 85 ca trên CT | Gốc |

---

## 6. Thay huyết tương

| Biến | Loại | Đơn vị / Mã hóa | Định nghĩa | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| `so_lan_pex` | Định lượng | `1` (80 ca); `2` (13 ca) | Số lần TPE. TPE lần 2 khi TG sau lần 1 ≥ 1000 mg/dL, cách khoảng 24 giờ | Gốc, LA |
| `onset_pex_0` | Thời gian | Chữ / số serial | **Thời điểm bắt đầu TPE lần 1**, không phải số giờ; 92 ca. Cần đổi sang giờ để tính thời gian đến TPE | DL |
| `onset_pex_1` | Thời gian | Chữ / số serial | Thời điểm bắt đầu TPE lần 2; 13 ca | Gốc |
| `PP_PEX1` | Danh định | `0`: Albumin 5% (59 ca); `1`: FFP (34 ca) | Dịch thay thế lần 1. Không phân ngẫu nhiên: lựa chọn phụ thuộc sự sẵn có và điều kiện kinh tế của bệnh nhân | Gốc, LA |
| `PP_PEX2` | Danh định | `0`: Albumin 5% (7 ca); `1`: FFP (6 ca) | Dịch thay thế lần 2 | Gốc |
| `machine_1` | Danh định | `1`: Prismaflex (52); `2`: Diapact (34); `3`: Omniselect (7) | Máy TPE. Luận án chỉ ghi Prismaflex | Gốc |
| `loai_qua_loc_1` | Danh định | `1`: PrismaFlex TPE 2000 (54); `2`: Hemoselect (34); `3`: OMNIset TPE (5) | Quả lọc. Luận án chỉ ghi TPE1000 | Gốc |
| `vi_tri_catheter_1` | Danh định | `1`: `tmdp` (90); `2`: `tmcp` (1); `3`: `tmdt` (2) | Vị trí catheter. Mã chữ gốc nhiều khả năng là tĩnh mạch đùi phải, cảnh phải, đùi trái | Gốc, Suy luận |
| `qb_1` | Định lượng | mL/phút | Tốc độ máu. Thực tế 100–200, trung bình 171; quy trình trong luận án ghi 80–100 | DL |
| `qr_1` | Định lượng | mL/giờ | Tốc độ dịch thay thế, 150–1800. Giá trị 150 cần kiểm tra | Gốc |
| `v_huyet_tuong_1` | Định lượng | mL | Thể tích huyết tương ước tính | Gốc |
| `thay_the_1` | Định lượng | `1,0`; `1,5`; `2,0`; `2,5` | Hệ số thay thế so với thể tích huyết tương | Gốc |
| `v_thay_the_1` | Định lượng | mL | Thể tích dịch thay thế; xấp xỉ `v_huyet_tuong_1 × thay_the_1`, đúng tuyệt đối ở 57/93 ca | DL |
| `heparin_bolus_1` | Định lượng | UI | Heparin liều đầu; 41 ca có dữ liệu, 3 ca bằng 0 | Gốc |
| `heparin_duy_tri_1` | Định lượng | UI/giờ | Heparin duy trì; 41 ca có dữ liệu | Gốc |
| `so_qua_loc_1` | Định lượng | Cái | Số quả lọc dùng trong TPE lần 1 (1–3) | Gốc |
| `thoi_gian_loc_1` | Định lượng | Giờ | Thời gian TPE; chỉ có `3`, `3,5`, `4`, `5`, trung bình 3,24 (luận án 2,8) | Gốc |
| `crtt_1` | Định lượng | Chưa rõ | CRRT (tên gốc `crrt`). Giá trị 0–14 nên **không phải nhị giá**, có thể là số lần hoặc số ngày. 55 ca khác 0; luận án 59 ca. Mọi ca `crtt_1 > 0` đều có CRRT trong dữ liệu bổ sung, nhưng một số ca CRRT có `crtt_1 = 0`; ưu tiên `bs_crrt` | Chưa rõ |
| `tho_may` | Nhị giá | `0`: Không; `1`: Có | Thở máy. **Chỉ 21 ca**, trong khi luận án và dữ liệu bổ sung đều là 69 ca, và không liên quan với `bs_tho_may` ở các ca đã ghép. Dùng `bs_tho_may` thay thế | Chưa rõ |

---

## 7. Theo dõi và kết cục

| Biến | Loại | Đơn vị / Mã hóa | Định nghĩa | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| `nhip_tim_1` | Định lượng | Lần/phút | Nhịp tim sau TPE 1 | Gốc |
| `nhip_tho_1` | Định lượng | Lần/phút | Nhịp thở sau TPE 1 | Gốc |
| `glasgow_1` / `glasgow_2` | Định lượng | Điểm | Glasgow sau TPE 1 / TPE 2 | Gốc |
| `los` | Định lượng | Ngày | Thời gian nằm viện: xuất viện − nhập viện. Có giá trị 150, 240 và 240 ngày, khiến trung bình 15,7 nhưng trung vị chỉ 8 | Gốc, LA |
| `Mor_thuc` | Nhị giá | `0`: Sống; `1`: Tử vong | Tử vong nội viện hoặc bệnh nặng xin về. **6 ca (6,5%)**; luận án 4 ca (4,3%) | Gốc, LA |

Các cột còn lại ở mốc `_1`, `_2` đã liệt kê ở mục 4 và 5.

---

## 8. Đối chiếu CSV với luận án

**Không tái lập được toàn bộ luận án chỉ từ CSV.** Các bảng của luận án khớp một phần với CSV và một phần với dữ liệu bổ sung (`Bo_sung_an_danh.csv`, gọi tắt là "Bổ sung" trong các bảng dưới).

**Khớp với CSV**

Tiền căn (ĐTĐ 53, THA 20, RLLM 20, rượu 15, VTC 27, có thai 4); BMI trung bình và phân nhóm; số lần TPE; TG trước và sau, mức giảm 3271,9 mg/dL, 77,8%; APACHE II 16,9 chung và theo nhóm; BISAP ≥ 3 (24 ca); CTSI ≥ 6 (37 ca); PaO₂/FiO₂ 337,9; glucose 262,4; tiểu cầu 231,9; aPTT 35,4; Qb 171,1; Qr 1325,3; nằm viện 15,7 chung, 8,6 và 27,9 theo nhóm.

**Khớp với file Bổ sung, không khớp CSV**

| Chỉ số | Luận án | Bổ sung | CSV |
| :--- | :--- | :--- | :--- |
| Tuổi | 40,2 ± 8,0 | 40,2 ± 7,9 (năm vào viện − năm sinh) | 41,8 ± 8,6 |
| Hct (%) | 43,1 | 43,2 | 44,4 |
| BUN (mg/dL) | 17,6 | 17,7 | 24,9 (`ure_0`) |
| Creatinine (mg/dL) | 1,28 | 1,29 | 1,46 |
| Nhiễm toan ceton | 39 | 39 | không có cột |
| Sốc | 19 | 19 | không có cột |
| Thở máy | 69 | 69 | 21 |
| Suy 1 / 2 / 3 cơ quan | 13 / 11 / 6 | 13 / 12 / 6 | không có cột |

**Không khớp với cả hai, hoặc chưa tìm thấy nguồn**

| Chỉ số | Luận án | CSV | Ghi chú |
| :--- | :--- | :--- | :--- |
| Giới nam / nữ | 66 / 27 | 64 / 29 | Bổ sung: 65 / 28 |
| SOFA trung bình | 7,2 ± 3,0 | 4,2 ± 3,0 | Xem dưới bảng |
| SOFA ≥ 7 | 49 ca | 21 ca | `sofa_0 ≥ 4` cho đúng 49 ca |
| Tử vong | 4 | 6 | Xem dưới bảng |
| Đau bụng | 93 | 85 | |
| Buồn nôn / nôn | 73 | 48 | |
| Sốt | 13 | 11 | |
| Tràn dịch màng phổi | 46 | 28 | |
| Creatinine > 1,9 mg/dL | 18 | 26 | |
| Hct > 44% | 40 | 46 | |
| Dịch thay thế (mL) | 3418,9 | 3747,3 | |
| Thời gian TPE (giờ) | 2,8 | 3,24 | |
| Mức giảm TG thấp nhất (mg/dL) | 763 | 195 | STT 44 |

**SOFA:** giá trị luận án bằng đúng `sofa_0 + 3` ở mọi chỗ đối chiếu được: trung bình chung, độ lệch chuẩn, hai nhóm (6,4 và 8,5 so với 6,41 và 8,59) và số ca SOFA ≥ 7. Không file nào giải thích khoản cộng 3 điểm này.

**Tử vong:** so theo TG nhập viện, 4 ca trong Bảng 3.30 tương ứng STT 43, 60, 68, 92; hai ca thêm trong CSV là STT 61 và 80. Tuổi, và một phần APACHE II, BMI của 4 ca này trong bảng không trùng với CSV.

---

## 9. Dữ liệu bổ sung chưa có trong CSV

Dữ liệu bổ sung gồm 47 bệnh nhân BV Chợ Rẫy và 46 bệnh nhân BV ĐHYD, với các biến CSV không có. Trong `Data_tong_hop.csv` và `Bo_sung_an_danh.csv` các cột này mang tiền tố `bs_`:

- **Hành chính:** `bs_benh_vien`, `bs_nam_nv`, `bs_tuoi_nv` (năm vào viện − năm sinh, đúng tuổi nhập viện), `bs_gioi_tinh` (`0`: Nam; `1`: Nữ).
- **Chỉ số viêm:** `bs_sii_0`, `bs_siri_0` tính từ tiểu cầu, neutrophil, lymphocyte, monocyte lúc nhập viện. Trung bình 2111,9 và 6,85, cao hơn luận án (1863,2 và 5,1) do có giá trị ngoại lai; cần kiểm tra trước khi báo cáo.
- **Thành phần theo mốc:** tiểu cầu, neutrophil, lymphocyte, monocyte, BUN, creatinine, CRP sau TPE 1 và TPE 2.
- **Thang điểm:** thành phần SIRS, Ranson (nhập viện và 48 giờ), Glasgow-Imrie, PASS, HAPS, JSS.
- **Sinh hiệu và điều trị:** SpO₂, sốc, opioid, TG xuất viện, chuyển tuyến, toan ceton, thở máy, thở máy trước TPE, CRRT, thời gian thở máy và CRRT.
- **Hình ảnh:** kết quả siêu âm và CT chi tiết.

Mã hóa: `1`: Có; `2`: Không (khác với mã `0`/`1` của CSV), trừ `bs_gioi_tinh`. Ở các cột `Suy tạng` của PASS: `1`: Tim mạch; `2`: Thận; `3`: Hô hấp; `0`: Không; số ghép như `13` nghĩa là nhiều cơ quan.

**Cách ghép:**

- Hai nguồn dùng số thứ tự khác nhau và không thể ghép bằng mã hồ sơ, vì các cặp ghép theo cách đó có tương quan xấp xỉ 0 ngay cả với năm sinh.
- Bệnh nhân được ghép **theo nội dung lâm sàng**, một-một trên toàn bộ 93 ca, dùng năm sinh, sinh hiệu, Hct, tiểu cầu, bạch cầu, creatinine, BUN, CRP, glucose, PaO₂.
- Một cặp được giữ khi cách biệt rõ với lựa chọn tốt thứ hai (margin ≥ 3), năm sinh lệch ≤ 1 và ba phép kiểm độc lập không dùng khi ghép đều đạt: giới; máy Diapact/Omniselect phải ở BV Chợ Rẫy; `crtt_1 > 0` không được mâu thuẫn với CRRT.
- Kết quả: **60 ca ghép được** (cột `ghep_bo_sung = 1`), gồm 34 ca Chợ Rẫy, 26 ca ĐHYD, 38 ca albumin và 22 ca FFP. 59/60 ca trùng đúng năm sinh.
- Trong 64 cặp đạt margin ≥ 3, chỉ 1 cặp sai giới, nên sai số ước tính khoảng 1–2 cặp. 33 ca còn lại được để trống thay vì ghép ép.

**Giới hạn khi dùng dữ liệu này:**

- **So sánh theo `PP_PEX1` trên biến `bs_*` chỉ dựa trên 60 ca.** Nhóm này có thể không đại diện vì các ca ghép được thường có dữ liệu đầy đủ hơn, và chỉ gồm 2/6 ca tử vong. Cần ghi rõ cỡ mẫu khi báo cáo.
- **Thống kê chung của 93 ca** (ví dụ thở máy 69 ca, toan ceton 39 ca, sốc 19 ca) lấy từ `Bo_sung_an_danh.csv`. Cột `STT_ghep` cho biết `STT` tương ứng nếu đã ghép.
- **125 ô số bị Excel đổi thành ngày tháng** (ví dụ ở BUN, creatinine, WBC, neutrophil, lymphocyte) đã được để trống vì không khôi phục được chắc chắn.
- **Một số ô chữ được giữ nguyên**, ví dụ `huyết thanh đục` khi xét nghiệm không đo được do huyết thanh đục.

---

## 10. Xử lý dữ liệu đề xuất

`Data_tong_hop.csv` đã bỏ `Unnamed: 0`, đã làm sạch `billirubin_tp_0`, `ca_1`, và thêm các cột nhãn chữ `nghe_nghiep_ten`, `machine_1_ten`, `loai_qua_loc_1_ten`, `PP_PEX1_ten`, `balthazar_0_do`. Các giá trị còn lại của CSV được giữ nguyên.

Việc còn lại:

- **Đổi tên** `apa_giam...187` → `apache_giam`; `apa_giam...188` → `tg_giam_lan2`; `apa_giam...189` → `pct_tg_giam_lan2`; `hba0c_0` → `hba1c_0`; `kali_2` → `k_2`; `pao2_fio2` → `pao2/fio2_2`.
- **Chuẩn hóa thời gian** `thoi_gian_nhap_vien`, `onset_pex_0`, `onset_pex_1`, gồm cả số serial Excel và ô thiếu năm.
- **Xác nhận với tác giả trước khi sửa:** `fio2_1` (STT 83), `lactate_0 = 63,32`, `glucose_0 = 18`, `qr_1 = 150`, `billirubin_tp_1 = 55`, `los` = 150 và 240, `can_nang` = 174.
- **Không dùng** `dich_bu` như dịch thực truyền, `tuoi` như tuổi nhập viện, `mof_*` như suy cơ quan, `Atlanta_*` như độ nặng, `tho_may` như tình trạng thở máy.

---

## 11. Thang điểm tiên lượng

Độ chính xác của các mốc dưới đây là số liệu y văn do luận án trích dẫn.

| Thang điểm | Mốc | Tiên lượng VTC nặng | Nhập ICU | Tử vong |
| :--- | :--- | :--- | :--- | :--- |
| APACHE II | ≥ 8 | 65,4% | 60,5% | 59,1% |
| SOFA | ≥ 7 | 89,0% | 97,4% | 98,0% |
| BISAP | ≥ 3 | 86,5% | 91,3% | 91,9% |
| HAPS | ≥ 1 | 50% | 29,9% | 29,9% |

- **BISAP (0–5):** ure > 25 mg/dL; rối loạn tri giác; SIRS ≥ 2; tuổi > 60; tràn dịch màng phổi.
- **SIRS (dương tính khi ≥ 2):** nhiệt độ > 38 °C hoặc < 36 °C; nhịp tim > 90/phút; nhịp thở > 20/phút hoặc PaCO₂ < 32 mmHg; bạch cầu > 12 G/L hoặc < 4 G/L.
- **HAPS (dương tính khi ≥ 1):** viêm phúc mạc; creatinine ≥ 2 mg/dL; Hct > 43% ở nam hoặc > 39,6% ở nữ.
- **CTSI (Balthazar):** điểm viêm (A = 0, B = 1, C = 2, D = 3, E = 4) cộng điểm hoại tử (không = 0, < 30% = 2, 30–50% = 4, > 50% = 6). Phân nhóm: 0–3 nhẹ, 4–6 trung bình, 7–10 nặng.
- **Marshall hiệu chỉnh (suy cơ quan khi ≥ 2 điểm):** PaO₂/FiO₂ ≤ 300; creatinine ≥ 1,9 mg/dL; HATT < 90 mmHg không đáp ứng dịch.
- **Atlanta 2012:** nhẹ: không suy cơ quan, không biến chứng; trung bình-nặng: suy cơ quan thoáng qua ≤ 48 giờ và/hoặc biến chứng; nặng: suy cơ quan kéo dài > 48 giờ.
