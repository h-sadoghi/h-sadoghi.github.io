---
layout: legacy_page
title: رفتار غیرنرمال رانندگان اتوبوس
permalink: /resources/teaching-toolkit-abnormal/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: true
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/toolkit/Abnormal/
legacy_group: Research toolkit
legacy_dir: rtl
lang: fa
---

{% raw %}

# تشخیص رفتار غیرعادی راننده با استفاده از شبکه عصبی عمیق برروی کامپیوترهای کوچک

## چکیده

در این پژوهش، یک دوربین هوشمند با قابلیت یادگیری مفهوم و پردازش داخلی طراحی شده است که از یک بستر ارتباطی پرسرعت برخوردار است که هزینه انتقال تصاویر را به حداقل می رساند. در این دوربین از ساختار پردازش موازی بر روی دو پردازنده به صورت همزمان استفاده می شود. همچنین، با استفاده از الگوریتم طبقه‌بند افزایشی بر روی وزن‌های طبقه‌بندی برگرفته از هر دوربین، وزن‌های داخلی همه آنها در بازه‌های زمانی تعریف شده، به صورت برخط به‌روزرسانی می‌گردد.

## مقدمه

انگیزه طراحی و ساخت چنین سیستمی، ایجاد بستری هوشمند برای سیستم‌های نظارت تصویری و آنلاین است که بتواند بدون نیاز به حضور نیروی انسانی و به صورت مستمر و هوشمند، محیط را پردازش کند.

## سیستم پیشنهادی

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/1-3-flowchart-ed96cfe995-480.webp 480w, /assets/img/legacy/1-3-flowchart-ed96cfe995-800.webp 800w, /assets/img/legacy/1-3-flowchart-ed96cfe995-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/1-3-flowchart-ed96cfe995.jpg" alt="طرح‌واره روش زمان ورود"></picture>

</div>

<div class="caption" markdown="1">

طرح‌واره روش زمان ورود

</div>

### فلوچارت روش پیشنهادی

سیستم از دو بخش کلی تشکیل شده است:

- **بخش داخل خودرو**:
  - سخت افزار
  - الگوریتم تشخیص
- **سرور مرکزی (بخش خارجی خودرو)**:
  - رابط کاربری گرافیکی (GUI)
  - بانک اطلاعاتی

### روش پیشنهادی

اجزای اصلی سیستم:

1. ارائه ساختار و شکل ظاهری مناسب
2. سخت‌افزار مناسب شرایط محیطی
3. پردازش تصویر و سیستم یادگیر با دقت قابل قبول
4. پیاده‌سازی بستر مخابراتی
5. پایگاه‌داده برای ذخیره‌سازی
6. رابط گرافیکی برای تحلیل اطلاعات

<div markdown="1">

    <img loading="lazy" src="/assets/img/legacy/data-flow-diagram-261b82b8f0.webp" alt="OPT">

</div>

<div class="caption" markdown="1">

محاسبه پارامترهای بهینه

</div>

### تهیه سخت افزار

قطعات استفاده شده:

- برد Raspberry Pi 3
- برد Tinker Board
- دوربین ۸ مگاپیکسل دید در شب
- سنسورهای مادون قرمز
- مودم اینترنت همراه
- حافظه ۳۲ گیگابایتی

<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چیدمان ماتریسی تصاویر</title>
</head>
<body>

<div class="container" markdown="1">

        <h1>نمایش سخت افزار</h1>

<div class="image-grid" markdown="1">

<div class="image-item" markdown="1">

                <picture><source type="image/webp" srcset="/assets/img/legacy/2-3-inside1-c0652e3598-480.webp 480w, /assets/img/legacy/2-3-inside1-c0652e3598-800.webp 800w, /assets/img/legacy/2-3-inside1-c0652e3598-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/2-3-inside1-c0652e3598.jpg" alt="سخت افزار نمای 1"></picture>

<div class="caption" markdown="1">

سخت افزار نمای 1

</div>

</div>

<div class="image-item" markdown="1">

                <picture><source type="image/webp" srcset="/assets/img/legacy/3-3-inside2-6b945cdc77-480.webp 480w, /assets/img/legacy/3-3-inside2-6b945cdc77-800.webp 800w, /assets/img/legacy/3-3-inside2-6b945cdc77-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/3-3-inside2-6b945cdc77.jpg" alt="سخت افزار نمای 2"></picture>

<div class="caption" markdown="1">

سخت افزار نمای 2

</div>

</div>

</div>

</div>

</body>
</html>

### طراحی نرم افزاری و سرور

- سرور تحت وب با حافظه ۱۴ گیگابایت
- پایگاه‌داده PostgreSQL
- فریم‌ورک Pyramid برای رابط کاربری
- نرم‌افزار تحت وب گرافیکی

<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چیدمان ماتریسی تصاویر</title>
</head>
<body>

<div class="container" markdown="1">

        <h1>برخی صفحات طراحی شده</h1>

<div class="image-grid" markdown="1">

<div class="image-item" markdown="1">

                <picture><source type="image/webp" srcset="/assets/img/legacy/5-3-mainpage-e86d710f98-480.webp 480w, /assets/img/legacy/5-3-mainpage-e86d710f98-800.webp 800w, /assets/img/legacy/5-3-mainpage-e86d710f98-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/5-3-mainpage-e86d710f98.jpg" alt="سامانه هوشمند تشخیص تخلفات"></picture>

<div class="caption" markdown="1">

سامانه هوشمند تشخیص تخلفات

