# -*- coding: utf-8 -*-
"""
Sinh toan bo bieu do cho poster hoi nghi Xac suat - Thong ke.
Nguon so lieu: ../Data/Data_tong_hop.csv (93 ca). Moi con so trong hinh duoc tinh lai
tu du lieu goc, khop voi Ket_qua.md / Data_analyzed.ipynb.

Chay:  python make_figures.py          -> figs_vn/ va figs_en/
"""
import os, sys, warnings
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

warnings.filterwarnings("ignore")
rng = np.random.default_rng(20261102)

HERE = os.path.dirname(os.path.abspath(__file__))
CSV  = os.path.join(HERE, "..", "Data", "Data_tong_hop.csv")

# ----------------------------------------------------------------------------
# Palette da duoc validate (OKLab CVD Delta E >= 8 cho cac cap ke nhau)
# ----------------------------------------------------------------------------
C = dict(blue="#2a78d6", orange="#eb6834", aqua="#1baf7a", yellow="#eda100",
         magenta="#e87ba4", green="#008300", violet="#4a3aa7", red="#e34948")
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8c8b85"
GRID, SURF = "#e4e3df", "#ffffff"
ALB, FFP = C["blue"], C["orange"]           # dinh danh nhom dich thay the
PRE, POST = C["violet"], C["aqua"]          # truoc / sau TPE
SEV, MOD = C["red"], C["blue"]              # nang / trung binh-nang
SIG, NS  = C["red"], INK3                   # co y nghia / khong

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 12.5, "axes.titleweight": "bold", "axes.labelsize": 11,
    "axes.edgecolor": INK3, "axes.linewidth": 0.8, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 10,
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7,
    "axes.axisbelow": True, "legend.frameon": False,
    "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06,
})

def tidy(ax, xgrid=False, ygrid=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK3)
    ax.xaxis.grid(xgrid); ax.yaxis.grid(ygrid)
    return ax

# ----------------------------------------------------------------------------
# Thong ke
# ----------------------------------------------------------------------------
def lilliefors_p(x, nsim=5000):
    """KS hieu chinh Lilliefors (p mo phong) - muc 2.8 cua luan an."""
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    n = len(x)
    def D(v):
        v = np.sort((v - v.mean()) / v.std(ddof=1))
        i = np.arange(1, len(v) + 1)
        cdf = stats.norm.cdf(v)
        return max(np.max(i / len(v) - cdf), np.max(cdf - (i - 1) / len(v)))
    d0 = D(x)
    sim = np.array([D(rng.standard_normal(n)) for _ in range(nsim)])
    return d0, (np.sum(sim >= d0) + 1) / (nsim + 1)

def or_wald(a, b, c, d):
    """a=phoi nhiem&benh, b=phoi nhiem&khong, c=khong&benh, d=khong&khong"""
    a, b, c, d = [v + 0.0 for v in (a, b, c, d)]
    if min(a, b, c, d) == 0:
        a, b, c, d = a + .5, b + .5, c + .5, d + .5
    orr = (a * d) / (b * c)
    se = np.sqrt(1/a + 1/b + 1/c + 1/d)
    return orr, orr * np.exp(-1.96 * se), orr * np.exp(1.96 * se)

def fisher_or_chi2(tab):
    """Chon chi2 khong hieu chinh / Fisher theo tan so mong doi < 5."""
    tab = np.asarray(tab, float)
    chi2, p_chi, _, exp = stats.chi2_contingency(tab, correction=False)
    if exp.min() < 5:
        return stats.fisher_exact(tab)[1], "Fisher"
    return p_chi, "chi2"

def logit_fit(X, y, maxit=200):
    b = np.zeros(X.shape[1])
    for _ in range(maxit):
        p = 1 / (1 + np.exp(-X @ b)); W = np.clip(p * (1 - p), 1e-12, None)
        H = X.T @ (X * W[:, None]); g = X.T @ (y - p)
        step = np.linalg.solve(H + 1e-10 * np.eye(len(b)), g)
        b = b + step
        if np.max(np.abs(step)) < 1e-10: break
    p = 1 / (1 + np.exp(-X @ b)); W = np.clip(p * (1 - p), 1e-12, None)
    cov = np.linalg.inv(X.T @ (X * W[:, None])); se = np.sqrt(np.diag(cov))
    ll = np.sum(y * np.log(np.clip(p, 1e-12, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-12, 1)))
    p0 = y.mean(); n = len(y)
    ll0 = np.sum(y * np.log(p0) + (1 - y) * np.log(1 - p0))
    nag = (1 - np.exp((ll0 - ll) * 2 / n)) / (1 - np.exp(2 * ll0 / n))
    pv = 2 * (1 - stats.norm.cdf(np.abs(b / se)))
    return b, se, pv, nag

def ols(X, y):
    XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y
    r = y - X @ b; n, k = X.shape
    s2 = r @ r / (n - k); se = np.sqrt(np.diag(XtXi) * s2)
    pv = 2 * (1 - stats.t.cdf(np.abs(b / se), n - k))
    r2 = 1 - (r @ r) / np.sum((y - y.mean()) ** 2)
    tq = stats.t.ppf(0.975, n - k)
    return b, se, pv, r2, tq

def pfmt(p, tex=False):
    if p is None or (isinstance(p, float) and np.isnan(p)): return "–"
    if p < 0.001: return "p < 0,001" if not tex else "p<0.001"
    return ("p = %.3f" % p).replace(".", ",") if not tex else "p=%.3f" % p

def num(v, nd=1, vn=True):
    s = f"{v:,.{nd}f}".replace(",", " ")
    return s.replace(".", ",") if vn else s

# ----------------------------------------------------------------------------
# Du lieu
# ----------------------------------------------------------------------------
d = pd.read_csv(CSV)
d["sev"]  = (d.Atlanta_0 == 3).astype(int)              # nang (n=15)
d["fluid"] = d.PP_PEX1_ten                               # Albumin 5% / FFP
d["pct1"] = (1 - d.tg_1 / d.tg_NV) * 100                 # % giam TG sau TPE 1
d["tg_last"] = np.where(d.so_lan_pex == 2, d.tg_2, d.tg_1)
d["pct_all"] = (1 - d.tg_last / d.tg_NV) * 100
alb = d[d.fluid == "Albumin 5%"].copy(); ffp = d[d.fluid == "FFP"].copy()
N, NA, NF = len(d), len(alb), len(ffp)

NORM_VARS = ["tuoi", "bmi", "apache_ii_0", "sofa_0", "bisap_0", "tg_NV", "wbc_0",
             "hct_0", "plt_0", "creatinin_0", "glucose_0", "los", "qb_1", "qr_1",
             "v_thay_the_1", "heparin_bolus_1", "thoi_gian_loc_1", "ure_0"]
_NORM_CACHE = {}
def norm_counts():
    if not _NORM_CACHE:
        k = 0
        for v in NORM_VARS:
            if lilliefors_p(d[v].dropna().values, 4000)[1] > .05: k += 1
        _NORM_CACHE["n_norm"] = k
        _NORM_CACHE["n_tot"] = len(NORM_VARS)
    return _NORM_CACHE["n_norm"], _NORM_CACHE["n_tot"]

