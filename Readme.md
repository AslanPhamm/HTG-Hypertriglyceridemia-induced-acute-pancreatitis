# BẢNG ĐỊNH NGHĨA BIẾN SỐ NGHIÊN CỨU

---

## 1. ĐẶC ĐIỂM NHÂN KHẨU HỌC VÀ THỂ TRẠNG

| Tên biến | Loại biến | Đơn vị / Mã hóa | Định nghĩa và Tiêu chuẩn đánh giá |
| :--- | :--- | :--- | :--- |
| **STT** | Định danh | Số nguyên | cỡ mẫu n = 93 |
| **Nam_sinh** | Định lượng | Năm | Năm sinh của bệnh nhân |
| **tuoi** | Định lượng | Năm | Tuổi của bệnh nhân |
| **gioi_tinh** | Nhị giá | `0`: Nam<br>`1`: Nữ | Giới tính của bệnh nhân |
| **nghe_nghiep** | Danh định | Mã hóa số | Nghề nghiệp của bệnh nhân |
| **can_nang** | Định lượng | kg | Cân nặng của bệnh nhân |
| **chieu_cao** | Định lượng | cm | Chiều cao của bệnh nhân |
| **bmi** | Định lượng | kg/m² | BMI = `can_nang / (chieu_cao / 100)²`. |
| **bmig** | Thứ tự | Phân nhóm | - *Gầy*: BMI < 18,5 kg/m²<br>- *Bình thường*: 18,5 ≤ BMI < 24,9 kg/m² <br>- *Thừa cân*: 24,9 ≤ BMI < 29,9 kg/m² <br>- *Béo phì*: BMI ≥ 29,9 kg/m² |

---

## 2. TIỀN CĂN BỆNH LÝ VÀ BỆNH KÈM THEO

| Tên biến | Loại biến | Đơn vị / Mã hóa | Định nghĩa và Tiêu chuẩn đánh giá |
| :--- | :--- | :--- | :--- |
| **dtd** | Nhị giá | `0`: Không<br>`1`: Có | Tiền căn đái tháo đường theo tiêu chuẩn ADA 2020: Đang điều trị hoặc có glucose lúc đói ≥ 126 mg/dL, glucose bất kỳ ≥ 200 mg/dL, nghiệm pháp dung nạp glucose ≥ 200 mg/dL, hoặc HbA1c ≥ 6,5%. |
| **tha** | Nhị giá | `0`: Không<br>`1`: Có | Tiền căn tăng huyết áp: Đang điều trị hạ áp hoặc huyết áp tâm thu ≥ 140 mmHg và/hoặc huyết áp tâm trương ≥ 90 mmHg. |
| **rllm** | Nhị giá | `0`: Không<br>`1`: Có | Tiền căn rối loạn lipid máu (NCEP-ATP III): Đang điều trị hoặc có ≥ 1 tiêu chuẩn: Cholesterol TP > 240 mg/dL (5,2 mmol/L), LDL-C > 160 mg/dL (3,4 mmol/L), HDL-C < 40 mg/dL (1,0 mmol/L), Triglyceride > 200 mg/dL (1,7 mmol/L). |
| **nghien_ruou** | Nhị giá | `0`: Không<br>`1`: Có | Tiền căn nghiện rượu: Có ít nhất 1 trong 3 biểu hiện kéo dài trong 12 tháng: thèm buộc phải uống, không bỏ được, hoặc có hội chứng cai khi ngừng rượu. |
| **tien_su_vtc** | Nhị giá | `0`: Không<br>`1`: Có | Tiền căn từng bị viêm tụy cấp trước đợt nhập viện này. |
| **so_lan_vtc** | Định lượng | Lần | Số lần bệnh nhân từng mắc viêm tụy cấp trong tiền sử. |
| **sd_tranhthai** | Nhị giá | `0`: Không<br>`1`: Có | Tiền sử sử dụng thuốc tránh thai đường uống. |
| **soi_mat** | Nhị giá | `0`: Không<br>`1`: Có | Tiền căn phát hiện sỏi túi mật hoặc sỏi đường mật. |
| **co_thai_1** | Nhị giá | `0`: Không<br>`1`: Có | Tình trạng đang mang thai tại thời điểm bị viêm tụy cấp. |

