---
layout: legacy_page
title: Non Linear Programming
permalink: /resources/teaching-patterneffort-nlp-libraries-comparison/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/patterneffort/nlp_libraries_comparison/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

# مقایسه کتابخانه‌های بهینه‌سازی غیرخطی (NLP) در پایتون

در این راهنما یک **مسأله ثابت** را با سه کتابخانه مطرح پایتون حل می‌کنیم و نتایج را با تصویرسازی کامل مقایسه می‌کنیم.

---

## 📐 پایه ریاضی مسأله

**هدف:** کمینه‌سازی مجموع مربعات (فاصله اقلیدسی از مبدأ)

$$\min_{x_1, x_2, x_3} \quad f(x_1, x_2, x_3) = x_1^2 + x_2^2 + x_3^2$$

**تحت قیود:**

| #   | نوع                    | فرمول                           | توضیح                     |
| --- | ---------------------- | ------------------------------- | ------------------------- |
| 1   | قید **خطی** (تساوی)    | $x_1 + x_2 + x_3 = 3$           | مجموع متغیرها ثابت است    |
| 2   | قید **غیرخطی** (تساوی) | $x_1 \times x_2 \times x_3 = 1$ | حاصل‌ضرب متغیرها ثابت است |

> **جواب تحلیلی:** طبق نامساوی AM-GM، جواب بهینه $x_1 = x_2 = x_3 = 1$ است که مقدار $f^* = 3$ را می‌دهد.

---

## 🗂️ کتابخانه‌های مورد بررسی

| #   | کتابخانه   | نصب                  | سالور         | روش گرادیان                | کاربرد اصلی              |
| --- | ---------- | -------------------- | ------------- | -------------------------- | ------------------------ |
| 1   | **SciPy**  | پیش‌نصب              | SLSQP         | Finite Difference (تقریب)  | علمی عمومی — سریع و ساده |
| 2   | **GEKKO**  | `pip install gekko`  | IPOPT (داخلی) | Automatic Diff             | کنترل بهینه و DAE        |
| 3   | **CasADi** | `pip install casadi` | IPOPT (داخلی) | Automatic Diff (دقیق‌ترین) | رباتیک، MPC، هوافضا      |

---

## 🔄 مراحل حل هر سالور

```
① تعریف تابع هدف f(x)
② تعریف قیود g(x) = 0
③ تعیین نقطه شروع x₀
④ فراخوانی الگوریتم بهینه‌سازی (SLSQP یا IPOPT)
⑤ استخراج جواب x* و تحقق قیود
⑥ مقایسه با جواب تحلیلی
```

---

## ⚙️ راه‌اندازی اولیه — NumPy و نقطه شروع

```python
import numpy as np

# نقطه اولیه (Initial Guess)
# اکثر سالورهای NLP گرادیان‌محور از یک نقطه شروع کرده و به‌سمت minimum حرکت می‌کنند.
# نقطه شروع (x0) روی سرعت همگرایی و یافتن minimum محلی vs جهانی تأثیر دارد.
x0 = [0.5, 0.5, 0.5]

# جواب تحلیلی (Analytical Solution)
# با استفاده از نامساوی AM-GM:
#   AM ≥ GM  →  (x1+x2+x3)/3 ≥ (x1·x2·x3)^(1/3)
#   3/3 ≥ 1^(1/3)  →  تساوی فقط زمانی برقرار است که x1=x2=x3
# پس جواب بهینه: x1 = x2 = x3 = 1 ، مقدار تابع: f* = 1² + 1² + 1² = 3
x_analytical = np.array([1.0, 1.0, 1.0])

print(f"📌 حدس اولیه: {x0}")
print(f"🎯 جواب تحلیلی: {x_analytical.tolist()}")
print(f"🎯 مقدار بهینه تابع هدف: f* = {sum(x_analytical**2)}")
```

**خروجی:**

```
📌 حدس اولیه: [0.5, 0.5, 0.5]
🎯 جواب تحلیلی: [1.0, 1.0, 1.0]
🎯 مقدار بهینه تابع هدف: f* = 3.0
```

---

