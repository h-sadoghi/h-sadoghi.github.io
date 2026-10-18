---
layout: legacy_page
title: CVXPY Guidance
permalink: /resources/teaching-patterneffort-cvxpy-guidance/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/patterneffort/cvxpy_guidance/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

# راهنمای جامع بهینه‌سازی محدب با CVXPY

## از برنامه‌ریزی خطی تا توصیف داده با بردار پشتیبان

# بخش اول: برنامه‌ریزی خطی (Linear Programming)

## ۱.۱ معرفی

**برنامه‌ریزی خطی** (LP) یکی از پایه‌ای‌ترین و پرکاربردترین روش‌های بهینه‌سازی است. در این نوع مسائل:

- **تابع هدف** خطی است.
- **قیود (محدودیت‌ها)** خطی هستند.
- هدف، **حداکثر یا حداقل کردن** تابع هدف در ناحیه‌ی شدنی است.

**فرم کلی مسئله:**

$$\max_{x} \quad c^T x$$

$$\text{s.t.} \quad Ax \leq b$$

$$x \geq 0$$

---

### مثال ساده

**مسئله:**

$$\max \quad Z = 3x_1 + 2x_2$$

$$\text{s.t.} \quad x_1 + x_2 \leq 6$$

$$2x_1 + x_2 \leq 10$$

$$x_1, x_2 \geq 0$$

**حل ریاضی:**

**گام ۱: یافتن رأس‌ها**

رأس‌های ناحیه‌ی شدنی از تقاطع قیدهاست:

- تقاطع محور $x_2$ با قید اول: $(0, 6)$
- تقاطع محور $x_1$ با قید دوم: $(5, 0)$
- تقاطع دو قید اصلی:

$$x_1 + x_2 = 6 \quad \text{و} \quad 2x_1 + x_2 = 10$$

از تفریق: $x_1 = 4$، پس $x_2 = 2$ → نقطه $(4, 2)$

- مبدأ: $(0, 0)$

**گام ۲: محاسبه تابع هدف در رأس‌ها**

| نقطه رأس |   $Z = 3x_1 + 2x_2$   |
| :------: | :-------------------: |
| $(0, 0)$ |          $0$          |
| $(5, 0)$ |         $15$          |
| $(4, 2)$ | $\mathbf{16}$ ← بهینه |
| $(0, 6)$ |         $12$          |

**نتیجه:** جواب بهینه

$$
x_1^* = 4، x_2^* = 2، Z^* = 16
$$

<div markdown="1">

</div>

<div class="caption" markdown="1">

شکل ۱: ناحیه شدنی و رأس‌های — نقطه ستاره بهینه است

</div>

---

## ۱.۲ حل با CVXPY

```python
import cvxpy as cp
import numpy as np

# ==== مثال ساده (Graphical) ====
x = cp.Variable(2, nonneg=True, name="x")

# ضرایب تابع هدف
c = np.array([3, 2])

# ماتریس قیود
A = np.array([[1, 1],
              [2, 1]])
b = np.array([6, 10])

# تعریف مسئله
objective = cp.Maximize(c @ x)
constraints = [A @ x <= b]
prob = cp.Problem(objective, constraints)
prob.solve()

print("=== مثال ساده ===")
print(f"جواب بهینه: x1={x.value[0]:.2f}, x2={x.value[1]:.2f}")
print(f"مقدار هدف: Z={prob.value:.2f}")
```

**خروجی:**

```
=== مثال ساده ===
جواب بهینه: x1=4.00, x2=2.00
مقدار هدف: Z=16.00
```

---

# بخش دوم: برنامه‌ریزی درجه دوم (Quadratic Programming)

## ۲.۱ فرم کلی

**برنامه‌ریزی درجه دوم** (QP) تعمیم LP است که تابع هدف درجه دوم دارد اما قیود همچنان خطی هستند:

$$\min_{x} \quad \frac{1}{2} x^T Q x + c^T x$$

$$\text{s.t.} \quad Ax \leq b$$

$$Cx = d$$

$$x \geq 0$$

**توضیح متغیر ها:**