# ============================================================================
L = {}   # nhan ngon ngu
L["vn"] = dict(
    f1t="12/18 biến định lượng không chuẩn → dùng phép kiểm phi tham số",
    f1a="Triglyceride nhập viện (mg/dL)", f1b="Điểm APACHE II nhập viện",
    f1c="Phân vị lý thuyết (chuẩn)", f1d="Phân vị quan sát của TG",
    f1y="Số bệnh nhân", f1n="Lệch phải mạnh → phép kiểm phi tham số",
    f1n2="Xấp xỉ chuẩn → t-test", f1qq="Q–Q plot: TG lệch chuẩn rõ",
    f2t="Theo độ nặng: chỉ BISAP ≥ 3 và SOFA ≥ 7 khác biệt có ý nghĩa", f2x="Tỉ lệ bệnh nhân (%)",
    f2l1="Nặng (n = 15)", f2l2="Trung bình–nặng (n = 78)",
    f3t="Đơn biến: chỉ 3/12 yếu tố nhập viện có ý nghĩa",
    f3x="Tỉ số odds (thang log)", f3n="Đỏ: KTC 95% không chứa 1",
    f4t="Đa biến: sau hiệu chỉnh chỉ còn BISAP ≥ 3 có ý nghĩa (R² = 0,19)",
    f4x="OR hiệu chỉnh (thang log)",
    f4m1="Mô hình A: 6 biến, n = 93, 15 biến cố",
    f4m2="Mô hình B: 7 biến, n = 58, 9 biến cố",
    f5t="TPE giảm triglyceride 77,8% (p < 0,001); hai dịch không khác biệt",
    f5y="Triglyceride (mg/dL, thang log)", f5x1="Trước TPE", f5x2="Sau TPE",
    f6t="Cả ba thang điểm đều cải thiện sau TPE (p < 0,001)",
    f6x="Điểm trung bình", f7t="Không khác biệt tỉ lệ giảm TG ở cả ba mốc (mọi KTC chứa 0)",
    f7y="Tỉ lệ giảm TG sau TPE lần 1 (%)",
    f7b="Hiệu số FFP − albumin và KTC 95%",
    f8t="Sau hiệu chỉnh gây nhiễu: không còn khác biệt (mọi KTC chứa 1)",
    f8x="Tỉ số TG còn lại  FFP / albumin", f8r="R² mô hình",
    f9t="Không một chỉ số hiệu quả giảm TG nào đạt p < 0,05",
    f9a="Giá trị p của 30 kiểm định so sánh albumin – FFP",
    f9x="Thứ hạng kiểm định", f9y="Giá trị p",
    f9b="Tỉ lệ giảm triglyceride (%) theo từng kịch bản",
    f0t="Quy trình phân tích thống kê",
)
L["en"] = dict(
    f1t="12 of 18 quantitative variables non-normal → non-parametric tests",
    f1a="Admission triglyceride (mg/dL)", f1b="Admission APACHE II score",
    f1c="Theoretical normal quantiles", f1d="Observed TG quantiles",
    f1y="Number of patients", f1n="Strong right skew → non-parametric tests",
    f1n2="Approximately normal → t-test", f1qq="Q–Q plot: clear departure",
    f2t="By severity: only BISAP ≥ 3 and SOFA ≥ 7 differ significantly", f2x="Patients (%)",
    f2l1="Severe (n = 15)", f2l2="Moderately severe (n = 78)",
    f3t="Univariate: only 3 of 12 admission factors are significant",
    f3x="Odds ratio (log scale)", f3n="Red: 95% CI excludes 1",
    f4t="Multivariable: only BISAP ≥ 3 stays significant (R² = 0.19)",
    f4x="Adjusted OR (log scale)",
    f4m1="Model A: 6 covariates, n = 93, 15 events",
    f4m2="Model B: 7 covariates, n = 58, 9 events",
    f5t="TPE lowers triglyceride by 77.8% (p < 0.001); fluids do not differ",
    f5y="Triglyceride (mg/dL, log scale)", f5x1="Pre-TPE", f5x2="Post-TPE",
    f6t="All three severity scores improve after TPE (p < 0.001)",
    f6x="Mean score", f7t="No difference in TG reduction at any time point (all CIs span 0)",
    f7y="TG reduction after first TPE (%)",
    f7b="FFP − albumin difference with 95% CI",
    f8t="After confounder adjustment: no difference (all CIs contain 1)",
    f8x="Residual TG ratio  FFP / albumin", f8r="Model R²",
    f9t="No triglyceride-efficacy endpoint reaches p < 0.05",
    f9a="p-values of 30 albumin-vs-FFP comparisons",
    f9x="Test rank", f9y="p-value",
    f9b="Triglyceride reduction (%) per scenario",
    f0t="Statistical analysis pipeline",
)

def dec(s, lang):
    """Dau thap phan theo ngon ngu."""
    return s.replace(".", ",") if lang == "vn" else s