## 1️⃣ SciPy — `scipy.optimize.minimize` با روش SLSQP

### ویژگی‌ها

- بدون نیاز به نصب جداگانه (بخشی از اکوسیستم SciPy)
- سالور پیش‌فرض `SLSQP` برای مسائل NLP با قید
- قیود به‌صورت دیکشنری تعریف می‌شوند: `{'type': 'eq'|'ineq', 'fun': ...}`
- مناسب برای مسائل کوچک تا متوسط

### الگوریتم SLSQP چیست؟

**SLSQP = Sequential Least SQuares Programming**

- در هر تکرار یک زیرمسأله QP (برنامه‌ریزی درجه‌دوم) حل می‌کند
- گرادیان را با **تفاضل متناهی (Finite Difference)** تقریب می‌زند:

$$\frac{\partial f}{\partial x_i} \approx \frac{f(x + h e_i) - f(x)}{h} \qquad \text{خطای } O(h)$$

- برای مسائل کوچک تا متوسط (< ~1000 متغیر) مناسب است

### کد پیاده‌سازی

```python
from scipy.optimize import minimize

# ── تعریف تابع هدف ────────────────────────────────────────────────────────
def obj_scipy(x):
    # f(x) = x1² + x2² + x3²  (مجموع مربعات = distance² از مبدأ)
    return x[0]**2 + x[1]**2 + x[2]**2

# ── تعریف قیود به‌صورت دیکشنری ────────────────────────────────────────────
# 'type': 'eq'  → g(x) = 0  (قید تساوی)
# 'fun'         → تابعی که g(x) را برمی‌گرداند (باید صفر شود)
cons_scipy = (
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] - 3},   # g₁: x1+x2+x3-3 = 0
    {'type': 'eq', 'fun': lambda x: x[0] * x[1] * x[2] - 1}    # g₂: x1·x2·x3-1 = 0
)

# ── ردیابی مسیر همگرایی با Callback ──────────────────────────────────────
# callback(xk): بعد از هر تکرار فراخوانی می‌شود (xk = نقطه فعلی)
scipy_history = {'x': [], 'f': [], 'g1': [], 'g2': []}

def scipy_callback(xk):
    scipy_history['x'].append(xk.copy())
    scipy_history['f'].append(obj_scipy(xk))
    scipy_history['g1'].append(abs(xk[0] + xk[1] + xk[2] - 3))  # نقض قید ۱
    scipy_history['g2'].append(abs(xk[0] * xk[1] * xk[2] - 1))  # نقض قید ۲

# نقطه شروع نامتقارن (چرا نه [0.5,0.5,0.5]؟)
# SLSQP در نقاط متقارن ممکن است ماتریس ژاکوبین تکین (Singular) شود
x0_scipy = [0.8, 1.0, 1.2]

# ── فراخوانی سالور ────────────────────────────────────────────────────────
# ftol=1e-12 : همگرایی با دقت بسیار بالا (تغییر کمتر از 1e-12)
# maxiter=500: حداکثر تعداد تکرار
res_scipy = minimize(
    obj_scipy,
    x0_scipy,
    method='SLSQP',
    constraints=cons_scipy,
    callback=scipy_callback,
    options={'ftol': 1e-12, 'maxiter': 500}
)

# ── استخراج نتایج ─────────────────────────────────────────────────────────
sol_scipy    = np.round(res_scipy.x, 6)
obj_val_scipy = round(res_scipy.fun, 6)

print(f"وضعیت    : {'✅ موفق' if res_scipy.success else '❌ ناموفق'} — {res_scipy.message}")
print(f"جواب x*  : {np.round(sol_scipy, 4).tolist()}")
print(f"f(x*)    : {obj_val_scipy}")
print(f"‖x-x*‖   : {np.linalg.norm(sol_scipy - np.array([1,1,1])):.2e}")
print(f"تکرار    : {res_scipy.nit} iteration(s)")
print(f"ارزیابی  : {res_scipy.nfev} function evaluations")
```

**خروجی:**