- $Q \in \mathbb{R}^{n \times n}$: ماتریس درجه دوم — برای محدب بودن باید **نیمه معین مثبت (PSD)** باشد ($Q \succeq 0$)
- $c \in \mathbb{R}^n$: بردار ضرایب خطی
- $A, b$: قیدهای نامساوی
- $C, d$: قیدهای تساوی

**شرط محدب بودن QP:** ماتریس $Q$ نیمه معین مثبت باشد. یعنی برای هر $v \neq 0$: $v^T Q v \geq 0$

<div markdown="1">

</div>

<div class="caption" markdown="1">

شکل ۲: چپ — تابع محدب (هر کمینه محلی = کمینه کلی)؛ راست — تابع غیرمحدب

</div>

---

## ۲.۲ مثال ساده QP — حل کامل ریاضی

**مسئله:**

$$\min \quad f(x_1, x_2) = x_1^2 + x_2^2 - 2x_1 - 4x_2$$

$$\text{s.t.} \quad x_1 + x_2 \leq 4$$

$$x_1, x_2 \geq 0$$

**بیان ماتریسی:**

$$Q = \begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix}, \quad c = \begin{pmatrix} -2 \\ -4 \end{pmatrix}$$

**گام ۱: شرط KKT (Karush-Kuhn-Tucker)**

لاگرانژیان:

$$\mathcal{L} = x_1^2 + x_2^2 - 2x_1 - 4x_2 + \lambda(x_1 + x_2 - 4) - \mu_1 x_1 - \mu_2 x_2$$

شرایط مانایی (Stationarity):

$$\frac{\partial \mathcal{L}}{\partial x_1} = 2x_1 - 2 + \lambda - \mu_1 = 0$$

$$\frac{\partial \mathcal{L}}{\partial x_2} = 2x_2 - 4 + \lambda - \mu_2 = 0$$

**گام ۲: بررسی حالت‌ها**

فرض: قید $x_1 + x_2 \leq 4$ **غیرفعال** است ($\lambda = 0$) و $x_1, x_2 > 0$ ($\mu_1 = \mu_2 = 0$):

$$2x_1 - 2 = 0 \Rightarrow x_1^* = 1$$

$$2x_2 - 4 = 0 \Rightarrow x_2^* = 2$$

**تأیید:** $x_1 + x_2 = 3 \leq 4$ ✓، $x_1 = 1 \geq 0$ ✓، $x_2 = 2 \geq 0$ ✓

**مقدار بهینه:**

$$f^* = 1 + 4 - 2 - 8 = -5$$

**نتیجه:**

$$
x_1^* = 1، x_2^* = 2، f^* = -5
$$

<!-- QP Contours
_شکل ۷: منحنی‌های تراز تابع هدف QP — نقطه بهینه (۱، ۲) داخل ناحیه شدنی است_ -->

<div markdown="1">

</div>

<div class="caption" markdown="1">

شکل ۳: منحنی‌های تراز تابع هدف — نقطه بهینه (۱، ۲) داخل ناحیه شدنی است

</div>

---

## ۲.۳ حل QP با CVXPY

```python
import cvxpy as cp
import numpy as np

# ==== مثال ساده QP ====
x = cp.Variable(2, name="x")

Q1 = np.array([[2, 0], [0, 2]])
c1 = np.array([-2, -4])
A1 = np.array([[1, 1]])
b1 = np.array([4])

objective1 = cp.Minimize(0.5 * cp.quad_form(x, Q1) + c1 @ x)
constraints1 = [A1 @ x <= b1, x >= 0]
prob1 = cp.Problem(objective1, constraints1)
prob1.solve()

print("=== مثال ساده QP ===")
print(f"جواب بهینه: x1={x.value[0]:.4f}, x2={x.value[1]:.4f}")
print(f"مقدار هدف: f*={prob1.value:.4f}")
```

**خروجی:**

```
=== مثال ساده QP ===
جواب بهینه: x1=1.0000, x2=2.0000
مقدار هدف: f*=-5.0000
```

---

# بخش سوم: توصیف داده با بردار پشتیبان (SVDD)