---

## 3. LÂM SÀNG VÀ SINH HIỆU THỜI ĐIỂM NHẬP VIỆN (HẬU TỐ `_0`)

| Tên biến | Loại biến | Đơn vị / Mã hóa | Định nghĩa và Tiêu chuẩn đánh giá |
| :--- | :--- | :--- | :--- |
| **thoi_gian_nhap_vien** | Thời gian | Giờ, ngày | Thời điểm bệnh nhân nhập viện điều trị. |
| **gio_khoi_phat** | Định lượng | Giờ | Khoảng thời gian tính từ lúc khởi phát cơn đau bụng đầu tiên đến lúc nhập viện. |
| **dau_bung_0** | Nhị giá | `0`: Không<br>`1`: Có | Triệu chứng đau bụng điển hình của VTC: Đau vùng thượng vị khởi phát đột ngột, dữ dội, đau lan sau lưng. |
| **noi_oi_0** | Nhị giá | `0`: Không<br>`1`: Có | Triệu chứng buồn nôn hoặc nôn ói. |
| **sot_0** | Nhị giá | `0`: Không<br>`1`: Có | Triệu chứng sốt lúc nhập viện: Nhiệt độ đo được > 38,3°C. |
| **nhip_tim_0** | Định lượng | Lần/phút | Tần số tim đo được lúc vào viện (mạch nhanh khi > 100 lần/phút). |
| **sys_0** | Định lượng | mmHg | Huyết áp tâm thu lúc nhập viện. |
| **dia_0** | Định lượng | mmHg | Huyết áp tâm trương lúc nhập viện. |
| **map_0** | Định lượng | mmHg | Huyết áp động mạch trung bình: `MAP = dia_0 + (sys_0 - dia_0) / 3`. |
| **nhip_tho_0** | Định lượng | Lần/phút | Tần số thở ban đầu của bệnh nhân. |
| **nhiet_do_0** | Định lượng | °C | Thân nhiệt đo tại thời điểm nhập viện. |
| **glasgow_0** | Định lượng | Điểm | Thang điểm hôn mê Glasgow lúc vào viện (3 – 15 điểm). |
| **dich_bu** | Định lượng | Lít | Tổng thể tích dịch truyền hồi sức ban đầu được chỉ định. |

---

## 4. XÉT NGHIỆM CẬN LÂM SÀNG LÚC NHẬP VIỆN (HẬU TỐ `_0`)