# ============================================================================
def fig1(lang, out):
    t = L[lang]; vn = lang == "vn"
    n_norm, n_tot = norm_counts()
    fig, ax = plt.subplots(1, 3, figsize=(14.6, 3.5))
    fig.subplots_adjust(wspace=.30)
    # (a) TG - lech phai manh
    a = ax[0]
    a.hist(d.tg_NV, bins=18, color=C["aqua"], edgecolor=SURF, linewidth=1.1, alpha=.95)
    kx = np.linspace(d.tg_NV.min(), d.tg_NV.max(), 200)
    a.plot(kx, stats.gaussian_kde(d.tg_NV)(kx) * len(d) * (d.tg_NV.max()-d.tg_NV.min())/18,
           color=C["violet"], lw=2.2)
    a.axvline(d.tg_NV.mean(), color=C["orange"], lw=2.2, ls="--")
    a.axvline(d.tg_NV.median(), color=C["blue"], lw=2.2, ls=":")
    a.set_xlabel(t["f1a"] + (" — nghìn" if vn else " — thousands"))
    a.set_ylabel(t["f1y"]); tidy(a)
    a.set_xticks([2000, 6000, 10000, 14000]); a.set_xticklabels(["2", "6", "10", "14"])
    a.set_title("(a) " + ("Lệch phải mạnh" if vn else "Strong right skew"), color="#157f59")
    a.text(.96, .95, (("TB = %s   Trung vị = %s\nKS–Lilliefors: p < 0,001") if vn else
                      ("Mean = %s   Median = %s\nKS–Lilliefors: p < 0.001"))
           % (num(d.tg_NV.mean(), 0, vn), num(d.tg_NV.median(), 0, vn)),
           transform=a.transAxes, ha="right", va="top", fontsize=9.6, color=INK2,
           bbox=dict(fc="#f7f7f5", ec=GRID, boxstyle="round,pad=0.35"))
    a.text(.5, -.38, "→ Wilcoxon rank-sum" if vn else "→ Wilcoxon rank-sum",
           transform=a.transAxes, ha="center", fontsize=11, color=C["violet"],
           fontweight="bold")
    # (b) Tuoi - xap xi chuan
    _, p1 = lilliefors_p(d.tuoi, 4000)
    b = ax[1]
    b.hist(d.tuoi, bins=14, color=C["yellow"], edgecolor=SURF, linewidth=1.1)
    kx = np.linspace(d.tuoi.min(), d.tuoi.max(), 200)
    b.plot(kx, stats.norm.pdf(kx, d.tuoi.mean(), d.tuoi.std(ddof=1))
           * len(d) * (d.tuoi.max()-d.tuoi.min())/14, color=C["violet"], lw=2.2)
    b.axvline(d.tuoi.mean(), color=C["orange"], lw=2.2, ls="--")
    b.axvline(d.tuoi.median(), color=C["blue"], lw=2.2, ls=":")
    b.set_xlabel("Tuổi (năm)" if vn else "Age (years)"); b.set_ylabel(t["f1y"]); tidy(b)
    b.set_title("(b) " + ("Xấp xỉ chuẩn" if vn else "Near-normal"), color="#a37000")
    b.text(.96, .95, (("TB ± ĐLC = %s ± %s\nKS–Lilliefors: p = %s") if vn else
                      ("Mean ± SD = %s ± %s\nKS–Lilliefors: p = %s"))
           % (num(d.tuoi.mean(), 1, vn), num(d.tuoi.std(ddof=1), 1, vn),
              dec("%.2f" % p1, lang)),
           transform=b.transAxes, ha="right", va="top", fontsize=9.6, color=INK2,
           bbox=dict(fc="#f7f7f5", ec=GRID, boxstyle="round,pad=0.35"))
    b.text(.5, -.38, "→ t-test", transform=b.transAxes, ha="center", fontsize=11,
           color=C["violet"], fontweight="bold")
    # (c) Q-Q plot
    cc = ax[2]
    osm, osr = stats.probplot(d.tg_NV, dist="norm", fit=False)
    cc.scatter(osm, osr/1000, s=26, color=C["magenta"], edgecolor=SURF, linewidth=.8, zorder=3)
    sl, it = np.polyfit(osm, osr/1000, 1)
    cc.plot(osm, sl*osm + it, color=INK2, lw=1.6, ls="--")
    cc.set_xlabel(t["f1c"]); cc.set_ylabel(("TG quan sát (nghìn mg/dL)" if vn else
                                            "Observed TG (thousands)"))
    tidy(cc, xgrid=True)
    cc.set_title("(c) " + ("Q–Q plot của TG" if vn else "Q–Q plot of TG"), color="#c04f7a")
    cc.text(.5, -.38, (("%d/%d biến định lượng không chuẩn") % (n_tot-n_norm, n_tot)) if vn
            else ("%d/%d quantitative variables non-normal" % (n_tot-n_norm, n_tot)),
            transform=cc.transAxes, ha="center", fontsize=11, color=C["violet"],
            fontweight="bold")
    fig.suptitle(t["f1t"], fontsize=14.5, fontweight="bold", y=1.14)
    fig.legend(handles=[Line2D([], [], color=C["orange"], lw=2.2, ls="--",
                               label="Trung bình" if vn else "Mean"),
                        Line2D([], [], color=C["blue"], lw=2.2, ls=":",
                               label="Trung vị" if vn else "Median"),
                        Line2D([], [], color=C["violet"], lw=2.2,
                               label="Mật độ / phân phối chuẩn" if vn else "Density / normal")],
               loc="upper center", bbox_to_anchor=(.5, 1.07), ncol=3, fontsize=10.5)
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def fig2(lang, out):
    t = L[lang]; vn = lang == "vn"
    rows = [
        ("BISAP ≥ 3",            (d.bisap_0 >= 3)),
        ("SOFA ≥ 7",             (d.sofa_0 >= 7)),
        ("Urê > 20 mg/dL" if vn else "Urea > 20 mg/dL", (d.ure_0 > 20)),
        ("CTSI ≥ 6",             (d.ctsi_0 >= 6)),
        ("SIRS ≥ 2",             (d.s_0 >= 1)),
        ("Hct > 44%",            (d.hct_0 > 44)),
        ("Creatinin > 1,9" if vn else "Creatinine > 1.9", (d.creatinin_0 > 1.9)),
        ("Giới nam" if vn else "Male sex", (d.gioi_tinh == 0)),
        ("TG ≥ 2000 mg/dL",      (d.tg_NV >= 2000)),
        ("BMI ≥ 25",             (d.bmi >= 25)),
    ]
    labs, ps, pm, pvals = [], [], [], []
    s = d.sev == 1
    for nm, m in rows:
        a, b = int((m & s).sum()), int((m & ~s).sum())
        c, dd = int((~m & s).sum()), int((~m & ~s).sum())
        p, _ = fisher_or_chi2([[a, b], [c, dd]])
        labs.append(nm); ps.append(a/s.sum()*100); pm.append(b/(~s).sum()*100); pvals.append(p)
    o = np.argsort(np.array(ps) - np.array(pm))
    labs = [labs[i] for i in o]; ps = np.array(ps)[o]; pm = np.array(pm)[o]
    pvals = np.array(pvals)[o]
    y = np.arange(len(labs)); h = .38
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    ax.barh(y + h/2, ps, h, color=SEV, edgecolor=SURF, linewidth=1.2, label=t["f2l1"])
    ax.barh(y - h/2, pm, h, color=MOD, edgecolor=SURF, linewidth=1.2, label=t["f2l2"])
    for i in range(len(labs)):
        ax.text(ps[i]+1.8, y[i]+h/2, dec("%.1f" % ps[i], lang), va="center", fontsize=9.6,
                color=SEV, fontweight="bold")
        ax.text(pm[i]+1.8, y[i]-h/2, dec("%.1f" % pm[i], lang), va="center", fontsize=9.6,
                color=MOD)
        star = pvals[i] < .05
        ax.text(123, y[i], dec("p = %.3f" % pvals[i], lang), va="center", ha="right",
                fontsize=9.6, fontweight="bold" if star else "normal",
                color=SIG if star else INK3)
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=10.8)
    ax.set_xlabel(t["f2x"]); ax.set_xlim(0, 123); ax.set_xticks([0, 20, 40, 60, 80, 100])
    tidy(ax, xgrid=True, ygrid=False)
    ax.set_title(t["f2t"], loc="left")
    ax.legend(loc="lower right", bbox_to_anchor=(1.02, -.19), ncol=2, fontsize=10.2)
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
UNI = None
def fig3(lang, out):
    global UNI
    t = L[lang]; vn = lang == "vn"
    rows = [
        ("BISAP ≥ 3",  (d.bisap_0 >= 3)),
        ("SOFA ≥ 7",   (d.sofa_0 >= 7)),
        ("Urê > 20 mg/dL" if vn else "Urea > 20 mg/dL", (d.ure_0 > 20)),
        ("CTSI ≥ 6",   (d.ctsi_0 >= 6)),
        ("SIRS ≥ 2",   (d.s_0 >= 1)),
        ("Hct > 44%",  (d.hct_0 > 44)),
        ("Creatinin > 1,9 mg/dL" if vn else "Creatinine > 1.9 mg/dL", (d.creatinin_0 > 1.9)),
        ("Giới nam" if vn else "Male sex", (d.gioi_tinh == 0)),
        ("Tiền căn VTC" if vn else "Prior AP", (d.tien_su_vtc == 1)),
        ("Đái tháo đường" if vn else "Diabetes", (d.dtd == 1)),
        ("TG ≥ 2000 mg/dL", (d.tg_NV >= 2000)),
        ("BMI ≥ 25",   (d.bmi >= 25)),
    ]
    res = []
    s = d.sev == 1
    for nm, m in rows:
        a, b = int((m & s).sum()), int((m & ~s).sum())
        c, dd = int((~m & s).sum()), int((~m & ~s).sum())
        o, lo, hi = or_wald(a, b, c, dd)
        p, test = fisher_or_chi2([[a, b], [c, dd]])
        res.append((nm, o, lo, hi, p, test))
    UNI = res
    res = sorted(res, key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(11.0, 4.3))
    fig.subplots_adjust(right=.66)
    y = np.arange(len(res))
    for i, (nm, o, lo, hi, p, test) in enumerate(res):
        col = SIG if (lo > 1 or hi < 1) else NS
        ax.plot([lo, hi], [y[i], y[i]], color=col, lw=2.6, solid_capstyle="round", zorder=2)
        for e in (lo, hi):
            ax.plot([e, e], [y[i]-.16, y[i]+.16], color=col, lw=2.0)
        ax.scatter([o], [y[i]], s=95, color=col, edgecolor=SURF, linewidth=1.6,
                   zorder=4, marker="s")
        ax.text(1.04, y[i], dec("%.2f (%.2f–%.2f)" % (o, lo, hi), lang),
                transform=ax.get_yaxis_transform(), fontsize=9.6, va="center", color=INK2)
        ax.text(1.44, y[i], dec("%.3f" % p, lang), transform=ax.get_yaxis_transform(),
                fontsize=9.6, va="center", color=SIG if p < .05 else INK3,
                fontweight="bold" if p < .05 else "normal")
    ax.axvline(1, color=INK2, lw=1.4, ls="--", zorder=1)
    ax.set_xscale("log"); ax.set_xlim(0.08, 45)
    ax.set_xticks([0.1, 0.25, 0.5, 1, 2, 5, 10, 25])
    ax.set_xticklabels(["0,1", "0,25", "0,5", "1", "2", "5", "10", "25"] if vn else
                       ["0.1", "0.25", "0.5", "1", "2", "5", "10", "25"])
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in res], fontsize=10.8)
    ax.set_xlabel(t["f3x"]); tidy(ax, xgrid=True, ygrid=False)
    ax.set_title(t["f3t"], loc="left")
    ax.text(1.04, len(res)-.32, "OR (KTC 95%)" if vn else "OR (95% CI)",
            transform=ax.get_yaxis_transform(), fontsize=9.8, fontweight="bold", color=INK)
    ax.text(1.44, len(res)-.32, "p", transform=ax.get_yaxis_transform(),
            fontsize=9.8, fontweight="bold", color=INK)
    ax.text(0, -.135, t["f3n"], transform=ax.transAxes, fontsize=9.8, color=SIG)
    ax.text(1.62, -.135, ("χ² không hiệu chỉnh / Fisher khi kỳ vọng < 5"
                          if vn else "Uncorrected χ² / Fisher when expected < 5"),
            transform=ax.transAxes, fontsize=9.8, color=INK3, ha="right")
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
MULTI = None
def fig4(lang, out):
    global MULTI
    t = L[lang]; vn = lang == "vn"
    nmv = (["Tuổi (mỗi năm)", "Creatinin > 1,9 mg/dL", "BISAP ≥ 3", "SIRS ≥ 2",
            "Glucose (mỗi mg/dL)", "Bạch cầu > 16 G/L", "SIRI (mỗi đơn vị)"] if vn else
           ["Age (per year)", "Creatinine > 1.9 mg/dL", "BISAP ≥ 3", "SIRS ≥ 2",
            "Glucose (per mg/dL)", "WBC > 16 G/L", "SIRI (per unit)"])
    y = (d.sev == 1).astype(float).values
    base = [d.tuoi.values, (d.creatinin_0 > 1.9).astype(float).values,
            (d.bisap_0 >= 3).astype(float).values, (d.s_0 >= 1).astype(float).values,
            d.glucose_0.values, (d.wbc_0 > 16).astype(float).values]
    XA = np.column_stack([np.ones(N)] + base)
    bA, seA, pA, nagA = logit_fit(XA, y)
    m = d.bs_siri_0.notna().values
    XB = np.column_stack([np.ones(m.sum())] + [v[m] for v in base] + [d.bs_siri_0.values[m]])
    bB, seB, pB, nagB = logit_fit(XB, y[m])
    MULTI = dict(A=(bA, seA, pA, nagA, int(y.sum()), N),
                 B=(bB, seB, pB, nagB, int(y[m].sum()), int(m.sum())))
    fig, ax = plt.subplots(figsize=(10.4, 3.9))
    k = 7; yy = np.arange(k)[::-1]; off = .20
    for i in range(k):
        for b, se, pv, col, sh in ((bA, seA, pA, C["blue"], +off),
                                   (bB, seB, pB, C["orange"], -off)):
            if i >= len(b) - 1: continue
            j = i + 1
            o = np.exp(b[j]); lo = np.exp(b[j]-1.96*se[j]); hi = np.exp(b[j]+1.96*se[j])
            lo, hi = max(lo, .025), min(hi, 350)
            sig = (lo > 1 or hi < 1)
            ax.plot([lo, hi], [yy[i]+sh]*2, color=col, lw=2.5,
                    alpha=1.0 if sig else .60, solid_capstyle="round", zorder=2)
            ax.scatter([o], [yy[i]+sh], s=92 if sig else 62, color=col, edgecolor=SURF,
                       linewidth=1.5, zorder=4, marker="D" if sig else "o",
                       alpha=1.0 if sig else .72)
            if sig:
                ax.text(o*1.25, yy[i]+sh+.30, dec("OR %.2f  p = %.3f" % (o, pv[j]), lang),
                        ha="center", fontsize=9.6, color=col, fontweight="bold")
    ax.axvline(1, color=INK2, lw=1.4, ls="--", zorder=1)
    ax.set_xscale("log"); ax.set_xlim(.025, 350)
    ax.set_xticks([.1, 1, 10, 100])
    ax.set_xticklabels(["0,1", "1", "10", "100"] if vn else ["0.1", "1", "10", "100"])
    ax.set_yticks(yy); ax.set_yticklabels(nmv, fontsize=10.8)
    ax.set_ylim(-.7, k-.3)
    ax.set_xlabel(t["f4x"]); tidy(ax, xgrid=True, ygrid=False)
    ax.set_title(t["f4t"], loc="left", pad=22)
    ax.text(0, 1.015, (("Biến cố / biến số = 2,5 (A) và 1,3 (B) — dưới ngưỡng 10 "
                        "⇒ KTC rất rộng") if vn else
                       ("Events per variable = 2.5 (A), 1.3 (B) — below 10 "
                        "⇒ very wide CIs")),
            transform=ax.transAxes, fontsize=9.8, color=C["violet"], fontweight="bold")
    ax.legend(handles=[Line2D([], [], color=C["blue"], lw=2.5, marker="D", ms=7,
                              label=t["f4m1"] + dec("  ·  R² = %.2f" % nagA, lang)),
                       Line2D([], [], color=C["orange"], lw=2.5, marker="o", ms=7,
                              label=t["f4m2"] + dec("  ·  R² = %.2f" % nagB, lang))],
              loc="lower left", bbox_to_anchor=(-.02, -.40), ncol=1, fontsize=10)
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def fig5(lang, out):
    t = L[lang]; vn = lang == "vn"
    fig, ax = plt.subplots(1, 2, figsize=(12.2, 4.3),
                           gridspec_kw=dict(width_ratios=[1.75, 1]))
    fig.subplots_adjust(wspace=.33)
    a = ax[0]
    for g, col, xo in ((alb, ALB, -.035), (ffp, FFP, .035)):
        for _, r in g.iterrows():
            a.plot([xo, 1+xo], [r.tg_NV, r.tg_1], color=col, lw=.9, alpha=.30, zorder=2)
        a.scatter(np.full(len(g), xo), g.tg_NV, s=15, color=col, alpha=.5, zorder=3)
        a.scatter(np.full(len(g), 1+xo), g.tg_1, s=15, color=col, alpha=.5, zorder=3)
        a.plot([xo, 1+xo], [g.tg_NV.mean(), g.tg_1.mean()], color=col, lw=4.2, zorder=5,
               solid_capstyle="round")
        a.scatter([xo, 1+xo], [g.tg_NV.mean(), g.tg_1.mean()], s=130, color=col,
                  edgecolor=SURF, linewidth=2, zorder=6)
    a.set_yscale("log"); a.set_xlim(-.32, 1.75)
    a.set_yticks([200, 500, 1000, 2000, 5000, 10000])
    a.set_yticklabels(["200", "500", "1 000", "2 000", "5 000", "10 000"])
    a.set_xticks([0, 1]); a.set_xticklabels([t["f5x1"], t["f5x2"]], fontsize=11.5)
    a.set_ylabel(t["f5y"]); tidy(a)
    a.axhline(1000, color=C["green"], lw=1.8, ls="--", zorder=1)
    a.text(-.30, 1060, ("Ngưỡng 1000 mg/dL" if vn else "1000 mg/dL threshold"),
           fontsize=9.6, color=C["green"], va="bottom", fontweight="bold")
    a.text(1.10, ffp.tg_NV.mean()*.92,
           (("FFP\n%s → %s mg/dL\n−79,1%%   p < 0,001") if vn else
            ("FFP\n%s → %s mg/dL\n−79.1%%   p < 0.001"))
           % (num(ffp.tg_NV.mean(), 0, vn), num(ffp.tg_1.mean(), 0, vn)),
           fontsize=10, color=FFP, va="top", fontweight="bold")
    a.text(1.10, alb.tg_1.mean()*.92,
           (("Albumin 5%%\n%s → %s mg/dL\n−74,0%%   p < 0,001") if vn else
            ("Albumin 5%%\n%s → %s mg/dL\n−74.0%%   p < 0.001"))
           % (num(alb.tg_NV.mean(), 0, vn), num(alb.tg_1.mean(), 0, vn)),
           fontsize=10, color=ALB, va="top", fontweight="bold")
    a.set_title("(a) " + ("Từng bệnh nhân, thang log" if vn else
                          "Per patient, log scale"), loc="left")
    # (b)
    b = ax[1]
    parts = b.violinplot([alb.pct1.values, ffp.pct1.values], positions=[0, 1],
                         widths=.78, showextrema=False)
    for pc, col in zip(parts["bodies"], (ALB, FFP)):
        pc.set_facecolor(col); pc.set_alpha(.24); pc.set_edgecolor(col); pc.set_linewidth(1.6)
    bp = b.boxplot([alb.pct1.values, ffp.pct1.values], positions=[0, 1], widths=.2,
                   patch_artist=True, showfliers=False, zorder=4)
    for pa_, col in zip(bp["boxes"], (ALB, FFP)):
        pa_.set_facecolor(SURF); pa_.set_edgecolor(col); pa_.set_linewidth(1.8)
    for key in ("whiskers", "caps", "medians"):
        for ln in bp[key]: ln.set_color(INK2); ln.set_linewidth(1.5)
    for i, (g, col) in enumerate(((alb, ALB), (ffp, FFP))):
        b.scatter(i + rng.normal(0, .055, len(g)), g.pct1, s=20, color=col, alpha=.6,
                  edgecolor=SURF, linewidth=.5, zorder=5)
        b.scatter([i], [g.pct1.mean()], marker="D", s=85, color=col, edgecolor=SURF,
                  linewidth=1.6, zorder=6)
        b.text(i, 114, dec("%.1f%%" % g.pct1.mean(), lang), ha="center", fontsize=11,
               color=col, fontweight="bold")
    pw = stats.mannwhitneyu(alb.pct1, ffp.pct1)[1]
    b.set_xticks([0, 1]); b.set_xticklabels(["Albumin 5%\n(n = 59)", "FFP\n(n = 34)"],
                                            fontsize=10.8)
    b.set_ylabel(t["f7y"]); b.set_ylim(-5, 126); b.set_yticks([0, 20, 40, 60, 80, 100])
    tidy(b)
    b.plot([0, 0, 1, 1], [100, 104, 104, 100], color=INK2, lw=1.3)
    b.text(.5, 105, dec("Wilcoxon p = %.3f" % pw, lang), ha="center", fontsize=10.2,
           color=INK2, fontweight="bold")
    b.set_title("(b) " + (dec("Không khác biệt (p = %.3f)" % pw, lang) if vn
                          else "No difference (p = %.3f)" % pw), loc="left",
                color=C["violet"])
    fig.suptitle(t["f5t"], fontsize=14, fontweight="bold", y=1.03)
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def fig6(lang, out):
    t = L[lang]; vn = lang == "vn"
    scores = [("APACHE II", "apache_ii_0", "apache_ii_1"),
              ("SOFA", "sofa_0", "sofa_1"), ("BISAP", "bisap_0", "bisap_1")]
    fig, ax = plt.subplots(1, 3, figsize=(10.4, 2.9))
    fig.subplots_adjust(wspace=.42)
    for k, (sc, c0, c1) in enumerate(scores):
        A = ax[k]
        lo_all, hi_all = [], []
        for i, (g, gn, col) in enumerate(((alb, "Albumin 5%", ALB), (ffp, "FFP", FFP))):
            pre, post = g[c0].mean(), g[c1].mean()
            p = stats.wilcoxon(g[c0], g[c1])[1]
            A.plot([pre, post], [i, i], color=col, lw=3.2, zorder=2, solid_capstyle="round")
            A.scatter([pre], [i], s=150, color=PRE, edgecolor=SURF, linewidth=1.8, zorder=4)
            A.scatter([post], [i], s=150, color=POST, edgecolor=SURF, linewidth=1.8, zorder=4)
            A.text(pre, i+.33, dec("%.1f" % pre, lang), ha="center", fontsize=10,
                   color=PRE, fontweight="bold")
            A.text(post, i+.33, dec("%.1f" % post, lang), ha="center", fontsize=10,
                   color=POST, fontweight="bold")
            A.text(.5, i-.40, dec("%s:  Δ %.1f   %s" % (gn, post-pre,
                   "p < 0,001" if p < .001 else "p = %.3f" % p), lang) if vn else
                   "%s:  Δ %.1f   %s" % (gn, post-pre,
                   "p < 0.001" if p < .001 else "p = %.3f" % p),
                   transform=A.get_yaxis_transform(), ha="center", fontsize=9.8,
                   color=col, fontweight="bold")
            lo_all += [pre, post]; hi_all += [pre, post]
        pad = (max(hi_all)-min(lo_all))*.42 + .4
        A.set_xlim(min(lo_all)-pad, max(hi_all)+pad)
        A.set_ylim(-.95, 1.75); A.set_yticks([])
        A.set_xlabel(t["f6x"], fontsize=10)
        tidy(A, xgrid=True, ygrid=False)
        A.spines["left"].set_visible(False)
        A.set_title(sc, loc="center", fontsize=12.5, color=INK)
    fig.suptitle(t["f6t"], fontsize=13.5, fontweight="bold", y=1.26)
    fig.legend(handles=[Line2D([], [], marker="o", ls="", ms=11, color=PRE,
                               label="Trước TPE" if vn else "Pre-TPE"),
                        Line2D([], [], marker="o", ls="", ms=11, color=POST,
                               label="Sau TPE" if vn else "Post-TPE"),
                        Line2D([], [], marker="", ls="", label="Wilcoxon bắt cặp"
                               if vn else "Paired Wilcoxon")],
               loc="upper center", bbox_to_anchor=(.5, 1.17), ncol=3, fontsize=10.5)
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def fig7(lang, out):
    t = L[lang]; vn = lang == "vn"
    sub = d[d.so_lan_pex == 2].copy()
    sub["pp2"] = np.where(sub.PP_PEX2 == 0, "Albumin 5%", "FFP")
    sub["pct2"] = (1 - sub.tg_2 / sub.tg_1) * 100
    items = [(("TPE lần 1\n(n = 59 / 34)" if vn else "First TPE\n(n = 59 / 34)"),
              alb.pct1.values, ffp.pct1.values),
             (("TPE lần 2\n(n = 7 / 6)" if vn else "Second TPE\n(n = 7 / 6)"),
              sub.loc[sub.pp2 == "Albumin 5%", "pct2"].values,
              sub.loc[sub.pp2 == "FFP", "pct2"].values),
             (("Chung\n(n = 59 / 34)" if vn else "Overall\n(n = 59 / 34)"),
              d.loc[d.fluid == "Albumin 5%", "pct_all"].values,
              d.loc[d.fluid == "FFP", "pct_all"].values)]
    fig, ax = plt.subplots(1, 2, figsize=(10.6, 3.6),
                           gridspec_kw=dict(width_ratios=[1.05, 1]))
    fig.subplots_adjust(wspace=.40)
    a = ax[0]; w = .33
    for i, (nm, av, fv) in enumerate(items):
        a.bar(i-w/2-.02, av.mean(), w, color=ALB, edgecolor=SURF, linewidth=1.3,
              yerr=av.std(ddof=1)/np.sqrt(len(av))*1.96, capsize=4,
              error_kw=dict(ecolor=INK2, lw=1.4))
        a.bar(i+w/2+.02, fv.mean(), w, color=FFP, edgecolor=SURF, linewidth=1.3,
              yerr=fv.std(ddof=1)/np.sqrt(len(fv))*1.96, capsize=4,
              error_kw=dict(ecolor=INK2, lw=1.4))
        a.text(i-w/2-.02, av.mean()+5.5, dec("%.1f" % av.mean(), lang), ha="center",
               fontsize=10.5, color=ALB, fontweight="bold")
        a.text(i+w/2+.02, fv.mean()+5.5, dec("%.1f" % fv.mean(), lang), ha="center",
               fontsize=10.5, color=FFP, fontweight="bold")
    a.set_xticks(range(3)); a.set_xticklabels([x[0] for x in items], fontsize=10.2)
    a.set_ylabel(t["f7y"]); a.set_ylim(0, 108); a.set_yticks([0, 20, 40, 60, 80, 100])
    tidy(a)
    a.set_title("(a) " + ("Trung bình và KTC 95%" if vn else "Mean with 95% CI"), loc="left")
    a.legend(handles=[Patch(fc=ALB, label="Albumin 5%"), Patch(fc=FFP, label="FFP")],
             loc="lower center", bbox_to_anchor=(.5, -.42), ncol=2, fontsize=10.2)
    b = ax[1]; diffs = []
    for nm, av, fv in items:
        dm = fv.mean() - av.mean()
        se = np.sqrt(av.var(ddof=1)/len(av) + fv.var(ddof=1)/len(fv))
        tq = stats.t.ppf(.975, len(av)+len(fv)-2)
        p = stats.mannwhitneyu(av, fv)[1] if len(av) > 8 else stats.ttest_ind(av, fv)[1]
        diffs.append((nm.split("\n")[0], dm, dm-tq*se, dm+tq*se, p))
    yy = np.arange(len(diffs))[::-1]
    for i, (nm, dm, lo, hi, p) in enumerate(diffs):
        col = SIG if (lo > 0 or hi < 0) else C["violet"]
        b.plot([lo, hi], [yy[i]]*2, color=col, lw=2.8, solid_capstyle="round", zorder=3)
        for e in (lo, hi):
            b.plot([e, e], [yy[i]-.12, yy[i]+.12], color=col, lw=2)
        b.scatter([dm], [yy[i]], s=105, color=col, marker="D", edgecolor=SURF,
                  linewidth=1.6, zorder=4)
        b.text(dm, yy[i]-.42, (dec("%+.1f  (%.1f đến %.1f)" % (dm, lo, hi), lang) if vn
               else "%+.1f  (%.1f to %.1f)" % (dm, lo, hi)),
               ha="center", fontsize=9.8, color=col, fontweight="bold")
        b.text(.99, yy[i], dec("p = %.3f" % p, lang), transform=b.get_yaxis_transform(),
               fontsize=9.8, va="center", ha="right", color=INK2)
    b.axvline(0, color=INK2, lw=1.5, ls="--")
    b.set_yticks(yy); b.set_yticklabels([x[0] for x in diffs], fontsize=10.8)
    b.set_ylim(-.75, len(diffs)-.35)
    b.set_xlabel(t["f7b"]); b.set_xlim(-20, 26); tidy(b, xgrid=True, ygrid=False)
    b.set_title("(b) " + ("Mọi KTC đều chứa 0" if vn else "Every CI contains 0"),
                loc="left", color=C["violet"])
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def fig8(lang, out):
    t = L[lang]; vn = lang == "vn"
    yv = np.log(d.tg_1.values / d.tg_NV.values)
    ffp_i = (d.fluid == "FFP").astype(float).values
    ltg0 = np.log(d.tg_NV.values)
    vol = (d.v_thay_the_1 / d.v_huyet_tuong_1).values
    mach = pd.get_dummies(d.machine_1, prefix="m", drop_first=True).astype(float).values
    models = [np.column_stack([np.ones(N), ffp_i]),
              np.column_stack([np.ones(N), ffp_i, ltg0, vol]),
              np.column_stack([np.ones(N), ffp_i, ltg0, vol, mach])]
    labs = (["1. Thô (chưa hiệu chỉnh)", "2. + TG ban đầu, lượng dịch thay",
             "3. + loại máy lọc"] if vn else
            ["1. Crude (unadjusted)", "2. + baseline TG, exchange volume",
             "3. + machine type"])
    res = [ols(X, yv) for X in models]
    out_rows = []
    for b, se, pv, r2, tq in res:
        out_rows.append((np.exp(b[1]), np.exp(b[1]-tq*se[1]), np.exp(b[1]+tq*se[1]),
                         pv[1], r2))
    fig, ax = plt.subplots(figsize=(9.4, 3.1))
    fig.subplots_adjust(left=.30, right=.97)
    yy = np.arange(3)[::-1]; cols = [C["magenta"], C["violet"], C["aqua"]]
    for i, (o, lo, hi, p, r2) in enumerate(out_rows):
        col = cols[i]
        ax.plot([lo, hi], [yy[i]]*2, color=col, lw=3.0, solid_capstyle="round", zorder=3)
        for e in (lo, hi):
            ax.plot([e, e], [yy[i]-.13, yy[i]+.13], color=col, lw=2.2)
        ax.scatter([o], [yy[i]], s=115, color=col, marker="D", edgecolor=SURF,
                   linewidth=1.6, zorder=4)
        ax.text(hi+.02, yy[i], dec("%.2f (%.2f–%.2f)   p = %.3f   R² = %.2f"
                % (o, lo, hi, p, r2), lang), fontsize=9.8, va="center", color=INK2)
    ax.axvline(1, color=INK2, lw=1.5, ls="--")
    ax.set_yticks(yy); ax.set_yticklabels(labs, fontsize=10.6)
    ax.set_ylim(-.6, 2.5)
    ax.set_xlabel(t["f8x"]); ax.set_xlim(.52, 1.62); ax.set_xticks([.6, .8, 1.0, 1.2])
    ax.set_xticklabels(["0,6", "0,8", "1,0", "1,2"] if vn else ["0.6", "0.8", "1.0", "1.2"])
    tidy(ax, xgrid=True, ygrid=False)
    ax.set_title(t["f8t"], loc="left", pad=16)
    ax.text(0, -.40, (("Tỉ số < 1: FFP để lại ít TG hơn. KTC 95% chứa 1 ở cả ba mô hình "
                       "⇒ không có khác biệt") if vn else
                      ("Ratio < 1: FFP leaves less TG. All three CIs contain 1 "
                       "⇒ no difference")),
            transform=ax.transAxes, fontsize=10, color=C["violet"], fontweight="bold")
    fig.savefig(out, dpi=300); plt.close(fig)
    return out_rows