```
وضعیت    : ✅ موفق — Optimization terminated successfully
جواب x*  : [1.0, 1.0, 1.0]
f(x*)    : 3.0
‖x-x*‖   : ~1e-10
تکرار    : ~12 iteration(s)
ارزیابی  : ~80 function evaluations
```

> **نکته کلیدی:** SciPy برای محاسبه گرادیان نیاز دارد تابع را چند بار اضافه ارزیابی کند (Finite Difference)، به همین دلیل `nfev` (تعداد ارزیابی) بیشتر از تعداد تکرار است.

---

## 2️⃣ GEKKO — بهینه‌سازی با سالور IPOPT داخلی

### ویژگی‌ها

- نصب: `pip install gekko`
- سالور IPOPT به‌صورت **باینری اجرایی داخلی** همراه پکیج ارائه می‌شود
- `remote=False` → اجرای کاملاً محلی (بدون اینترنت)
- مناسب برای کنترل بهینه و مسائل دینامیکی (DAE/ODE)
- متغیرها با `m.Array` یا `m.Var` تعریف می‌شوند

### ساختار مدل در GEKKO

```
① GEKKO(remote=False)   → ساخت مدل محلی
② m.Var(value=...)      → تعریف متغیرهای تصمیم
③ m.Obj(f(x))           → تعریف تابع هدف
④ m.Equation(g(x)==0)   → تعریف قیود
⑤ m.options.SOLVER = 3  → انتخاب IPOPT
⑥ m.solve(disp=False)   → اجرا
```

### انتخاب سالور در GEKKO

| گزینه        | توضیح                                                         |
| ------------ | ------------------------------------------------------------- |
| `SOLVER = 1` | APOPT — سالور اختصاصی GEKKO، مناسب MINLP                      |
| `SOLVER = 2` | BPOPT — سالور داخلی دیگر                                      |
| `SOLVER = 3` | **IPOPT** ← بهترین برای NLP پیوسته (Interior Point OPTimizer) |

### الگوریتم IPOPT

IPOPT از روش **نقطه داخلی (Interior Point Method)** استفاده می‌کند:

- به‌جای حرکت روی مرز فضای شدنی، از **داخل** آن عبور می‌کند
- برای مسائل بزرگ‌مقیاس بسیار کارآمد است

### کد پیاده‌سازی

```python
from gekko import GEKKO

# ── ساخت مدل ──────────────────────────────────────────────────────────────
# remote=False → اجرای کاملاً محلی (بدون اینترنت)
# remote=True  → ارسال به سرور APMonitor.com (نیاز به اینترنت)
m_g = GEKKO(remote=False)

# ── تعریف متغیرها ─────────────────────────────────────────────────────────
# m_g.Array(m_g.Var, 3, value=0.5)
#   → آرایه‌ای از ۳ متغیر بهینه‌سازی با مقدار اولیه ۰.۵
xg = m_g.Array(m_g.Var, 3, value=0.5)
x1g, x2g, x3g = xg[0], xg[1], xg[2]

m_g.Obj(x1g**2 + x2g**2 + x3g**2)    # تابع هدف: کمینه کردن f = x1²+x2²+x3²
m_g.Equation(x1g + x2g + x3g == 3)   # قید ۱ — خطی:    x1+x2+x3 = 3
m_g.Equation(x1g * x2g * x3g == 1)   # قید ۲ — غیرخطی: x1·x2·x3 = 1

m_g.options.SOLVER = 3    # IPOPT — Interior Point OPTimizer
m_g.options.IMODE  = 3    # حالت ۳ = Steady-state optimization (پیش‌فرض NLP)
m_g.solve(disp=False)     # حل با لاگ خاموش

# ── استخراج نتایج ─────────────────────────────────────────────────────────
# variable.value[0] → GEKKO از لیست استفاده می‌کند؛ [0] مقدار اسکالر است.
sol_gekko    = np.round([x1g.value[0], x2g.value[0], x3g.value[0]], 6)
obj_val_gekko = round(sum(v**2 for v in sol_gekko), 6)

print(f"جواب x* : {np.round(sol_gekko, 4).tolist()}")
print(f"f(x*)   : {obj_val_gekko}")
print(f"‖x-x*‖  : {np.linalg.norm(sol_gekko - np.array([1,1,1])):.2e}")
```