| Tên biến | Loại biến | Đơn vị / Mã hóa | Định nghĩa và Tiêu chuẩn đánh giá |
| :--- | :--- | :--- | :--- |
| **wbc_0** | Định lượng | G/L | Số lượng bạch cầu máu toàn phần (WBC). |
| **rbc_0** | Định lượng | T/L | Số lượng hồng cầu máu (RBC). |
| **hb_0** | Định lượng | g/dL | Nồng độ Hemoglobin trong máu. |
| **hct_0** | Định lượng | % | Thể tích khối hồng cầu Hematocrit (Hct > 44% phản ánh cô đặc máu nặng). |
| **plt_0** | Định lượng | G/L | Số lượng tiểu cầu (PLT). |
| **pt_0** | Định lượng | Giây | Thời gian Prothrombin (đông máu ngoại sinh). |
| **aptt_0** | Định lượng | Giây | Thời gian Thromboplastin một phần hoạt hóa (đông máu nội sinh). |
| **fibrinogen_0** | Định lượng | g/L | Nồng độ Fibrinogen huyết tương. |
| **tg_NV / TG_0** | Định lượng | mg/dL | Nồng độ Triglyceride máu thời điểm nhập viện (tiêu chuẩn chọn mẫu: TG ≥ 1000 mg/dL; quy đổi: mg/dL = mmol/L × 88,5). |
| **amylase_0** | Định lượng | U/L | Nồng độ men Amylase huyết thanh (tăng ≥ 3 lần giới hạn trên giúp chẩn đoán VTC). |
| **lipase_0** | Định lượng | U/L | Nồng độ men Lipase huyết thanh (tăng ≥ 3 lần giới hạn trên giúp chẩn đoán VTC). |
| **glucose_0** | Định lượng | mg/dL | Nồng độ Glucose máu lúc vào viện. |
| **hba0c_0** | Định lượng | % | Tỷ lệ chỉ số glycated hemoglobin (HbA1c). |
| **ceton_0** | Nhị giá | `0`: Âm tính<br>`1`: Dương tính | Thể Ceton trong máu hoặc nước tiểu. |
| **ure_0** | Định lượng | mg/dL | Nồng độ Ure huyết thanh. |
| **creatinin_0** | Định lượng | mg/dL | Nồng độ Creatinine máu (tiêu chuẩn Marshall: Creatinine > 1,9 mg/dL là suy thận cấp). |
| **egfr_0** | Định lượng | mL/min/1,73m² | Mức lọc cầu thận ước tính theo công thức CKD-EPI. |
| **ast_0** | Định lượng | U/L | Men gan AST (Aspartate aminotransferase). |
| **alt_0** | Định lượng | U/L | Men gan ALT (Alanine aminotransferase). |
| **billirubin_tp_0** | Định lượng | µmol/L | Bilirubin toàn phần huyết thanh. |
| **billirubin_tt_0** | Định lượng | µmol/L | Bilirubin trực tiếp huyết thanh. |
| **albumin_0** | Định lượng | g/L | Nồng độ Albumin huyết thanh. |
| **ldh_0** | Định lượng | U/L | Nồng độ Lactate Dehydrogenase huyết thanh. |
| **crp_0** | Định lượng | mg/L (hoặc mg/dL) | Protein C phản ứng (CRP > 150 mg/dL sau 48 giờ là chỉ dấu tiên lượng nặng). |
| **procalcitonin_0**| Định lượng | ng/mL | Dấu ấn sinh học viêm/nhiễm trùng Procalcitonin. |
| **na_0** | Định lượng | mmol/L | Nồng độ Natri máu đã hiệu chỉnh theo mức Triglyceride: `Na_hc = na_do + (tg_NV * 0,002)`. |
| **k_0** | Định lượng | mmol/L | Nồng độ Kali máu. |
| **cl_0** | Định lượng | mmol/L | Nồng độ Clo máu. |
| **ca_0** | Định lượng | mmol/L | Nồng độ Canxi toàn phần huyết thanh. |
| **pH_mau_0** | Định lượng | Không đơn vị | pH máu động mạch. |
| **paco2_0** | Định lượng | mmHg | Phân áp CO₂ trong máu động mạch. |
| **pao2_0** | Định lượng | mmHg | Phân áp O₂ trong máu động mạch. |
| **hco3_0** | Định lượng | mmol/L | Nồng độ Bicarbonate (HCO₃⁻) máu động mạch. |
| **fio2_0** | Định lượng | % hoặc số thập phân | Phân đoạn oxy trong khí thở vào (FiO₂). |
| **pao2/fio2_0** | Định lượng | mmHg | Tỷ lệ PaO₂/FiO₂ lúc nhập viện (< 300 mmHg xác định suy hô hấp theo Marshall). |
| **lactate_0** | Định lượng | mmol/L | Nồng độ Acid Lactic máu. |
| **SII** | Định lượng | Điểm | Chỉ số viêm miễn dịch hệ thống: `SII = (plt * neutrophil) / lymphocyte`. |
| **SIRI** | Định lượng | Điểm | Chỉ số viêm đáp ứng hệ thống: `SIRI = (neutrophil * monocyte) / lymphocyte`. |