## ۳.۱ معرفی و انگیزه

**توصیف داده با بردار پشتیبان** یا SVDD یک روش **تشخیص ناهنجاری (Anomaly Detection)** است که توسط Tax و Duin (2004) معرفی شد.

**هدف:** کوچک‌ترین کره‌ای پیدا کن که اکثر داده‌های هدف را پوشش دهد. هر نقطه خارج از این کره **ناهنجاری** محسوب می‌شود.

<div markdown="1">

</div>

<div class="caption" markdown="1">

شکل ۴: چپ — بر داده‌های نرمال؛ راست — نقاط قرمز خارج از کره ناهنجاری

</div>

**کاربردها:**

- تشخیص تقلب (Fraud Detection)
- تشخیص خرابی در ماشین‌آلات (Fault Detection)
- تشخیص نفوذ شبکه (Network Intrusion Detection)
- طبقه‌بندی تک‌کلاسه (One-Class Classification)

---

## ۳.۲ فرم اولیه (Primal Form)

**مسئله:** یافتن مرکز $a$ و شعاع $R$ برای کوچک‌ترین کره‌ای که اکثر نقاط $\{x_i\}_{i=1}^n$ را دربرمی‌گیرد.

$$\min_{R, a, \xi} \quad R^2 + C \sum_{i=1}^{n} \xi_i$$

$$\text{s.t.} \quad \|x_i - a\|_2^2 \leq R^2 + \xi_i \quad \forall i = 1, \ldots, n$$

$$\xi_i \geq 0 \quad \forall i$$

$$R \geq 0$$

**توضیح متغیرها:**

- $R \in \mathbb{R}^+$: شعاع کره
- $a \in \mathbb{R}^d$: مرکز کره
- $\xi_i \geq 0$: متغیرهای شل (Slack Variables) — اجازه می‌دهند برخی نقاط خارج از کره باشند
- $C > 0$: پارامتر ترازبخشی — مقدار بزرگ‌تر $C$ کره سخت‌گیرتر (ناهنجاری کمتر)، مقدار کوچک‌تر کره کوچک‌تر اما با تولرانس بیشتر

---

## ۳.۳ استخراج فرم دوگان (Dual Form)

**لاگرانژیان:**

$$\mathcal{L} = R^2 + C\sum_i \xi_i - \sum_i \alpha_i (R^2 + \xi_i - \|x_i - a\|_2^2) - \sum_i \gamma_i \xi_i$$

جایی که $\alpha_i \geq 0$ و $\gamma_i \geq 0$ ضرایب لاگرانژ هستند.

**شرایط KKT:**

**۱. نسبت به $R$:**

$$\frac{\partial \mathcal{L}}{\partial R} = 2R - 2R\sum_i \alpha_i = 0 \Rightarrow \sum_{i=1}^n \alpha_i = 1$$

**۲. نسبت به $a$:**

$$\frac{\partial \mathcal{L}}{\partial a} = 2\sum_i \alpha_i (x_i - a) = 0 \Rightarrow a = \sum_{i=1}^n \alpha_i x_i$$

**۳. نسبت به $\xi_i$:**

$$\frac{\partial \mathcal{L}}{\partial \xi_i} = C - \alpha_i - \gamma_i = 0 \Rightarrow \alpha_i = C - \gamma_i$$

چون $\gamma_i \geq 0$، داریم $\alpha_i \leq C$.

**جایگزینی در لاگرانژیان:**

مرکز بهینه: $a^* = \sum_i \alpha_i x_i$

$$\|x_i - a\|^2 = \langle x_i, x_i \rangle - 2\sum_j \alpha_j \langle x_i, x_j \rangle + \sum_{j,k} \alpha_j \alpha_k \langle x_j, x_k \rangle$$

**فرم دوگان نهایی:**

$$\max_{\alpha} \quad \sum_i \alpha_i \langle x_i, x_i \rangle - \sum_{i,j} \alpha_i \alpha_j \langle x_i, x_j \rangle$$

$$\text{s.t.} \quad \sum_i \alpha_i = 1$$