**خروجی:**

```
جواب x* : [1.0, 1.0, 1.0]
f(x*)   : 3.0
‖x-x*‖  : ~1e-11
```

---

## 3️⃣ CasADi — مشتق‌گیری خودکار + IPOPT داخلی

### ویژگی‌ها

- نصب: `pip install casadi`
- تخصص در **Automatic Differentiation (AD)** — محاسبه گرادیان و هسیان دقیق
- زبان نمادین (Symbolic): `SX` (سریع‌تر) یا `MX` (انعطاف بیشتر)
- سالور IPOPT و OSQP به‌صورت داخلی موجودند
- اینترفیس یکپارچه با MATLAB و C++
- پرکاربرد در رباتیک، کنترل پیش‌بین مدل (MPC) و یادگیری ماشین

### Automatic Differentiation (AD) چیست؟

تفاوت اساسی با SciPy:

| روش        | نحوه محاسبه گرادیان              | دقت                           |
| ---------- | -------------------------------- | ----------------------------- |
| **SciPy**  | تفاضل متناهی (Finite Difference) | تقریبی $O(h) \approx 10^{-8}$ |
| **CasADi** | قانون زنجیره روی گراف محاسباتی   | دقت ماشین $\approx 10^{-16}$  |

AD نه تفاضل عددی است، نه مشتق‌گیری نمادین — **قانون زنجیره (Chain Rule)** را روی گراف محاسباتی اعمال می‌کند:

- پیچیدگی: $O(n)$ برای **forward mode**، $O(m)$ برای **reverse mode**
- نتیجه: گرادیان کاملاً دقیق بدون هیچ تقریبی

### ساختار مدل در CasADi

```
① SX.sym('x', n)       → تعریف متغیرهای نمادین
② f = expr(x)          → تعریف تابع هدف نمادین
③ g = vertcat(...)     → بردار قیود نمادین
④ nlpsol(...)          → ساخت سالور با backend IPOPT
⑤ solver(x0, lbg, ubg) → حل عددی
```

### کد پیاده‌سازی

```python
import casadi as ca

# ── تعریف متغیرهای نمادین (Symbolic Variables) ────────────────────────────
# ca.SX.sym('x', 3) → بردار نمادین 3×1
#   SX = Scalar eXpression  — برای مسائل کوچک: سریع‌ترین نوع
#   MX = Matrix eXpression  — برای مسائل بزرگ یا با ماتریس‌های پراکنده
# نکته: در این مرحله هیچ عدد محاسبه نمی‌شود — فقط نماد ریاضی
x_ca = ca.SX.sym('x', 3)   # [x₁, x₂, x₃] — بردار نمادین

# ── تعریف تابع هدف نمادین ────────────────────────────────────────────────
# CasADi از این عبارت، گراف محاسباتی (Computational Graph) می‌سازد
# و سپس گرادیان و هسیان را دقیقاً از آن مشتق می‌گیرد.
obj_ca = x_ca[0]**2 + x_ca[1]**2 + x_ca[2]**2   # f = x1²+x2²+x3²  (نمادین)

# ── تعریف بردار قیود g(x) ────────────────────────────────────────────────
# ca.vertcat() → متصل کردن عمودی (vertical concatenation)
# قراداد CasADi برای قیود:  lbg ≤ g(x) ≤ ubg
# برای تساوی: lbg = ubg = 0  →  g(x) = 0 دقیقاً
g_ca = ca.vertcat(
    x_ca[0] + x_ca[1] + x_ca[2] - 3,    # g₁ = x1+x2+x3-3  (باید = 0)
    x_ca[0] * x_ca[1] * x_ca[2] - 1     # g₂ = x1·x2·x3-1  (باید = 0)
)

# ── ساخت دیکشنری NLP و سالور ──────────────────────────────────────────────
# فرمت استاندارد NLP در CasADi: {'x': متغیرها, 'f': هدف, 'g': قیود}
nlp = {'x': x_ca, 'f': obj_ca, 'g': g_ca}

solver_ca = ca.nlpsol(
    'solver', 'ipopt', nlp,
    {
        'print_time'        : 0,
        'ipopt.print_level' : 0,
        'ipopt.tol'         : 1e-12,   # تلورانس نهایی IPOPT
        'ipopt.max_iter'    : 1000     # حداکثر تکرار IPOPT
    }
)

# ── حل مسأله ──────────────────────────────────────────────────────────────
# solver_ca(x0, lbg, ubg):
#   x0  = [0.5, 0.5, 0.5]  → نقطه شروع عددی
#   lbg = [0, 0]           → کران پایین  g(x) ≥ 0
#   ubg = [0, 0]           → کران بالای  g(x) ≤ 0
#   ترکیب lbg=ubg=0 → g(x) = 0  (قید تساوی دقیق)
res_ca = solver_ca(x0=[0.5, 0.5, 0.5], lbg=[0, 0], ubg=[0, 0])

# ── استخراج نتایج ─────────────────────────────────────────────────────────
# res_ca['x']     → نوع DM (Dense Matrix) در CasADi
# res_ca['lam_g'] → ضرایب لاگرانژ قیود (Lagrange Multipliers)
sol_casadi    = np.round(np.array(res_ca['x']).flatten(), 6)
obj_val_casadi = round(float(res_ca['f']), 6)
lam_g         = np.array(res_ca['lam_g']).flatten()

print(f"جواب x*  : {np.round(sol_casadi, 4).tolist()}")
print(f"f(x*)    : {obj_val_casadi}")
print(f"‖x-x*‖   : {np.linalg.norm(sol_casadi - np.array([1,1,1])):.2e}")
print(f"λ (Lagrange Multipliers): {np.round(lam_g, 4).tolist()}")
```