</div>

</div>

<div class="image-item" markdown="1">

                <picture><source type="image/webp" srcset="/assets/img/legacy/6-3-singleview-a86f4de8a9-480.webp 480w, /assets/img/legacy/6-3-singleview-a86f4de8a9-800.webp 800w, /assets/img/legacy/6-3-singleview-a86f4de8a9-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/6-3-singleview-a86f4de8a9.jpg" alt="مشخصات"></picture>

<div class="caption" markdown="1">

مشخصات

</div>

</div>

</div>

</div>

</body>
</html>

### الگوریتم تشخیص

کلاس‌های تشخیص:

- رفتار عادی
- استعمال دخانیات
- صحبت کردن با تلفن همراه
- ارسال پیامک

مراحل پردازش:

1. پیش‌پردازش تصویر
2. استخراج ویژگی‌ها
3. طبقه‌بندی
4. ارسال نتیجه

### شبکه عصبی مورد استفاده

شبکه‌های مورد بررسی:

- AlexNet (دقت ۶۱٪)
- MobileNet (دقت ۶۳٪)
- ResNet50 (دقت ۶۷٪)
- DenseNet (دقت ۷۱٪) - انتخاب نهایی

## ارزیابی سیستم

### مجموعه داده

داده‌های جمع‌آوری شده:

- کلاس عادی: ۱۴۰۵۰ تصویر
- استعمال دخانیات: ۱۱۷۳۰ تصویر
- صحبت با تلفن: ۱۱۷۳۵ تصویر
- ارسال پیامک: ۱۳۶۴۵ تصویر
- مجموع: ۵۱۱۶۰ تصویر

<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چیدمان ماتریسی تصاویر</title>
</head>
<body>

<div class="container" markdown="1">

        <h1>رفتار غیرنرمال</h1>

<div class="image-grid" markdown="1">

<div class="image-item" markdown="1">

                <picture><source type="image/webp" srcset="/assets/img/legacy/8-3-smoking-40820b9f03-480.webp 480w, /assets/img/legacy/8-3-smoking-40820b9f03-800.webp 800w, /assets/img/legacy/8-3-smoking-40820b9f03-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/8-3-smoking-40820b9f03.jpg" alt="abnorma1"></picture>

<div class="caption" markdown="1">

رفتار غیرنرمال سیگار کشیدن

</div>

</div>

<div class="image-item" markdown="1">

                <picture><source type="image/webp" srcset="/assets/img/legacy/10-3-texting-313aae14da-480.webp 480w, /assets/img/legacy/10-3-texting-313aae14da-800.webp 800w, /assets/img/legacy/10-3-texting-313aae14da-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/10-3-texting-313aae14da.jpg" alt="ab2"></picture>

<div class="caption" markdown="1">

رفتار غیرنرمال نگاه کردن به موبایل در حین رانندگی

</div>

</div>

</div>

</div>

</body>
</html>

### نتایج

- دقت کلی سیستم: ۶۹٪
- دقت در داده‌های روز: ۷۱٪
- دقت در داده‌های شب: ۶۷٪
- بهبود دقت با روش افزایشی: به ۷۳٪

<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>چیدمان ماتریسی تصاویر</title>
</head>
<body>

<div class="container" markdown="1">

        <h1>رفتار</h1>

<div class="image-grid" markdown="1">

<div class="image-item" markdown="1">

                <picture><source type="image/webp" srcset="/assets/img/legacy/7-3-normal-034d493d93-480.webp 480w, /assets/img/legacy/7-3-normal-034d493d93-800.webp 800w, /assets/img/legacy/7-3-normal-034d493d93-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/7-3-normal-034d493d93.jpg" alt="abnorma1"></picture>

<div class="caption" markdown="1">

رفتار نرمال

</div>

</div>

<div class="image-item" markdown="1">

                <picture><source type="image/webp" srcset="/assets/img/legacy/9-3-phonecall-ba12ff8658-480.webp 480w, /assets/img/legacy/9-3-phonecall-ba12ff8658-800.webp 800w, /assets/img/legacy/9-3-phonecall-ba12ff8658-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/9-3-phonecall-ba12ff8658.jpg" alt="ab2"></picture>

<div class="caption" markdown="1">

رفتار غیرنرمال مکالمه با موبایل در حین رانندگی

</div>

</div>

</div>

</div>

</body>
</html>

## نتیجه‌گیری

سیستم طراحی شده توانست با موفقیت پیاده‌سازی شود و چالش‌های محیط واقعی را حل کند. این سیستم قابلیت توسعه برای کاربردهای دیگر مانند تشخیص سرقت و نظارت بر بیماران را دارد.

```mermaid
graph TD
    A[دوربین هوشمند] --> B[پردازش موازی]
    B --> C[تشخیص رفتار]
    C --> D[ارسال نتایج]
    D --> E[سرور مرکزی]
    E --> F[ذخیره در پایگاه داده]
    F --> G[نمایش در رابط کاربری]
```

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/flowchart-0cd29aabfa-480.webp 480w, /assets/img/legacy/flowchart-0cd29aabfa-800.webp 800w, /assets/img/legacy/flowchart-0cd29aabfa-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/flowchart-0cd29aabfa.jpg" alt="OPT"></picture>

</div>

<div class="caption" markdown="1">

فلوچارت

</div>

## جزییات بیشتر در پایان نامه سید محمد حسینی کارشناسی ارشد از دانشگاه فردوسی مشهد

{% endraw %}