$$0 \leq \alpha_i \leq C \quad \forall i$$

**تفسیر $\alpha_i$:**

|  مقدار $\alpha_i$  |          نوع نقطه           |
| :----------------: | :-------------------------: |
|   $\alpha_i = 0$   |      داخل کره (نرمال)       |
| $0 < \alpha_i < C$ | روی مرز کره (بردار پشتیبان) |
|   $\alpha_i = C$   |   خارج از کره (ناهنجاری)    |

**محاسبه شعاع:** برای یک بردار پشتیبان $x_s$ با $0 < \alpha_s < C$:

$$R^2 = \|x_s - a\|^2 = \langle x_s, x_s \rangle - 2\sum_j \alpha_j \langle x_s, x_j \rangle + \sum_{j,k} \alpha_j \alpha_k \langle x_j, x_k \rangle$$

**قانون تشخیص ناهنجاری:**

$$\|x_{\text{test}} - a^*\|^2 \leq R^2 \quad \Rightarrow \quad \text{نرمال}$$

$$\|x_{\text{test}} - a^*\|^2 > R^2 \quad \Rightarrow \quad \text{ناهنجاری}$$

---

## ۳.۴ تعمیم با Kernel

با جایگزینی $\langle x_i, x_j \rangle$ با تابع هسته $K(x_i, x_j)$، مرز تصمیم می‌تواند غیرخطی شود:

**kernel های متداول:**

$$K_{\text{RBF}}(x_i, x_j) = \exp\left(-\frac{\|x_i - x_j\|^2}{2\sigma^2}\right)$$

$$K_{\text{Polynomial}}(x_i, x_j) = (\langle x_i, x_j \rangle + r)^d$$

---

## ۳.۵ پیاده‌سازی SVDD با CVXPY (فرم اولیه)