**خروجی:**

```
جواب x*  : [1.0, 1.0, 1.0]
f(x*)    : 3.0
‖x-x*‖   : ~1e-12
λ (Lagrange Multipliers): [-2.0, -0.0]
```

---

## 📈 تصویرسازی — چشم‌انداز مسأله و مسیر حل

### پلات ۱ — چشم‌انداز مسأله

چون مسأله ۳ متغیر دارد، برای رسم ۲D از **تقلیل بُعد** استفاده می‌کنیم:

از قید خطی: $x_3 = 3 - x_1 - x_2$

بعد از جایگذاری:
$$f(x_1,x_2) = x_1^2 + x_2^2 + (3 - x_1 - x_2)^2$$

قید غیرخطی باقی‌مانده: $x_1 \cdot x_2 \cdot (3 - x_1 - x_2) = 1$

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# شبکه محاسباتی
x1_r = np.linspace(0.1, 2.7, 400)
x2_r = np.linspace(0.1, 2.7, 400)
X1, X2 = np.meshgrid(x1_r, x2_r)
X3 = 3 - X1 - X2         # مقدار x3 از قید خطی

F  = X1**2 + X2**2 + X3**2   # تابع هدف بعد از حذف x3
G2 = X1 * X2 * X3            # قید غیرخطی (باید = 1 باشد)

mask    = (X3 > 0) & (X1 > 0) & (X2 > 0)
F_plot  = np.where(mask, F, np.nan)
G2_plot = np.where(mask, G2, np.nan)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# ─ نمودار Contour 2D ─────────────────────────────────────────────────────
ax1 = axes[0]
cp  = ax1.contourf(X1, X2, F_plot, levels=30, cmap='YlOrRd', alpha=0.85)
plt.colorbar(cp, ax=ax1)
ax1.contour(X1, X2, G2_plot, levels=[1.0], colors='#e63946', linewidths=2.5)
ax1.plot(1, 1, '*', color='#2d6a4f', markersize=18, label='$x^* = (1,1,1)$')
ax1.set_title('2D View: Objective Contours')
ax1.legend()

# ─ نمودار Surface 3D ─────────────────────────────────────────────────────
ax2 = axes[1]
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(X1, X2, F_plot, cmap='coolwarm', alpha=0.7)
ax2.scatter([1], [1], [3], color='#2d6a4f', s=200, label='$x^* = (1,1,1)$')
ax2.set_title('3D Objective Surface')