---

## 5. THANG ĐIỂM TIÊN LƯỢNG, ĐỘ NẶNG VÀ HÌNH ẢNH HỌC

| Tên biến | Loại biến | Đơn vị / Mã hóa | Định nghĩa và Tiêu chuẩn đánh giá |
| :--- | :--- | :--- | :--- |
| **Atlanta_0** | Thứ tự | `1`: Nhẹ<br>`2`: Trung bình - nặng<br>`3`: Nặng | Phân loại độ nặng theo tiêu chuẩn Atlanta sửa đổi 2012:<br>- *VTC nhẹ*: Không suy cơ quan, không biến chứng tại chỗ/toàn thân.<br>- *VTC trung bình - nặng*: Suy cơ quan thoáng qua (≤ 48 giờ) và/hoặc có biến chứng tại chỗ/toàn thân.<br>- *VTC nặng*: Suy cơ quan kéo dài (> 48 giờ). |
| **apache_ii_0** | Định lượng | Điểm (0 – 71) | Thang điểm APACHE II đánh giá trong 24 giờ đầu (tiêu chuẩn chọn bệnh: APACHE II ≥ 8). |
| **mor_du_doan_0** | Định lượng | % | Tỷ lệ tử vong dự đoán theo mô hình APACHE II. |
| **sofa_0** | Định lượng | Điểm (0 – 24) | Thang điểm đánh giá suy đa cơ quan SOFA (SOFA ≥ 7 có giá trị tiên lượng nặng cao). |
| **bisap_0** | Định lượng | Điểm (0 – 5) | Thang điểm tiên lượng độ nặng BISAP trong 24 giờ đầu (BISAP ≥ 3 là mốc nguy cơ cao):<br>- `b_0`: BUN > 25 mg/dL (1 điểm)<br>- `i_0`: Rối loạn tri giác / Glasgow < 15 (1 điểm)<br>- `s_0`: Hội chứng SIRS ≥ 2 tiêu chuẩn (1 điểm)<br>- `a_0`: Tuổi > 60 (1 điểm)<br>- `p_0`: Tràn dịch màng phổi trên X-quang/CT (1 điểm). |
| **ranson_0** | Định lượng | Điểm (0 – 11) | Thang điểm tiên lượng mức độ nặng Ranson. |
| **ctsi_0 / balthazar_0** | Định lượng | Điểm (0 – 10) | Chỉ số độ nặng trên CT (CTSI) = Điểm viêm theo Balthazar (0–4) + Điểm hoại tử tụy (0–6). Mốc CTSI ≥ 6 phản ánh viêm tụy cấp nặng trên hình ảnh. |
| **mof_phoi_0** | Nhị giá | `0`: Không<br>`1`: Có | Suy hô hấp theo hệ thống Marshall hiệu chỉnh (PaO₂/FiO₂ ≤ 300). |
| **mof_than_0** | Nhị giá | `0`: Không<br>`1`: Có | Suy thận cấp theo Marshall hiệu chỉnh (Creatinine máu > 1,9 mg/dL hay > 170 µmol/L). |
| **mof_tim_0** | Nhị giá | `0`: Không<br>`1`: Có | Suy tuần hoàn/tim mạch theo Marshall hiệu chỉnh (Huyết áp tâm thu < 90 mmHg không đáp ứng bù dịch). |
| **phu_ne_0** | Nhị giá | `0`: Không<br>`1`: Có | Tụ dịch / phù nề mô kẽ tụy phát hiện trên chẩn đoán hình ảnh. |
| **hoai_tu_0** | Nhị giá | `0`: Không<br>`1`: Có | Hoại tử nhu mô tụy và/hoặc mô mỡ quanh tụy trên CT cản quang. |
| **tu_dich_0** | Nhị giá | `0`: Không<br>`1`: Có | Tụ dịch cấp tính quanh tụy trên chẩn đoán hình ảnh. |

