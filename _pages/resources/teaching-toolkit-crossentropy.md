---
layout: legacy_page
title: Cross-Entropy
permalink: /resources/teaching-toolkit-crossentropy/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/toolkit/CrossEntropy/
legacy_group: Research toolkit
legacy_dir: rtl
lang: fa
---

{% raw %}

# به‌روزرسانی پارامترهای نرون سیگمویدی با Cross-Entropy

مدل نرون:

$$
\hat y = g(z) = \sigma(z) = \sigma(w^T x + b)
$$

که در آن:

- $x$ بردار ویژگی‌ها
- $w$ وزن‌ها
- $b$ بایاس
- $z = w^T x + b$
- $\sigma(z) = \frac{1}{1+e^{-z}}$

مسئله: طبقه‌بندی دودویی

---

# تابع ضرر Cross-Entropy دودویی

برای یک نمونه با برچسب واقعی $y \in \{0,1\}$:

$$
L = -\big[y \log(\hat y) + (1-y)\log(1-\hat y)\big]
$$

---

# هدف یادگیری

$$
\min_{w,b} L
$$

با گرادیان کاهشی:

$$
w \leftarrow w - \eta \frac{\partial L}{\partial w}
$$

$$
b \leftarrow b - \eta \frac{\partial L}{\partial b}
$$

---

# محاسبه گرادیان — مرحله به مرحله

## مشتق loss نسبت به خروجی

$$
\frac{\partial L}{\partial \hat y}
=
-\left(\frac{y}{\hat y} - \frac{1-y}{1-\hat y}\right)
$$

---

## مشتق سیگموید

$$
\frac{d\sigma}{dz} = \sigma(z)(1-\sigma(z)) = \hat y(1-\hat y)
$$

---

## نتیجه مهم (ساده‌سازی بزرگ)

با قاعده زنجیره:

$$
\frac{\partial L}{\partial z}
=
\hat y - y
$$

این ساده شدن دلیل اصلی استفاده Cross-Entropy با سیگموید است.

---

# گرادیان نسبت به وزن‌ها

چون:

$$
z = w^T x + b
$$

داریم:

$$
\frac{\partial z}{\partial w} = x
$$

پس:

$$
\frac{\partial L}{\partial w}
=
(\hat y - y) x
$$

---

# گرادیان نسبت به بایاس

$$
\frac{\partial L}{\partial b}
=
\hat y - y
$$

---

# قانون به‌روزرسانی پارامترها

## وزن‌ها:

$$
w \leftarrow w - \eta (\hat y - y)x
$$

## بایاس:

$$
b \leftarrow b - \eta (\hat y - y)
$$

---

# تفسیر شهودی

ترم خطا:

$$
(\hat y - y)
$$

- اگر $\hat y > y$ → بیش‌برآورد → وزن‌ها کاهش
- اگر $\hat y < y$ → کم‌برآورد → وزن‌ها افزایش

---

# فرم برداری برای یک Batch

اگر $X$ ماتریس داده باشد:

$$
\nabla_w L = X^T(\hat y - y)
$$

# استفاده از Cross-Entropy در شبکه‌های عصبی عمیق

در شبکه‌های عصبی عمیق، Cross-Entropy پرکاربردترین تابع ضرر برای **مسائل طبقه‌بندی** است.  
ایده همان است که قبلاً در نرون سیگمویدی دیدید — فقط اکنون خروجی از چندین لایه عبور می‌کند و گرادیان با **Backpropagation** به همه لایه‌ها منتقل می‌شود.

---

# ساختار کلی شبکه

$$
x → Layers → z^{(L)} → g(z^{(L)}) → \hat y
$$

- $z^{(L)}$ خروجی خطی لایه آخر
- $g$ تابع فعال‌سازی خروجی
- $\hat y$ پیش‌بینی احتمالاتی

---

# انتخاب تابع خروجی + Cross-Entropy

## ✅ طبقه‌بندی دودویی

خروجی: **Sigmoid**

$$
\hat y = \sigma(z)
$$

Cross-Entropy دودویی:

$$
L = - [ y \log(\hat y) + (1-y)\log(1-\hat y) ]
$$

---

## ✅ طبقه‌بندی چندکلاسه

خروجی: **Softmax**

$$
\hat y_i = \frac{e^{z_i}}{\sum_j e^{z_j}}
$$

Cross-Entropy چندکلاسه:

$$
L = - \sum_i y_i \log(\hat y_i)
$$

(برچسب‌ها معمولاً one-hot هستند)

---

# خاصیت طلایی Softmax + Cross-Entropy

اگر Softmax و Cross-Entropy با هم استفاده شوند:

## گرادیان بسیار ساده می‌شود:

$$
\frac{\partial L}{\partial z_i} = \hat y_i - y_i
$$

👉 این همان ساده‌شدنی است که در سیگموید هم دیدیم.

---

# روند آموزش در شبکه عمیق

# پیاده‌سازی در کتابخانه‌ها

## PyTorch

```python
loss = torch.nn.CrossEntropyLoss()
```

TensorFlow / Keras
loss = tf.keras.losses.CategoricalCrossentropy(from_logits=True)

خلاصه تصویری جریان گرادیان
Softmax + CrossEntropy
↓
delta = y_hat − y
↓
Backprop در کل شبکه
↓
به‌روزرسانی همه وزن‌ها
{% endraw %}