# ============================================================================
BASE_KEYS = ["SOFA nhập viện", "SOFA sau TPE", "CRRT", "BISAP sau TPE",
             "APACHE II nhập viện", "Tốc độ thay thế Qr", "BMI",
             "Thể tích dịch thay thế", "Creatinin nhập viện", "APACHE II sau TPE",
             "Heparin bolus", "Heparin duy trì", "Thời gian lọc", "Tốc độ rút máu Qb",
             "TG trước TPE", "Glucose nhập viện", "BISAP ≥ 3", "Số ngày nằm viện",
             "Tiểu cầu nhập viện", "Bạch cầu nhập viện", "Hct nhập viện",
             "BISAP nhập viện", "Độ nặng (Atlanta)", "Tuổi", "Giới nam",
             "Đái tháo đường", "Tử vong"]
EFF_KEYS = ["Tỉ lệ giảm TG lần 1", "Tỉ lệ giảm TG chung", "Mức giảm TG", "TG sau TPE 1",
            "Đạt TG < 1000 sau TPE 1", "Cần TPE lần 2"]
EN_NAME = {"SOFA nhập viện": "SOFA at admission", "SOFA sau TPE": "SOFA after TPE",
           "CRRT": "CRRT", "BISAP sau TPE": "BISAP after TPE",
           "APACHE II nhập viện": "APACHE II at admission",
           "Tốc độ thay thế Qr": "Replacement rate Qr", "BMI": "BMI",
           "Thể tích dịch thay thế": "Exchange volume",
           "Creatinin nhập viện": "Creatinine", "APACHE II sau TPE": "APACHE II after TPE",
           "Tỉ lệ giảm TG lần 1": "TG reduction, 1st TPE",
           "Tỉ lệ giảm TG chung": "TG reduction, overall", "Mức giảm TG": "Absolute TG drop",
           "TG sau TPE 1": "TG after 1st TPE",
           "Đạt TG < 1000 sau TPE 1": "Reaching TG < 1000", "Cần TPE lần 2": "Needing 2nd TPE"}

