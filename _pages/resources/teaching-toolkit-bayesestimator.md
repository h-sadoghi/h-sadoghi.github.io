---
layout: legacy_page
title: تخمین گر بیز- تابع ضرر مربعات
permalink: /resources/teaching-toolkit-bayesestimator/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/toolkit/BayesianEstimator/
legacy_group: Research toolkit
legacy_dir: rtl
lang: fa
---

{% raw %}
**مولف-دکتر علیرضا مهرابی**

## صورت مسئله

می‌خواهیم نسبت زیر را محاسبه کنیم:

$$
\frac{
\int_{-\infty}^{\infty} \mu \, f(\mu \mid x_1,x_2,\dots,x_N)\, d\mu
}{
\int_{-\infty}^{\infty} f(\mu \mid x_1,x_2,\dots,x_N)\, d\mu
}
$$

فرض می‌کنیم:

$$
\mu \sim \mathcal{N}(\mu_0,\sigma_0^2)
$$

و داده‌ها مستقل بوده و

$$
x_i = \mu + \eta
$$

که در آن

$$
\eta \sim \mathcal{N}(0,\sigma_n^2)
$$

در نتیجه

$$
x_i \mid \mu \sim \mathcal{N}(\mu,\sigma_n^2)
$$

---

# محاسبه انتگرال صورت

داریم

$$
A =
\int_{-\infty}^{\infty}
\mu
\frac{1}{(\sqrt{2\pi}\sigma_n)^N}
e^{-\frac{\sum_{i=1}^N(\mu-x_i)^2}{2\sigma_n^2}}
\frac{1}{\sqrt{2\pi}\sigma_0}
e^{-\frac{(\mu-\mu_0)^2}{2\sigma_0^2}}
d\mu
$$

ابتدا ثابت‌ها را خارج می‌کنیم:

$$
A =
\frac{1}{(\sqrt{2\pi}\sigma_n)^N \sqrt{2\pi}\sigma_0}
\int_{-\infty}^{\infty}
\mu
\exp\left(
-\frac{\sum_{i=1}^N(\mu-x_i)^2}{2\sigma_n^2}
-\frac{(\mu-\mu_0)^2}{2\sigma_0^2}
\right)
d\mu
$$

---

## بسط مجموع مربعات

$$
\sum_{i=1}^N (\mu-x_i)^2
=
\sum_{i=1}^N (\mu^2 - 2\mu x_i + x_i^2)
=
N\mu^2 - 2\mu \sum x_i + \sum x_i^2
$$

جایگذاری:

$$
A =
\gamma
\int
\mu
\exp\left(
-\alpha \mu^2 + \beta \mu - \text{const}
\right)
d\mu
$$

---

## تعریف ضرایب

تعریف می‌کنیم

$$
\gamma =
\frac{1}{(\sqrt{2\pi}\sigma_n)^N \sqrt{2\pi}\sigma_0}
\exp\left(
-\frac{\sigma_0^2\sum x_i^2 + \sigma_n^2\mu_0^2}{2\sigma_n^2\sigma_0^2}
\right)
$$

$$
\alpha =
\frac{1}{2}
\left(
\frac{N}{\sigma_n^2} + \frac{1}{\sigma_0^2}
\right)
$$

$$
\beta =
\frac{\sum x_i}{\sigma_n^2} + \frac{\mu_0}{\sigma_0^2}
$$

پس

$$
A =
\gamma
\int_{-\infty}^{\infty}
\mu e^{-\alpha \mu^2 + \beta \mu} d\mu
$$

---

# کامل کردن مربع

$$
-\alpha \mu^2 + \beta \mu
=
-\alpha
\left(
\mu^2 - \frac{\beta}{\alpha}\mu
\right)
$$

$$
=
-\alpha
\left(
(\mu-\frac{\beta}{2\alpha})^2 - \frac{\beta^2}{4\alpha^2}
\right)
$$

$$
=
-\alpha(\mu-\frac{\beta}{2\alpha})^2 + \frac{\beta^2}{4\alpha}
$$

پس

$$
A =
\gamma e^{\frac{\beta^2}{4\alpha}}
\int
\mu
e^{-\alpha(\mu-\frac{\beta}{2\alpha})^2}
d\mu
$$

---

# تغییر متغیر

$$
u = \mu - \frac{\beta}{2\alpha}
$$

$$
\mu = u + \frac{\beta}{2\alpha}
$$

جایگذاری:

$$
A =
\gamma e^{\frac{\beta^2}{4\alpha}}
\int
\left(u + \frac{\beta}{2\alpha}\right)
e^{-\alpha u^2} du
$$

---

# تجزیه انتگرال

$$
A =
\gamma e^{\frac{\beta^2}{4\alpha}}
\left[
\int u e^{-\alpha u^2} du
+
\frac{\beta}{2\alpha}
\int e^{-\alpha u^2} du
\right]
$$

تابع اول فرد است:

$$
\int_{-\infty}^{\infty} u e^{-\alpha u^2} du = 0
$$

پس

$$
A =
\gamma e^{\frac{\beta^2}{4\alpha}}
\frac{\beta}{2\alpha}
\int_{-\infty}^{\infty} e^{-\alpha u^2} du
$$

---

# انتگرال گاوسی

می‌دانیم:

$$
\int_{-\infty}^{\infty} e^{-\alpha u^2} du
=
\sqrt{\frac{\pi}{\alpha}}
$$

پس

$$
A =
\gamma e^{\frac{\beta^2}{4\alpha}}
\frac{\beta}{2\alpha}
\sqrt{\frac{\pi}{\alpha}}
$$

---

# محاسبه مخرج

مشابه قبل:

$$
C =
\gamma e^{\frac{\beta^2}{4\alpha}}
\int_{-\infty}^{\infty} e^{-\alpha u^2} du
$$

$$
C =
\gamma e^{\frac{\beta^2}{4\alpha}}
\sqrt{\frac{\pi}{\alpha}}
$$

---

# نسبت نهایی

$$
\frac{A}{C}
=
\frac{
\gamma e^{\frac{\beta^2}{4\alpha}}
\frac{\beta}{2\alpha}
\sqrt{\frac{\pi}{\alpha}}
}{
\gamma e^{\frac{\beta^2}{4\alpha}}
\sqrt{\frac{\pi}{\alpha}}
}
$$

ساده‌سازی:

$$
\boxed{
\frac{A}{C}
=
\frac{\beta}{2\alpha}
}
$$

---

# جایگذاری ضرایب

$$
\frac{A}{C}
=
\frac{
\frac{\sum x_i}{\sigma_n^2} + \frac{\mu_0}{\sigma_0^2}
}{
\frac{N}{\sigma_n^2} + \frac{1}{\sigma_0^2}
}
$$

---

# فرم نهایی ساده

اگر

$$
\bar{x} = \frac1N \sum x_i
$$

آنگاه

$$
\boxed{
\frac{A}{C}
=
\frac{
\frac{N}{\sigma_n^2}\bar{x} + \frac{1}{\sigma_0^2}\mu_0
}{
\frac{N}{\sigma_n^2} + \frac{1}{\sigma_0^2}
}
}
$$

---

# نتیجه

این مقدار دقیقاً میانگین توزیع پسین است:

$$
\frac{A}{C} = \mathbb{E}[\mu \mid x]
$$

---

# تحلیل‌های علمی تکمیلی و تفسیر آماری

در این بخش، نتایج به‌دست‌آمده را از دیدگاه بیزی، آماری و یادگیری ماشین تفسیر می‌کنیم تا درک عمیق‌تری از فرمول نهایی حاصل شود.

---

# ۱) بازنویسی تخمین پسین به صورت ترکیب وزن‌دار (Shrinkage Form)

میانگین پسین را به دست آوردیم:

$$
\mathbb{E}[\mu \mid x]
=
\frac{\frac{N}{\sigma_n^2}\bar{x} + \frac{1}{\sigma_0^2}\mu_0}
{\frac{N}{\sigma_n^2} + \frac{1}{\sigma_0^2}}
$$

این رابطه را می‌توان به شکل زیر نوشت:

$$
\mathbb{E}[\mu \mid x]
=
w\,\bar{x} + (1-w)\mu_0
$$

که در آن

$$
w =
\frac{N\sigma_0^2}{N\sigma_0^2 + \sigma_n^2}
$$

---

## تفسیر

- اگر داده‌ها زیاد باشند → وزن داده‌ها بیشتر می‌شود
- اگر نویز زیاد باشد → وزن پیشین بیشتر می‌شود

بنابراین:

> تخمین بیزی میانگین، ترکیبی وزن‌دار از «میانگین نمونه» و «اطلاعات پیشین» است.

این نوع تخمین در آمار با نام

**Shrinkage Estimator**

شناخته می‌شود.

---