```python
import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. Generate synthetic data
# ============================================================
np.random.seed(42)
n = 50          # number of samples
d = 2           # number of features
X = np.random.randn(n, d) * 0.5 + 1.5

C_param = 0.1   # trade-off parameter

# ============================================================
# 2. Precompute ||x_i||²  (diagonal of the Gram matrix)
#
#   K[i,j] = <x_i, x_j>  →  K[i,i] = ||x_i||²
#
#   We NEVER build the full n×n matrix K explicitly.
#   Reason explained in Section 4 below.
# ============================================================
kii = np.sum(X ** 2, axis=1)    # shape (n,)

# ============================================================
# 3. Define the CVXPY dual variable
#
#   α ∈ ℝⁿ — one weight per training point.
#   nonneg=True enforces  αᵢ ≥ 0  at the variable level.
# ============================================================
alpha = cp.Variable(n, nonneg=True, name="alpha")

# ============================================================
# 4. Dual objective — DCP-compliant formulation
#
#   From KKT (Section 3.3), the dual to solve is:
#
#     max  Σᵢ αᵢ‖xᵢ‖²  −  Σᵢⱼ αᵢ αⱼ <xᵢ,xⱼ>
#   ≡ min  αᵀ K α  −  diag(K)ᵀ α                        ... (*)
#
#   ─── Why NOT cp.quad_form(alpha, K)? ─────────────────────
#   K = X Xᵀ is rank-d (here d=2, n=50), so 48 eigenvalues
#   are numerically zero.  CVXPY's quad_form verifies PSD via
#   Cholesky decomposition and raises DCPError on any
#   rank-deficient matrix — even if all eigenvalues are ≥ 0.
#
#   ─── Algebraic fix (exact, no approximation) ──────────────
#   Because K = X Xᵀ, the quadratic term factors cleanly:
#
#     αᵀ K α  =  αᵀ (X Xᵀ) α  =  (Xᵀα)ᵀ (Xᵀα)  =  ‖Xᵀα‖²
#
#   So (*) becomes:
#
#     min  ‖Xᵀα‖²  −  diag(K)ᵀ α
#
#   cp.sum_squares(X.T @ alpha) = ‖Xᵀα‖²
#   This is always convex and DCP-compliant regardless of rank.
# ============================================================
dual_objective = cp.Minimize(
    cp.sum_squares(X.T @ alpha)   # ‖Xᵀα‖² = αᵀKα  ← always DCP
    - kii @ alpha                  # − diag(K)ᵀα     ← affine
)

# ============================================================
# 5. Dual constraints (directly from KKT)
#
#   ∂L/∂R  = 0  →  Σᵢ αᵢ = 1
#   ∂L/∂ξᵢ = 0  →  αᵢ = C − γᵢ,  γᵢ ≥ 0  →  αᵢ ≤ C
# ============================================================
constraints = [
    cp.sum(alpha) == 1,    # Σ αᵢ = 1
    alpha <= C_param,      # αᵢ ≤ C   (αᵢ ≥ 0 from nonneg=True)
]

# ============================================================
# 6. Solve
# ============================================================
problem = cp.Problem(dual_objective, constraints)
problem.solve(solver=cp.ECOS, abstol=1e-9, reltol=1e-9)

print(f"Status      : {problem.status}")
print(f"Sum(alpha)  : {alpha.value.sum():.10f}  (must equal 1)")

# ============================================================
# 7. Recover primal variables from α*
#
#   Because K = X Xᵀ, all kernel inner products simplify:
#
#   Centre:
#     a* = Σᵢ αᵢ xᵢ = Xᵀ α*                (from ∂L/∂a = 0)
#
#   Radius (for any support vector x_s with 0 < α_s < C):
#     R² = K[s,s] − 2·αᵀK[:,s] + αᵀKα
#        = ‖x_s‖² − 2·(Xᵀα)·x_s + ‖Xᵀα‖²
#        = ‖x_s − Xᵀα‖²
#        = ‖x_s − a*‖²              ← plain Euclidean distance
# ============================================================
alpha_opt = alpha.value

# Centre
a_star = X.T @ alpha_opt          # = alpha_opt @ X
print(f"\nOptimal centre  a* = {np.round(a_star, 4)}")

# Classify training points by their α role
EPS          = 1e-5
inside_mask  = alpha_opt < EPS
sv_mask      = (alpha_opt >= EPS) & (alpha_opt < C_param - EPS)
outside_mask = alpha_opt >= C_param - EPS

print(f"\nPoint classification:")
print(f"  Inside  (α ≈ 0)        : {inside_mask.sum():3d} points")
print(f"  Support Vectors        : {sv_mask.sum():3d} points  ← used to compute R*")
print(f"  Outside (α = C)        : {outside_mask.sum():3d} points  (anomalies)")

# Radius averaged over all support vectors (values should be identical)
sv_indices = np.where(sv_mask)[0]
if len(sv_indices) > 0:
    R_sq_vals = [np.sum((X[s] - a_star) ** 2) for s in sv_indices]
    R_star    = float(np.sqrt(np.mean(R_sq_vals)))
else:
    # Fallback when no SVs exist (unusual; try adjusting C)
    dists  = np.linalg.norm(X - a_star, axis=1)
    R_star = float(np.percentile(dists, (1.0 - C_param) * 100.0))
    print("  [Warning] No SVs found — using percentile fallback for R*")

print(f"\nOptimal radius  R* = {R_star:.6f}")

# ============================================================
# 8. Anomaly detection
#
#   Decision rule (from dual derivation):
#     ‖x_test − a*‖ ≤ R*  →  Normal
#     ‖x_test − a*‖ > R*  →  Anomaly
# ============================================================
def predict_svdd(x_test, center, R):
    distances = np.linalg.norm(x_test - center, axis=1)
    labels    = distances <= R      # True = Normal
    return labels, distances

test_points = np.array([
    [1.5, 1.5],   # normal  — near centre
    [5.0, 5.0],   # anomaly — far away
    [1.0, 2.0],   # normal  — inside sphere
])

labels, dists = predict_svdd(test_points, a_star, R_star)
print("\nTest predictions:")
print(f"  {'Point':<14} {'Distance':>10}   {'Result'}")
print("  " + "─" * 38)
for pt, dist, lbl in zip(test_points, dists, labels):
    print(f"  {str(pt):<14} {dist:>10.4f}   {'Normal  ✓' if lbl else 'Anomaly ✗'}")

# ============================================================
# 9. Plot
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))

ax.scatter(X[inside_mask, 0], X[inside_mask, 1],
           c='steelblue', s=60, edgecolors='k', linewidths=0.5,
           zorder=3, label=r'Normal ($\alpha_i \approx 0$)')

ax.scatter(X[sv_mask, 0], X[sv_mask, 1],
           c='gold', s=180, edgecolors='k', linewidths=1.3,
           zorder=5, marker='D',
           label=r'Support Vector ($0 < \alpha_i < C$)')

ax.scatter(X[outside_mask, 0], X[outside_mask, 1],
           c='red', s=130, edgecolors='k', linewidths=0.8,
           zorder=4, marker='X',
           label=r'Anomaly ($\alpha_i = C$)')

theta = np.linspace(0, 2 * np.pi, 400)
ax.plot(a_star[0] + R_star * np.cos(theta),
        a_star[1] + R_star * np.sin(theta),
        'r-', linewidth=2.5, label=f'SVDD Boundary (R={R_star:.3f})')

ax.plot(*a_star, 'r+', markersize=18, markeredgewidth=3,
        label=r'Centre $a^*$', zorder=6)

for pt, lbl, dist in zip(test_points, labels, dists):
    colour = 'green' if lbl else 'darkred'
    ax.plot(*pt, 's', ms=12, color=colour, mec='k', mew=1.2, zorder=7)
    ax.annotate(f'd={dist:.2f}', pt, xytext=(8, 5),
                textcoords='offset points', fontsize=8, color=colour)

ax.set_aspect('equal')
ax.set_xlim(-0.3, 3.5)
ax.set_ylim(-0.3, 3.5)
ax.set_xlabel('Feature 1 ($x_1$)', fontsize=12)
ax.set_ylabel('Feature 2 ($x_2$)', fontsize=12)
ax.set_title(
    f'SVDD — Dual Form (CVXPY)\n'
    f'$R^* = {R_star:.3f}$,  $C = {C_param}$,  '
    f'SVs = {sv_mask.sum()},  Anomalies = {outside_mask.sum()}',
    fontsize=13, fontweight='bold')
ax.legend(fontsize=9, loc='upper right')
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('svdd_result.png', dpi=130)
plt.show()
```