PV = None
def fig9(lang, out):
    global PV
    t = L[lang]; vn = lang == "vn"
    if PV is None: PV = collect_pvalues()
    pv = np.array([p for _, p, _ in PV]); m = len(pv)
    bh_thr = (np.arange(1, m+1)/m)*.05
    srt = np.sort(pv); below = np.where(srt <= bh_thr)[0]
    nbh = below.max()+1 if len(below) else 0
    nraw = int((pv < .05).sum())
    fig, ax = plt.subplots(figsize=(10.8, 3.15))
    fig.subplots_adjust(left=.26, right=.98, bottom=.26)
    groups = [(("Đặc điểm nền và thông số\nquy trình TPE" if vn else
                "Baseline severity and\nTPE process variables"), BASE_KEYS, C["orange"]),
              (("Hiệu quả giảm\ntriglyceride" if vn else
                "Triglyceride\nefficacy endpoints"), EFF_KEYS, C["blue"])]
    for gi, (gname, keys, col) in enumerate(groups):
        pts = [(nm, p) for nm, p, _ in PV if nm in keys]
        xs = np.array([p for _, p in pts])
        ys = gi + rng.normal(0, .085, len(xs))
        ax.scatter(xs, ys, s=95, color=col, alpha=.85, edgecolor=SURF, linewidth=1.2,
                   zorder=4)
        sig = sorted([(nm, p) for nm, p in pts if p < .05], key=lambda z: z[1])[:5]
        for si, (nm, p) in enumerate(sig):
            lbl = nm if vn else EN_NAME.get(nm, nm)
            dy = [18, 40, 62, 18, 40][si % 5]
            ax.annotate(lbl, (p, gi), textcoords="offset points", xytext=(3, dy),
                        fontsize=9.2, color=col, fontweight="bold", ha="left",
                        arrowprops=dict(arrowstyle="-", color=col, lw=.8,
                                        shrinkA=0, shrinkB=3, alpha=.55))
        ax.text(-.02, gi, "%s\n(%d %s)" % (gname, len(pts),
                "kiểm định" if vn else "tests"),
                transform=ax.get_yaxis_transform(), ha="right", va="center",
                fontsize=10.4, color=col, fontweight="bold", linespacing=1.4)
    ax.axvline(.05, color=SIG, lw=2.0, ls="--", zorder=2)
    ax.text(.052, 1.72, dec("α = 0,05", lang) if vn else "α = 0.05", color=SIG,
            fontsize=10.4, fontweight="bold")
    ax.axvline(.05/m, color=C["violet"], lw=1.8, ls=":", zorder=2)
    ax.text(.05/m, 1.72, dec("Bonferroni %.4f" % (.05/m), lang), color=C["violet"],
            fontsize=9.6, fontweight="bold", ha="left")
    ax.set_xscale("log"); ax.set_xlim(5e-4, 1.6)
    ax.set_xticks([.001, .01, .05, .1, .5, 1])
    ax.set_xticklabels(["0,001", "0,01", "0,05", "0,1", "0,5", "1"] if vn else
                       ["0.001", "0.01", "0.05", "0.1", "0.5", "1"])
    ax.set_yticks([]); ax.set_ylim(-.6, 2.05)
    ax.set_xlabel(("Giá trị p (thang log) — %d kiểm định so sánh albumin 5%% với FFP"
                   % m) if vn else
                  ("p-value (log scale) — %d albumin-vs-FFP comparisons" % m))
    tidy(ax, xgrid=True, ygrid=False); ax.spines["left"].set_visible(False)
    ax.set_title(t["f9t"], loc="left", pad=30)
    ax.text(0, -.42, ((("Cả %d kiểm định có p < 0,05 đều thuộc nhóm đặc điểm nền và quy "
                        "trình; %d còn ý nghĩa sau hiệu chỉnh Benjamini–Hochberg.")
                       % (nraw, nbh)) if vn else
                      (("All %d tests with p < 0.05 are baseline or process variables; "
                        "%d survive Benjamini–Hochberg.") % (nraw, nbh))),
            transform=ax.transAxes, fontsize=10, color=C["violet"], fontweight="bold",
            va="top")
    fig.savefig(out, dpi=300); plt.close(fig)
    return nraw, m, nbh, .05/m