plt.tight_layout()
plt.savefig('plot1_landscape.png', dpi=120, bbox_inches='tight')
plt.show()
```

### پلات ۲ — مسیر همگرایی SciPy

این پلات نشان می‌دهد:

- از کجا شروع شد (`x0`)
- در هر تکرار به کجا رفت (مسیر آبی)
- چقدر طول کشید به جواب بهینه برسد
- نحوه کاهش تابع هدف و نقض قیودها در طول تکرارها

```python
fig, axes = plt.subplots(1, 3, figsize=(17, 5))
x_path = np.array(scipy_history['x'])
iters  = np.arange(len(scipy_history['f']))

# ① مسیر روی Contour
axes[0].contourf(X1, X2, F_plot, levels=25, cmap='YlOrRd', alpha=0.8)
axes[0].contour(X1, X2, G2_plot, levels=[1.0], colors='#e63946', linewidths=2, linestyles='--')
axes[0].plot(x_path[:, 0], x_path[:, 1], 'o-', color='#1d3557', linewidth=1.8)
axes[0].set_title('① Iteration Path on Contour Map')

# ② کاهش تابع هدف
axes[1].semilogy(iters, scipy_history['f'], 'o-', color='#e76f51')
axes[1].axhline(y=3.0, color='#2d6a4f', linestyle='--')
axes[1].set_title('② Objective Decrease per Iteration')

# ③ نقض قیودها
axes[2].semilogy(iters, np.array(scipy_history['g1']) + 1e-16, 's-', color='#457b9d', label='|g₁|')
axes[2].semilogy(iters, np.array(scipy_history['g2']) + 1e-16, '^-', color='#e63946', label='|g₂|')
axes[2].set_title('③ Constraint Convergence to Zero')
axes[2].legend()

plt.tight_layout()
plt.savefig('plot2_convergence.png', dpi=120, bbox_inches='tight')
plt.show()
```

### پلات ۳ — مقایسه جامع سه سالور

```python
libs   = ['SciPy', 'GEKKO', 'CasADi']
colors = ['#e76f51', '#457b9d', '#2a9d8f']

devs = [np.linalg.norm(results[lib]['sol'] - np.array([1,1,1])) for lib in libs]
objs = [results[lib]['obj'] for lib in libs]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# ① مقدار f(x*) هر سالور
axes[0,0].bar(libs, objs, color=colors)
axes[0,0].axhline(y=3.0, color='#e63946', linestyle='--')
axes[0,0].set_title('① Objective Value at Optimum')

# ② انحراف از جواب تحلیلی
axes[0,1].bar(libs, devs, color=colors)
axes[0,1].set_yscale('log')
axes[0,1].set_title('② Deviation from Analytical Solution')

# ③ مقادیر x1, x2, x3
x_idx, width = np.arange(3), 0.22
for i, (lib, col) in enumerate(zip(libs, colors)):
    axes[1,0].bar(x_idx + i*width, results[lib]['sol'], width, label=lib, color=col)
axes[1,0].axhline(y=1.0, color='#e63946', linestyle='--')
axes[1,0].set_title('③ Solution Variables x1, x2, x3')
axes[1,0].legend()

# ④ جدول مشخصات کیفی
axes[1,1].axis('off')
# (جدول مشخصات در نوت‌بوک به‌صورت جدول رنگی نمایش داده می‌شود)

plt.tight_layout()
plt.savefig('plot3_comparison.png', dpi=120, bbox_inches='tight')
plt.show()
```

---

## 📊 جدول مقایسه نتایج

```python
import pandas as pd

rows = []
x_star = np.array([1.0, 1.0, 1.0])

for lib, data in results.items():
    sol = data['sol']
    rows.append({
        'کتابخانه' : lib,
        'x₁'       : round(float(sol[0]), 6),
        'x₂'       : round(float(sol[1]), 6),
        'x₃'       : round(float(sol[2]), 6),
        'f(x*)'    : round(float(data['obj']), 8),
        '‖x−x*‖'   : f"{np.linalg.norm(np.array([float(sol[0]), float(sol[1]), float(sol[2])]) - x_star):.2e}",
        'الگوریتم'  : data['solver'],
        'گرادیان'   : data['grad'],
    })