---

**خروجی:**

```
Status      : optimal
Sum(alpha)  : 1.0000000000  (must equal 1)

Optimal centre  a* = [1.4602 1.4449]

Point classification:
  Inside  (α ≈ 0)        :  39 points
  Support Vectors        :   3 points
  Outside (α = C)        :   8 points

Optimal radius  R* = 0.853106

Test predictions:
  Result            Distance   Point
  ──────────────────────────────────────
  [1.5 1.5]          0.0680   Normal  ✓
  [5. 5.]            5.0169   Anomaly ✗
  [1. 2.]            0.7210   Normal  ✓
```

<div markdown="1">

</div>

---

# مراجع

1. **Boyd, S., & Vandenberghe, L. (2004). _Convex Optimization_. Cambridge University Press.** [stanford.edu](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)

2. **Tax, D. M. J., & Duin, R. P. W. (2004). Support Vector Data Description. _Machine Learning_, 54(1), 45–66.** [Springer](https://link.springer.com/article/10.1023/B:MACH.0000008084.60811.49)

3. **Diamond, S., & Boyd, S. (2016). CVXPY: A Python-Embedded Modeling Language for Convex Optimization. _JMLR_, 17(83), 1–5.** [JMLR](http://jmlr.org/papers/v17/15-454.html) | [Documentation](https://www.cvxpy.org/)

4. **Nocedal, J., & Wright, S. J. (2006). _Numerical Optimization_ (2nd ed.). Springer.**

5. **Bazaraa, M. S., Jarvis, J. J., & Sherali, H. D. (2011). _Linear Programming and Network Flows_ (4th ed.). Wiley.**

6. **Schölkopf, B., & Smola, A. J. (2002). _Learning with Kernels_. MIT Press.**
   {% endraw %}