---

## 6. THÔNG SỐ VÀ QUY TRÌNH THAY HUYẾT TƯƠNG (PEX / TPE)

| Tên biến | Loại biến | Đơn vị / Mã hóa | Định nghĩa và Tiêu chuẩn đánh giá |
| :--- | :--- | :--- | :--- |
| **so_lan_pex** | Định lượng | Lần | Tổng số lần bệnh nhân được can thiệp thay huyết tương (1 hoặc 2 lần). |
| **onset_pex_0** | Định lượng | Giờ | Khoảng thời gian từ lúc khởi phát đau bụng đến khi bắt đầu tiến hành TPE lần 1. |
| **thoi_gian_loc_1** | Định lượng | Giờ | Thời gian thực hiện cuộc thay huyết tương lần 1 (trung bình 2,8 ± 0,6 giờ). |
| **machine_1** | Danh định | Tên máy | Loại máy lọc máu/thay huyết tương sử dụng (máy Prismaflex hãng Baxter). |
| **loai_qua_loc_1** | Danh định | Tên quả lọc | Loại quả lọc tách huyết tương sử dụng (quả lọc TPE1000). |
| **vi_tri_catheter_1** | Danh định | Vị trí | Vị trí đặt ống thông tĩnh mạch trung tâm hai nòng (Tĩnh mạch bẹn, cảnh trong...). |
| **PP_PEX1, PP_PEX2** | Danh định | `1`: Albumin 5%<br>`2`: FFP | Loại dịch thay thế sử dụng trong cuộc lọc lần 1 và lần 2 (Albumin 5% hoặc Huyết tương tươi đông lạnh). |
| **v_huyet_tuong_1 / v_thay_the_1** | Định lượng | mL | Thể tích huyết tương thay thế tính theo khuyến cáo ASFA: `V = can_nang * 0,07 * (1 - Hct) * (1 đến 1,5)`. |
| **qb_1** | Định lượng | mL/phút | Tốc độ dòng máu rút ra qua catheter (cài đặt 80 – 100 mL/phút). |
| **qr_1** | Định lượng | mL/giờ | Tốc độ dịch thay thế đưa vào (cài đặt 1200 – 1500 mL/giờ). |
| **heparin_bolus_1** | Định lượng | UI | Liều chống đông Heparin tiêm tĩnh mạch ban đầu (20 – 60 UI/kg). |
| **heparin_duy_tri_1** | Định lượng | UI/giờ | Liều chống đông Heparin truyền duy trì trong cuộc lọc (10 UI/kg/giờ). |
| **crtt_1** | Nhị giá | `0`: Không<br>`1`: Có | Bệnh nhân có phối hợp điều trị thay thế thận liên tục (CRRT). |
| **tho_may** | Nhị giá | `0`: Không<br>`1`: Có | Bệnh nhân có can thiệp thở máy xâm lấn trong quá trình điều trị. |

---

## 7. THEO DÕI SAU TPE VÀ BIẾN KẾT CỤC ĐIỀU TRỊ