df = pd.DataFrame(rows)
print(df.to_string())
```

**خروجی نمونه:**

| #   | کتابخانه | x₁  | x₂  | x₃  | f(x\*) | ‖x−x\*‖ | الگوریتم         | گرادیان              |
| --- | -------- | --- | --- | --- | ------ | ------- | ---------------- | -------------------- |
| 1   | SciPy    | 1.0 | 1.0 | 1.0 | 3.0    | ~1e-10  | SLSQP            | Finite Difference    |
| 2   | GEKKO    | 1.0 | 1.0 | 1.0 | 3.0    | ~1e-11  | IPOPT (built-in) | Auto-Diff (internal) |
| 3   | CasADi   | 1.0 | 1.0 | 1.0 | 3.0    | ~1e-12  | IPOPT (built-in) | Exact AD             |

> 🎯 **جواب تحلیلی:** $x_1 = x_2 = x_3 = 1.0 \quad \Rightarrow \quad f^* = 3.0$ (از نامساوی AM-GM)

---

## 🏁 جمع‌بندی — مقایسه سه سالور NLP

### نتایج عددی

همه سه کتابخانه به جواب تحلیلی $x_1 = x_2 = x_3 = 1$، $f^* = 3$ رسیدند.

---

### تفاوت اصلی: روش محاسبه گرادیان

| سالور      | روش گرادیان       | دقت                    | توضیح                                                              |
| ---------- | ----------------- | ---------------------- | ------------------------------------------------------------------ |
| **SciPy**  | Finite Difference | تقریبی $O(h)$          | $\frac{\partial f}{\partial x_i} \approx \frac{f(x+he_i)-f(x)}{h}$ |
| **GEKKO**  | Auto-Diff (داخلی) | بالا                   | از گراف محاسباتی IPOPT                                             |
| **CasADi** | Exact Auto-Diff   | دقت ماشین ≈ $10^{-16}$ | Chain Rule روی گراف نمادین SX                                      |

---

### مراحل کلی حل هر NLP (مشترک بین هر سه سالور)

```
① تعریف f(x) — تابع هدف
② تعریف g(x) = 0 — قیود تساوی
③ x₀ — نقطه شروع اولیه
④ حل ← سالور (SLSQP یا IPOPT)
   ↳ محاسبه گرادیان ∇f و ژاکوبین ∇g
   ↳ حل زیرمسأله (QP یا barrier)
   ↳ به‌روزرسانی x ← x + αΔx
   ↳ بررسی شرایط KKT (Karush-Kuhn-Tucker)
⑤ خروجی: x* ، f(x*) ، ضرایب لاگرانژ λ
```

---

### راهنمای انتخاب

| سناریو شما                      | پیشنهاد    |
| ------------------------------- | ---------- |
| شروع سریع، بدون نصب اضافی       | **SciPy**  |
| کنترل بهینه، سیستم دینامیک، DAE | **GEKKO**  |
| رباتیک، MPC، گرادیان دقیق، C++  | **CasADi** |

> 💡 **قانون سرانگشتی:** مسأله کوچک؟ → SciPy. نیاز به دقت بالا یا مقیاس بزرگ؟ → CasADi.

---

## 📦 نصب پکیج‌ها

```bash
# SciPy (معمولاً از قبل نصب است)
pip install scipy numpy

# GEKKO
pip install gekko

# CasADi
pip install casadi

# برای تصویرسازی
pip install matplotlib pandas
```

---

## 📁 فایل‌های خروجی

| فایل                    | توضیح                                     |
| ----------------------- | ----------------------------------------- |
| `plot1_landscape.png`   | چشم‌انداز مسأله — Contour 2D و Surface 3D |
| `plot2_convergence.png` | مسیر همگرایی SLSQP در هر تکرار            |
| `plot3_comparison.png`  | مقایسه جامع سه سالور از نظر دقت و جواب    |

{% endraw %}