# ============================================================================
def fig10(lang, out):
    t = L[lang]; vn = lang == "vn"
    sc = sensitivity_rows(lang)
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    fig.subplots_adjust(left=.36, right=.88)
    yy = np.arange(len(sc))[::-1]
    for i, (nm, av, fv, p) in enumerate(sc):
        ax.plot([av, fv], [yy[i]]*2, color=GRID, lw=3.0, zorder=1, solid_capstyle="round")
        ax.scatter([av], [yy[i]], s=86, color=ALB, edgecolor=SURF, linewidth=1.2, zorder=4)
        ax.scatter([fv], [yy[i]], s=86, color=FFP, edgecolor=SURF, linewidth=1.2, zorder=4)
        ax.text(1.02, yy[i], dec("p = %.3f" % p, lang),
                transform=ax.get_yaxis_transform(), fontsize=9.8, va="center",
                color=SIG if p < .05 else INK3,
                fontweight="bold" if p < .05 else "normal")
    ax.set_yticks(yy); ax.set_yticklabels([s[0] for s in sc], fontsize=10.0)
    ax.set_xlabel(t["f9b"]); ax.set_xlim(55, 90); tidy(ax, xgrid=True, ygrid=False)
    ax.set_title(("Không kịch bản nào cho p < 0,05 — kết luận vững" if vn else
                  "No scenario yields p < 0.05 — the conclusion is robust"), loc="left")
    ax.legend(handles=[Line2D([], [], marker="o", ls="", ms=10, color=ALB,
                              label="Albumin 5%"),
                       Line2D([], [], marker="o", ls="", ms=10, color=FFP, label="FFP")],
              loc="lower center", bbox_to_anchor=(.5, -.30), ncol=2, fontsize=10.2)
    ax.text(1.02, -.30, ("11 kịch bản tính tỉ lệ giảm TG" if vn else
                         "11 ways of computing TG reduction"),
            transform=ax.transAxes, fontsize=10, color=INK3, ha="right")
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def collect_pvalues():
    """Toan bo kiem dinh so sanh albumin 5% voi FFP."""
    out = []
    quant = [("TG trước TPE", "tg_NV"), ("TG sau TPE 1", "tg_1"),
             ("Mức giảm TG", None), ("Tỉ lệ giảm TG lần 1", "pct1"),
             ("Tỉ lệ giảm TG chung", "pct_all"),
             ("APACHE II nhập viện", "apache_ii_0"), ("SOFA nhập viện", "sofa_0"),
             ("BISAP nhập viện", "bisap_0"), ("APACHE II sau TPE", "apache_ii_1"),
             ("SOFA sau TPE", "sofa_1"), ("BISAP sau TPE", "bisap_1"),
             ("Thể tích dịch thay thế", "v_thay_the_1"),
             ("Tốc độ rút máu Qb", "qb_1"), ("Tốc độ thay thế Qr", "qr_1"),
             ("Thời gian lọc", "thoi_gian_loc_1"), ("Heparin bolus", "heparin_bolus_1"),
             ("Heparin duy trì", "heparin_duy_tri_1"), ("Số ngày nằm viện", "los"),
             ("Tuổi", "tuoi"), ("BMI", "bmi"), ("Bạch cầu nhập viện", "wbc_0"),
             ("Hct nhập viện", "hct_0"), ("Tiểu cầu nhập viện", "plt_0"),
             ("Creatinin nhập viện", "creatinin_0"), ("Glucose nhập viện", "glucose_0")]
    for nm, col in quant:
        if col is None:
            av = (alb.tg_NV - alb.tg_1).values; fv = (ffp.tg_NV - ffp.tg_1).values
        else:
            av = d.loc[d.fluid == "Albumin 5%", col].dropna().values
            fv = d.loc[d.fluid == "FFP", col].dropna().values
        if len(av) < 3 or len(fv) < 3: continue
        pn_a = lilliefors_p(av, 1500)[1]; pn_f = lilliefors_p(fv, 1500)[1]
        if pn_a > .05 and pn_f > .05:
            p = stats.ttest_ind(av, fv, equal_var=True)[1]; test = "t"
        else:
            p = stats.mannwhitneyu(av, fv)[1]; test = "Wilcoxon"
        out.append((nm, p, test))
    cat = [("Giới nam", (d.gioi_tinh == 0)), ("Đái tháo đường", (d.dtd == 1)),
           ("Độ nặng (Atlanta)", (d.sev == 1)), ("BISAP ≥ 3", (d.bisap_0 >= 3)),
           ("CRRT", (d.crtt_1 > 0)), ("Tử vong", (d.Mor_thuc == 1)),
           ("Cần TPE lần 2", (d.so_lan_pex == 2)),
           ("Đạt TG < 1000 sau TPE 1", (d.tg_1 < 1000))]
    for nm, m in cat:
        f = d.fluid == "FFP"
        tab = [[int((m & f).sum()), int((m & ~f).sum())],
               [int((~m & f).sum()), int((~m & ~f).sum())]]
        p, test = fisher_or_chi2(tab)
        out.append((nm, p, test))
    return out