| Tên biến | Loại biến | Đơn vị / Mã hóa | Định nghĩa và Tiêu chuẩn đánh giá |
| :--- | :--- | :--- | :--- |
| **Hậu tố `_1` và `_2`**<br>*(wbc_1, tg_1, apache_ii_1, sofa_1, tg_2...)* | Định lượng | Tùy biến | Các chỉ số xét nghiệm và thang điểm tiên lượng được đo lại sau lần TPE thứ nhất (1–2 giờ) và sau lần TPE thứ hai để đánh giá hiệu quả phục hồi. |
| **tg_giam** | Định lượng | mg/dL | Lượng Triglyceride giảm tuyệt đối: `ΔTG = TG_trước - TG_sau`. |
| **%tg_giam** | Định lượng | % | Tỷ lệ phần trăm giảm Triglyceride sau can thiệp: `(ΔTG / TG_trước) * 100` (trung bình giảm 77,8%). |
| **bisap_giam / apa_giam...** | Định lượng | Điểm | Mức độ giảm của điểm số BISAP và APACHE II sau điều trị TPE. |
| **los** | Định lượng | Ngày | Thời gian nằm viện điều trị (Length of Stay): Lấy ngày xuất viện trừ ngày nhập viện. |
| **Mor_thuc** | Nhị giá | `0`: Sống<br>`1`: Tử vong | Kết cục điều trị nội viện (`0`: Bệnh nhân hồi phục xuất viện; `1`: Tử vong tại viện hoặc bệnh nặng tiên lượng tử vong xin về; tỷ lệ nghiên cứu là 4,3%). |
| **Mor_du_doan_2** | Định lượng | % | Tỷ lệ tử vong ước tính đánh giá lại sau can thiệp. |

---

# Các thang điểm tiên lượng mức độ nặng viêm tụy cấp
## **Thang điểm APACHE II**
+ Tiên lượng VTC nặng, APACHE II ≥ 8 điểm có độ chính xác là 65,4%.
+ Tiên lượng khả năng nhập khoa Chăm sóc đặc biệt, APACHE II ≥ 8 điểm có độ chính xác là 60,5%.
+ Tiên lượng nguy cơ tử vong, APACHE II ≥ 8 điểm có độ chính xác là 59,1%.
## **Thang điểm SOFA (Sequential Organ Failure Assessment)**
+ Tiên lượng VTC nặng, SOFA ≥ 7 điểm có độ chính xác là 89,0 %.
+ Tiên lượng khả năng cần nhập khoa Chăm sóc đặc biệt, SOFA ≥ 7 điểm có độ chính xác là 97,4%.
+ Tiên lượng nguy cơ tử vong, SOFA ≥ 7 điểm có độ chính xác là 98,0%.
## **Thang điểm BISAP (Bedside index of severity in acute pancreatitis)**
+ Tiên lượng VTC nặng, BISAP ≥ 3 điểm có độ chính xác là 86,5%.
+ Tiên lượng khả năng cần nhập khoa Chăm sóc đặc biệt, BISAP ≥ 3 điểm có độ chính xác là 91,3%.
+ Tiên lượng tử vong, BISAP ≥ 3 điểm có độ chính xác là 91,9%.
## **Thang điểm Balthazar (CTSI: Computed tomography severity index)**
- 0-3 điểm: VTC nhẹ, không có biến chứng nặng
- 4-6 điểm: VTC mức độ trung bình, biến chứng không rõ
- 7-10 điểm: VTC nặng, tử vong cao
## **Thang điểm SIRS (Systemic Inflammatory Response Syndrome)**
Đáp ứng viêm quá mức trong VTC dẫn đến tổn thương cơ quan và suy đa cơ quan (MODS), đây được xem là là nguyên nhân chính gây tử vong ở BN VTC. SIRS được đánh giá dựa trên 4 thông số tại thời điểm nhập viện. SIRS (+) khi có ≥ 2 thông số. Trong nghiên cứu của Düzenci (2021), tiến cứu 153 BN VTC cho thấy SIRS có liên quan với suy cơ quan, suy đa cơ quan và tỉ lệ tử vong ở BN VTC (p<0,05).
## **Thang điểm HAPS (Harmless Acute Pancreatitis Score )**
+ Tiên lượng VTC nặng, HAPS ≥1 điểm có độ chính xác là 50%.
+ Tiên lượng khả năng cần nhập khoa Chăm sóc đặc biệt, HAPS ≥1 điểm có độ chính xác là 29,9%.
+ Tiên lượng tử vong, HAPS ≥1 điểm có độ chính xác là 29,9%.