# ۲) بررسی حالات حدی (Limiting Cases)

بررسی رفتار فرمول در شرایط مرزی، صحت فیزیکی و آماری آن را تأیید می‌کند.

---

## حالت اول — تعداد داده زیاد

$$
N \to \infty
$$

آنگاه

$$
w \to 1
\quad \Rightarrow \quad
\mathbb{E}[\mu|x] \to \bar{x}
$$

یعنی پیشین بی‌اثر می‌شود.

این نتیجه مطابق **قانون اعداد بزرگ** است.

---

## حالت دوم — نویز بسیار زیاد

$$
\sigma_n^2 \to \infty
$$

$$
w \to 0
\quad \Rightarrow \quad
\mathbb{E}[\mu|x] \to \mu_0
$$

یعنی داده‌ها غیرقابل اعتماد شده و تخمین فقط بر اساس prior انجام می‌شود.

---

## حالت سوم — پیشین ضعیف (Non-informative prior)

$$
\sigma_0^2 \to \infty
$$

$$
\mathbb{E}[\mu|x] = \bar{x}
$$

که دقیقاً همان تخمین کلاسیک **Maximum Likelihood (MLE)** است.

---

# ۳) توزیع کامل پسین (نه فقط میانگین)

توزیع پسین همچنان گاوسی است:

$$
p(\mu|x) = \mathcal{N}(\mu_{\text{post}}, \sigma_{\text{post}}^2)
$$

---

## واریانس پسین

$$
\sigma_{\text{post}}^2
=
\left(
\frac{N}{\sigma_n^2} + \frac{1}{\sigma_0^2}
\right)^{-1}
$$

---

## تفسیر

- با افزایش تعداد داده‌ها → واریانس کاهش می‌یابد
- عدم قطعیت تقریباً متناسب با $1/N$ کاهش می‌یابد

یعنی:

> هرچه داده بیشتر، اطمینان آماری بیشتر

---

# ۴) فرم بهینه‌سازی معادل (دیدگاه Regularization)

بیشینه‌سازی پسین معادل کمینه‌سازی عبارت زیر است:

$$
\sum_{i=1}^N (x_i-\mu)^2
+
\lambda (\mu-\mu_0)^2
$$

که در آن

$$
\lambda = \frac{\sigma_n^2}{\sigma_0^2}
$$

---

## نتیجه مهم

این دقیقاً همان:

- Ridge Regression
- L2 Regularization
- Tikhonov Regularization

است.

بنابراین:

> Gaussian prior ⇔ L2 penalty

این ارتباط یکی از اصول بنیادی یادگیری ماشین بیزی است.

---

# ۵) بازنویسی با مفهوم Precision

تعریف می‌کنیم:

$$
\tau = \frac{1}{\sigma^2}
$$

که به آن **Precision (دقت آماری)** می‌گویند.

---

## میانگین پسین

$$
\mu_{\text{post}}
=
\frac{\tau_n N \bar{x} + \tau_0 \mu_0}
{\tau_n N + \tau_0}
$$

---

## واریانس پسین

$$
\tau_{\text{post}} = \tau_n N + \tau_0
$$

---

## تفسیر مهم

$$
\text{posterior precision}
=
\text{prior precision}
+
\text{data precision}
$$

یعنی:

> اطلاعات آماری جمع می‌شود.

این ویژگی پایهٔ نظری بسیاری از الگوریتم‌های بیزی است.

---

# ۶) ارتباط با مدل‌های پیشرفته‌تر

همین نتیجهٔ ساده، پایهٔ ریاضی بسیاری از روش‌های پیشرفته است:

- Bayesian Linear Regression
- Kalman Filter
- MAP Estimation
- Gaussian Processes

در واقع:

> مسئلهٔ حاضر ساده‌ترین نمونهٔ استنتاج بیزی پیوسته است.

---

# جمع‌بندی

نتیجهٔ اصلی ما:

$$
\mathbb{E}[\mu|x]
=
w\bar{x} + (1-w)\mu_0
$$

نشان می‌دهد که تخمین بیزی:

- داده و پیشین را ترکیب می‌کند
- دارای regularization طبیعی است
- عدم قطعیت را کمی‌سازی می‌کند
- و تعمیم مستقیم به مدل‌های پیچیده‌تر دارد

بنابراین این چارچوب از نظر آماری و یادگیری ماشین بسیار قدرتمندتر از تخمین کلاسیک میانگین است.
{% endraw %}