def sensitivity_rows(lang):
    vn = lang == "vn"
    rows = []
    def mw(a, f):
        return stats.mannwhitneyu(a, f)[1] if min(len(a), len(f)) > 8 \
               else stats.ttest_ind(a, f)[1]
    a1, f1 = alb.pct1.values, ffp.pct1.values
    rows.append((("Lần 1 — phân tích gốc" if vn else "1st TPE — primary"),
                 a1.mean(), f1.mean(), mw(a1, f1)))
    av = ((1 - alb.tg_1/alb.TG_0).replace([np.inf, -np.inf], np.nan).dropna()*100).values
    fv = ((1 - ffp.tg_1/ffp.TG_0).replace([np.inf, -np.inf], np.nan).dropna()*100).values
    rows.append((("Lần 1 — dùng TG_0 thay tg_NV" if vn else "1st — using TG_0"),
                 av.mean(), fv.mean(), mw(av, fv)))
    ex = alb[~alb.STT.isin([60, 62])].pct1.values
    rows.append((("Lần 1 — bỏ 2 ca nghi trùng" if vn else "1st — drop 2 duplicates"),
                 ex.mean(), f1.mean(), mw(ex, f1)))
    ex2 = alb[~alb.STT.isin([44, 66])].pct1.values
    rows.append((("Lần 1 — bỏ 2 ca giảm < 10%" if vn else "1st — drop 2 outliers"),
                 ex2.mean(), f1.mean(), mw(ex2, f1)))
    a4 = alb.loc[alb.tg_NV >= 2000, "pct1"].values
    f4 = ffp.loc[ffp.tg_NV >= 2000, "pct1"].values
    rows.append((("Lần 1 — chỉ ca TG ≥ 2000" if vn else "1st — only TG ≥ 2000"),
                 a4.mean(), f4.mean(), mw(a4, f4)))
    sub = d[d.so_lan_pex == 2].copy()
    sub["pp2"] = np.where(sub.PP_PEX2 == 0, "Albumin 5%", "FFP")
    sub["pct2"] = (1 - sub.tg_2/sub.tg_1)*100
    a2 = sub.loc[sub.pp2 == "Albumin 5%", "pct2"].values
    f2 = sub.loc[sub.pp2 == "FFP", "pct2"].values
    rows.append((("Lần 2 — theo dịch dùng ở lần 2" if vn else "2nd — fluid at 2nd session"),
                 a2.mean(), f2.mean(), stats.ttest_ind(a2, f2)[1]))
    a2b = sub.loc[sub.fluid == "Albumin 5%", "pct2"].values
    f2b = sub.loc[sub.fluid == "FFP", "pct2"].values
    rows.append((("Lần 2 — theo dịch lần 1" if vn else "2nd — fluid at 1st session"),
                 a2b.mean(), f2b.mean(), stats.ttest_ind(a2b, f2b)[1]))
    keep = sub[sub.fluid.map({"Albumin 5%": 0, "FFP": 1}) == sub.PP_PEX2]
    a2c = keep.loc[keep.fluid == "Albumin 5%", "pct2"].values
    f2c = keep.loc[keep.fluid == "FFP", "pct2"].values
    rows.append((("Lần 2 — bỏ 3 ca đổi dịch" if vn else "2nd — drop 3 switchers"),
                 a2c.mean(), f2c.mean(), stats.mannwhitneyu(a2c, f2c)[1]))
    a3 = d.loc[d.fluid == "Albumin 5%", "pct_all"].values
    f3 = d.loc[d.fluid == "FFP", "pct_all"].values
    rows.append((("Chung — phân tích gốc" if vn else "Overall — primary"),
                 a3.mean(), f3.mean(), mw(a3, f3)))
    ag = d.loc[d.fluid == "Albumin 5%", "%tg_giam"].dropna().values
    fg = d.loc[d.fluid == "FFP", "%tg_giam"].dropna().values
    if np.nanmax(ag) <= 1.5: ag, fg = ag*100, fg*100
    rows.append((("Chung — theo biến tg_giam" if vn else "Overall — via tg_giam"),
                 ag.mean(), fg.mean(), mw(ag, fg)))
    med_a = np.median(a1); med_f = np.median(f1)
    rows.append((("Lần 1 — dùng trung vị" if vn else "1st — medians"),
                 med_a, med_f, mw(a1, f1)))
    return rows

# ============================================================================
def fig0(lang, out):
    """So do quy trinh phan tich thong ke."""
    t = L[lang]; vn = lang == "vn"
    fig, ax = plt.subplots(figsize=(13.6, 2.35))
    ax.set_xlim(0, 100); ax.set_ylim(0, 24); ax.axis("off")
    steps = ([("93 bệnh nhân VTC\ndo tăng triglyceride",
               "359 biến số\nAlbumin 5%: 59  ·  FFP: 34", C["blue"]),
              ("Kiểm định\nphân phối",
               "KS – Lilliefors\n(mô phỏng 5 000 lần)", C["magenta"]),
              ("So sánh\nhai nhóm độc lập",
               "t-test hoặc\nWilcoxon rank-sum\nχ² / Fisher", C["aqua"]),
              ("Phân tích bắt cặp\ntrước – sau TPE",
               "t bắt cặp hoặc\nWilcoxon signed-rank", C["yellow"]),
              ("Mô hình đa biến",
               "Logistic: OR hiệu chỉnh\nLog-tuyến tính:\nhiệu chỉnh gây nhiễu", C["violet"]),
              ("Kiểm soát sai số",
               "Benjamini–Hochberg\n11 kịch bản độ vững", C["orange"])]
             if vn else
             [("93 HTG-AP patients", "359 variables\nAlbumin 5%: 59  ·  FFP: 34", C["blue"]),
              ("Normality\ntesting", "KS – Lilliefors\n(5 000 simulations)", C["magenta"]),
              ("Two independent\ngroups", "t-test or\nWilcoxon rank-sum\nχ² / Fisher", C["aqua"]),
              ("Paired pre–post\nTPE analysis", "Paired t or\nWilcoxon signed-rank", C["yellow"]),
              ("Multivariable models",
               "Logistic: adjusted OR\nLog-linear:\nconfounder adjustment", C["violet"]),
              ("Error control",
               "Benjamini–Hochberg\n11 sensitivity scenarios", C["orange"])])
    w, gap, x0 = 14.2, 2.4, 1.0
    for i, (head, body, col) in enumerate(steps):
        x = x0 + i*(w+gap)
        ax.add_patch(FancyBboxPatch((x, 1.2), w, 20.6,
                                    boxstyle="round,pad=0.25,rounding_size=1.2",
                                    fc=col, ec="none", alpha=.12, zorder=1))
        ax.add_patch(FancyBboxPatch((x, 15.0), w, 6.8,
                                    boxstyle="round,pad=0.25,rounding_size=1.2",
                                    fc=col, ec="none", zorder=2))
        ax.text(x+w/2, 18.4, head, ha="center", va="center", fontsize=11.2,
                color="white", fontweight="bold", zorder=3, linespacing=1.3)
        ax.text(x+w/2, 8.0, body, ha="center", va="center", fontsize=10.2,
                color=INK2, zorder=3, linespacing=1.55)
        ax.text(x+1.0, 2.9, "%d" % (i+1), ha="center", va="center", fontsize=12,
                color=col, fontweight="bold", zorder=3)
        if i < len(steps)-1:
            ax.add_patch(FancyArrowPatch((x+w+.2, 11.5), (x+w+gap-.2, 11.5),
                                         arrowstyle="-|>", mutation_scale=18,
                                         color=INK3, lw=1.8, zorder=4))
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def fig0_tall(lang, out):
    """So do quy trinh phan tich, bo cuc 3 hang x 2 cot (cho cot hep)."""
    vn = lang == "vn"
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    steps = ([("Dữ liệu nghiên cứu",
               "93 bệnh nhân · 359 biến\nAlbumin 5%: 59 · FFP: 34", C["blue"]),
              ("Kiểm định phân phối",
               "Kolmogorov–Smirnov\nhiệu chỉnh Lilliefors\n(p mô phỏng 5 000 lần)", C["magenta"]),
              ("So sánh hai nhóm độc lập",
               "t-test hoặc Wilcoxon\nrank-sum · χ² / Fisher", C["aqua"]),
              ("Phân tích bắt cặp\ntrước – sau TPE",
               "t bắt cặp hoặc\nWilcoxon signed-rank", C["yellow"]),
              ("Mô hình đa biến",
               "Logistic: OR hiệu chỉnh\nLog-tuyến tính:\nhiệu chỉnh gây nhiễu", C["violet"]),
              ("Kiểm soát sai số",
               "Benjamini–Hochberg\nBonferroni\n11 kịch bản độ vững", C["orange"])]
             if vn else
             [("Study data",
               "93 patients · 359 variables\nAlbumin 5%: 59 · FFP: 34", C["blue"]),
              ("Normality testing",
               "Kolmogorov–Smirnov\nwith Lilliefors correction\n(p simulated 5 000×)", C["magenta"]),
              ("Two independent groups",
               "t-test or Wilcoxon\nrank-sum · χ² / Fisher", C["aqua"]),
              ("Paired pre–post\nTPE analysis",
               "Paired t or\nWilcoxon signed-rank", C["yellow"]),
              ("Multivariable models",
               "Logistic: adjusted OR\nLog-linear: confounder\nadjustment", C["violet"]),
              ("Error control",
               "Benjamini–Hochberg\nBonferroni\n11 sensitivity scenarios", C["orange"])])
    w, h = 45.0, 28.0
    xs = [2.0, 53.0]; ys = [69.0, 36.0, 3.0]
    # bo cuc ran truon: hang 1 trai->phai, hang 2 phai->trai, hang 3 trai->phai
    pos = [(xs[0], ys[0]), (xs[1], ys[0]),
           (xs[1], ys[1]), (xs[0], ys[1]),
           (xs[0], ys[2]), (xs[1], ys[2])]
    for i, ((x, y), (head, body, col)) in enumerate(zip(pos, steps)):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.4,rounding_size=1.6",
                                    fc=col, ec="none", alpha=.12, zorder=1))
        ax.add_patch(FancyBboxPatch((x, y + h - 8.4), w, 8.4,
                                    boxstyle="round,pad=0.4,rounding_size=1.6",
                                    fc=col, ec="none", zorder=2))
        ax.text(x + w/2, y + h - 4.2, head, ha="center", va="center", fontsize=11.0,
                color="white", fontweight="bold", zorder=3, linespacing=1.2)
        ax.text(x + w/2, y + (h - 8.4)/2 - 0.8, body, ha="center", va="center",
                fontsize=9.6, color=INK2, zorder=3, linespacing=1.5)
        ax.text(x + 2.4, y + 2.4, "%d" % (i + 1), ha="center", va="center",
                fontsize=12, color=col, fontweight="bold", zorder=3)
    arr = dict(arrowstyle="-|>", mutation_scale=17, color=INK3, lw=2.0, zorder=4)
    gx = (xs[0] + w + xs[1]) / 2                      # giua khe doc
    ax.add_patch(FancyArrowPatch((xs[0]+w+.8, ys[0]+h/2), (xs[1]-.8, ys[0]+h/2), **arr))
    ax.add_patch(FancyArrowPatch((xs[1]+w/2, ys[0]-.8), (xs[1]+w/2, ys[1]+h+.8), **arr))
    ax.add_patch(FancyArrowPatch((xs[1]-.8, ys[1]+h/2), (xs[0]+w+.8, ys[1]+h/2), **arr))
    ax.add_patch(FancyArrowPatch((xs[0]+w/2, ys[1]-.8), (xs[0]+w/2, ys[2]+h+.8), **arr))
    ax.add_patch(FancyArrowPatch((xs[0]+w+.8, ys[2]+h/2), (xs[1]-.8, ys[2]+h/2), **arr))
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def fig_design(lang, out):
    """So do thiet ke nghien cuu (kieu CONSORT) — thay cho khoi so lieu chu."""
    vn = lang == "vn"
    T = (dict(setting="Hai trung tâm tuyến cuối, TP. Hồ Chí Minh\nbệnh nhân nhập viện 2018 – 2023",
              elig="Tiêu chí chọn bệnh",
              eligb="Viêm tụy cấp  ·  TG nhập viện ≥ 1000 mg/dL\nđược thay huyết tương (TPE)",
              coh="Dân số nghiên cứu",
              cohb="93 bệnh nhân người lớn liên tiếp\n359 biến số được ghi nhận",
              alloc="Dịch thay thế do bác sĩ điều trị chọn\nKHÔNG phân nhóm ngẫu nhiên",
              a="Albumin 5%", an="n = 59", f="FFP", fn="n = 34",
              tpe="Số lần thay huyết tương",
              tpeb="1 lần: n = 80        2 lần: n = 13",
              end="Kết cục đánh giá",
              endb="① Diễn tiến nặng (nhị giá)   ② Tỉ lệ giảm TG\n③ Thay đổi APACHE II · SOFA · BISAP",
              warn="⇒ gây nhiễu do chỉ định")
         if vn else
         dict(setting="Two tertiary referral centres, Ho Chi Minh City\nadmissions 2018 – 2023",
              elig="Eligibility",
              eligb="Acute pancreatitis  ·  admission TG ≥ 1000 mg/dL\ntreated with plasma exchange (TPE)",
              coh="Study cohort",
              cohb="93 consecutive adult patients\n359 variables recorded",
              alloc="Replacement fluid chosen by the treating team\nNOT randomised",
              a="Albumin 5%", an="n = 59", f="FFP", fn="n = 34",
              tpe="Number of TPE sessions",
              tpeb="one: n = 80        two: n = 13",
              end="Endpoints",
              endb="① Progression to severe disease   ② % TG reduction\n③ Change in APACHE II · SOFA · BISAP",
              warn="⇒ confounding by indication"))
    fig, ax = plt.subplots(figsize=(7.0, 5.3))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

    def box(x, y, w, h, head, body, col, hh=6.4, fs_h=10.2, fs_b=9.0):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.4,rounding_size=1.5",
                                    fc=col, ec="none", alpha=.13, zorder=1))
        if head:
            ax.add_patch(FancyBboxPatch((x, y + h - hh), w, hh,
                                        boxstyle="round,pad=0.4,rounding_size=1.5",
                                        fc=col, ec="none", zorder=2))
            ax.text(x + w/2, y + h - hh/2, head, ha="center", va="center",
                    fontsize=fs_h, color="white", fontweight="bold", zorder=3)
            ax.text(x + w/2, y + (h - hh)/2, body, ha="center", va="center",
                    fontsize=fs_b, color=INK2, zorder=3, linespacing=1.35)
        else:
            ax.text(x + w/2, y + h/2, body, ha="center", va="center",
                    fontsize=fs_b, color=INK2, zorder=3, linespacing=1.35)

    arr = dict(arrowstyle="-|>", mutation_scale=16, color=INK3, lw=2.0, zorder=4)
    # 1 boi canh
    box(4, 91, 92, 9, "", T["setting"], C["blue"], fs_b=9.4)
    ax.add_patch(FancyArrowPatch((50, 90.2), (50, 86.8), **arr))
    # 2 tieu chuan chon
    box(4, 72, 92, 14, T["elig"], T["eligb"], C["blue"])
    ax.add_patch(FancyArrowPatch((50, 71.2), (50, 67.8), **arr))
    # 3 dan so nghien cuu
    box(4, 53, 92, 14, T["coh"], T["cohb"], C["blue"])
    ax.add_patch(FancyArrowPatch((50, 52.2), (50, 48.8), **arr))
    # 4 phan nhom khong ngau nhien
    ax.add_patch(FancyBboxPatch((9, 38), 82, 10,
                                boxstyle="round,pad=0.4,rounding_size=1.5",
                                fc=SIG, ec="none", alpha=.11, zorder=1))
    ax.text(50, 45.2, T["alloc"].split("\n")[0], ha="center", va="center",
            fontsize=9.5, color=INK2, zorder=3)
    ax.text(50, 41.0, T["alloc"].split("\n")[1] + "   " + T["warn"],
            ha="center", va="center", fontsize=9.8, color=SIG,
            fontweight="bold", zorder=3)
    for x1 in (27, 73):
        ax.add_patch(FancyArrowPatch((50, 37.2), (x1, 33.6), **arr))
    # 5 hai nhom dich thay the
    box(4, 19, 44, 14, T["a"], T["an"], ALB, fs_b=12.5)
    box(52, 19, 44, 14, T["f"], T["fn"], FFP, fs_b=12.5)
    for x0 in (26, 74):
        ax.add_patch(FancyArrowPatch((x0, 18.2), (50, 14.8), **arr))
    # 6 ket cuc
    box(4, 0, 92, 14, T["end"], T["endb"], C["aqua"])
    fig.savefig(out, dpi=300); plt.close(fig)

# ============================================================================
def run(lang):
    od = os.path.join(HERE, "figs_%s" % lang)
    os.makedirs(od, exist_ok=True)
    P = lambda n: os.path.join(od, n)
    fig0(lang, P("f0_pipeline.png"))
    fig0_tall(lang, P("f0_pipeline_tall.png"))
    fig_design(lang, P("f00_study_design.png"))
    fig1(lang, P("f1_distribution.png"))
    fig2(lang, P("f2_severity_profile.png"))
    fig3(lang, P("f3_forest_univariate.png"))
    fig4(lang, P("f4_forest_multivariable.png"))
    fig5(lang, P("f5_paired_tg.png"))
    fig6(lang, P("f6_scores_dumbbell.png"))
    r8 = fig8(lang, P("f8_adjusted.png"))
    fig7(lang, P("f7_reduction_compare.png"))
    r9 = fig9(lang, P("f9_pvalue_strip.png"))
    fig10(lang, P("f10_sensitivity.png"))
    print("[%s] xong -> %s" % (lang, od))
    return r8, r9

if __name__ == "__main__":
    langs = sys.argv[1:] or ["vn", "en"]
    r8 = r9 = None
    for lg in langs:
        r8, r9 = run(lg)
    print("\n--- so lieu de dien vao poster ---")
    print("Hieu chinh nhieu:")
    for nm, r in zip(["Tho", "+TG0,V", "+may"], r8):
        print("  %-8s ratio=%.2f (%.2f-%.2f) p=%.3f R2=%.2f" % (nm, *r))
    print("Da so sanh: %d/%d p<0.05 tho, %d sau BH, Bonferroni=%.4f"
          % (r9[0], r9[1], r9[2], r9[3]))
    if MULTI:
        for k, (b, se, pv, nag, ev, n) in MULTI.items():
            print("Mo hinh %s: n=%d, bien co=%d, Nagelkerke R2=%.3f" % (k, n, ev, nag))
    nn, nt = norm_counts()
    print("Phan phoi: %d/%d bien chuan, %d/%d khong chuan" % (nn, nt, nt-nn, nt))
