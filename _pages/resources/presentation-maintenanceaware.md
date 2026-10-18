---
layout: legacy_page
title: سیستم تعمیر-آگاه
permalink: /resources/presentation-maintenanceaware/
description: Research presentation and project archive
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/presentation/MaintenanceAware/
legacy_group: Presentations and proposals
legacy_dir: rtl
lang: fa
---

{% raw %}

## تعمیر آگاه چیست

با افزایش روزافزون پیچیدگی و مقیاس شبکه‌های برق مدرن، تأمین انرژی الکتریکی قابل اعتماد و پایدار به یکی از چالش‌های اصلی صنعت برق تبدیل شده است. در این میان، سیستم‌های توزیع به عنوان حلقه واسط بین تولید و مصرف، نقشی حیاتی ایفا می‌کنند و قابلیت اطمینان آن‌ها مستقیماً به کیفیت و به‌موقع بودن فعالیت‌های نگهداری و تعمیرات وابسته است. به این منظور نیاز به **سیستم های تعمیر آگاه** است.

این سیستم دایما خودش را پایش می کند و با ابزار مختلف از وضعیت خود با خبر می شود سپس توسط ابزار هوشمند برای دوقلوی دیجیتالی که از خود بوجود اورده به آگاهی دادن برای تعمیرات پیش بینانه اقدام می کند.

<a href="https://www.aurecongroup.com/projects/national-grid-uk" target="_blank"><strong>پلتفرم یکپارچه نگهداری و تعمیرات پیش‌بینانه (Predictive Maintenance)</strong></a> برای دارایی‌های شبکه توزیع برق با استفاده از هوش مصنوعی، اینترنت اشیاء (IoT) و فناوری دوقلوی دیجیتال (Digital Twin) این پروژه یک گام فراتر از نگهداری و تعمیرات سنتی است. به جای تعمیرات بر اساس یک برنامه زمانی ثابت (مثلاً هر ۶ ماه یکبار)، این سیستم بر اساس وضعیت واقعی و لحظه‌ای تجهیزات، زمان و نوع نیاز به تعمیر را پیش‌بینی می‌کند. این
<a href="https://www.aurecongroup.com/-/media/files/downloads-library/thought-leadership/aurecon-our-digital-futures-your-digital-decisions-report.pdf" target="_blank"><strong>گزارش</strong></a> را هم ببینید.

چنانچه دوقلوی دیجیتالی برای منظور تعمیر و نگه داری مشابه دوقلوی دیجیتال شبکه برق ایران داشته باشیم طبعا پیش بینی و حتی مکانیز "چی می شد اگر" نیز مقدور می شد.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/whatif-tehran-mashhad-d7c55a7f64-480.webp 480w, /assets/img/legacy/whatif-tehran-mashhad-d7c55a7f64-800.webp 800w, /assets/img/legacy/whatif-tehran-mashhad-d7c55a7f64-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/whatif-tehran-mashhad-d7c55a7f64.jpg" alt="RAG1"></picture>

</div>

<div class="caption" markdown="1">

دوقلوی دیجیتال شبکه برق ملی ایران

</div>

## اجزای اصلی پروژه پیش بینانه:

### لایه جمع‌آوری داده (Data Layer - IoT):

**سنسورهای هوشمند:** نصب سنسورهای اینترنت اشیاء (IoT) بر روی دارایی‌های حیاتی شبکه توزیع مانند ترانسفورماتورها، کلیدهای قدرت، فیدرها و پایه‌ها. این سنسورها داده‌هایی مانند دما، رطوبت، ارتعاشات، جریان بار و گازهای محلول در روغن ترانس (DGA) را به صورت لحظه‌ای ارسال می‌کنند.
پهپادها و ربات‌ها: استفاده از پهپادهای مجهز به دوربین‌های با وضوح بالا، حرارتی (Thermal) و LiDAR برای بازرسی منظم و خودکار خطوط، شناسایی خوردگی، شکستگی عایق‌ها و رشد بیش از حد گیاهان در نزدیکی خطوط (Vegetation Management).
**داده‌های هواشناسی:** یکپارچه‌سازی داده‌های پیش‌بینی آب و هوا (طوفان، رعد و برق، یخبندان) برای ارزیابی ریسک‌های احتمالی.

### لایه پردازش و مدل‌سازی (Processing & Modeling Layer - Digital Twin):

**ایجاد دوقلوی دیجیتال**: ساخت یک نسخه مجازی و پویا از کل شبکه توزیع (یا بخشی از آن). این مدل دیجیتال، تمام داده‌های دریافتی از سنسورها و پهپادها را در خود منعکس می‌کند. برای توضیح بیشتر این متن را مطالعه کنید

<a href="/resources/presentation-humandt/" target="_blank"><strong>کلیک کنید</strong></a>

**شبیه‌سازی**: با استفاده از این دوقلوی دیجیتال، مدیران شبکه می‌توان سناریوهای مختلف را شبیه‌سازی کنند. برای مثال: "اگر یک طوفان شدید در منطقه X رخ دهد، کدام بخش از شبکه آسیب‌پذیرترین خواهد بود؟" یا "اثر خروج یک ترانسفورماتور مشخص بر شبکه چیست؟".

### لایه تحلیل و هوش مصنوعی (AI & Analytics Layer):

**الگوریتم‌های یادگیری ماشین (Machine Learning)**: این مغز متفکر سیستم است. الگوریتم‌های هوش مصنوعی، داده‌های تاریخی و لحظه‌ای را تحلیل می‌کنند تا الگوهای نامعقول و نشانه‌های اولیه خرابی را شناسایی کنند.
**پیش‌بینی خرابی:** سیستم می‌تواند با دقت بالایی پیش‌بینی کند که کدام ترانسفورماتور در ۳ ماه آینده دچار نقص فنی خواهد شد یا کدام بخش از عایق‌ها در حال تخریب هستند. این پیش‌بینی‌ها با اولویت‌بندی (مثلاً از بحرانی تا کم‌اهمیت) به تیم نگهداری اعلام می‌شود.

## لایه اجرا و مدیریت (Execution & Management Layer):

**ایجاد خودکار دستور کار (Work Order)**: سیستم به صورت خودکار یک دستور کار دقیق برای تیم تعمیرات صادر می‌کند. این دستور کار شامل مشخصات دقیق مشکل، مکان دارایی روی نقشه، و تاریخ پیشنهادی برای تعمیر است.
**بهینه‌سازی مسیر**: سیستم با توجه به موقعیت تیم‌های تعمیراتی و ترافیک، بهینه‌ترین مسیر برای رسیدن به محل را پیشنهاد می‌دهد.
راهنمایی تعمیرات با واقعیت افزوده (AR): تکنسین‌های تعمیرات می‌توانند با استفاده از عینک‌های هوشمند یا تبلت، اطلاعات دیجیتال (مانند دیاگرام‌ها، دستورالعمل‌ها و داده‌های سنسور) را روی دنیای واقعی و روی خود تجهیزات مشاهده کنند.

## مثال‌های واقعی و پروژه‌های در دست اجرا در دنیا:

این مفهوم دیگر یک ایده تئوریک نیست و شرکت‌های برق بزرگ در سراسر جهان در حال پیاده‌سازی آن هستند:

<a href="https://www.nationalgrid.com/electricity-transmission/national-grid-play-key-role-new-drone-infrastructure-inspection-policy" target="_blank"><strong>شرکت National Grid (بریتانیا و آمریکا):
</strong></a>

روش کار برای بازرسی خطوط برق، بهره‌گیری از فناوری پهپادهای مجهز به دوربین‌های با وضوح بالا است که قابلیت پرواز «فراتر از خط دید» را دارند. این رویکرد نوین، که با مشارکت شرکت‌هایی مانند National Grid و همکاری مراجع قانونی مانند سازمان هوانوردی بریتانیا توسعه یافته، امکان بازرسی ایمن، سریع و دقیق دکل‌ها و خطوط انتقال نیرو را از راه دور و حتی از یک اتاق کنترل مرکزی فراهم می‌کند. این روش نه تنها هزینه‌ها و زمان عملیات را کاهش می‌دهد، بلکه با حذف نیاز به صعود فیزیکی کارکنان به دکل‌ها برای بازدید بصری، سطح ایمنی نیروی متخصص را به طور چشمگیری افزایش می‌دهد و آن‌ها را برای تمرکز بر وظایف تخصصی‌تر و تعمیرات آماده می‌سازد.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/powerlinesurveillance-5b1e508f5f-480.webp 480w, /assets/img/legacy/powerlinesurveillance-5b1e508f5f-800.webp 800w, /assets/img/legacy/powerlinesurveillance-5b1e508f5f-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/powerlinesurveillance-5b1e508f5f.jpg" alt="RAG1"></picture>

</div>

<div class="caption" markdown="1">

پایش خطوط با پهپاد

</div>

این شرکت به طور گسترده از پهپادها و تحلیل داده‌های مبتنی بر هوش مصنوعی برای مدیریت پوشش گیاهی (Vegetation Management) استفاده می‌کند. پهپادها با اسکن LiDAR، نقشه سه‌بعدی دقیقی از خطوط و درختان اطراف ایجاد می‌کنند و هوش مصنوعی خطر برخورد درختان با خطوط را در آینده نزدیک پیش‌بینی می‌کند. این کار از قطعی‌های ناشی از این علت که یکی از دلایل اصلی خاموشی‌هاست، جلوگیری می‌کند.

### نمونه کار آزمایشگاه الگو دانشگاه فردوسی مشهد

پایش بر اساس تصاویر ماهواره

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-12-14-12-36-22-fcab103207-480.webp 480w, /assets/img/legacy/photo-2025-12-14-12-36-22-fcab103207-800.webp 800w, /assets/img/legacy/photo-2025-12-14-12-36-22-fcab103207-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-12-14-12-36-22-fcab103207.jpg" alt="powerline1"></picture>

</div>

<div class="caption" markdown="1">

پایش خطوط با تصاویر ماهواره

</div>

مسیرهای تصاویر اخذ شده در شکل زیر آمده است

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-12-14-12-35-52-c88e001948-480.webp 480w, /assets/img/legacy/photo-2025-12-14-12-35-52-c88e001948-800.webp 800w, /assets/img/legacy/photo-2025-12-14-12-35-52-c88e001948-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-12-14-12-35-52-c88e001948.jpg" alt="powerline1"></picture>

</div>

<div class="caption" markdown="1">

دکلهای فشار قوی اخذ شده

</div>

نمونه از خروجی برنامه روی نقشه را می توان اینجا مشاهده کرد

  <a href="https://hadisadoghiyazdi1971.github.io/presentation/extended_power_towers_map.html" target="_blank">
      <strong>کلیک کنید</strong>
  </a>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/electricitypylone-dcf48d13b7-480.webp 480w, /assets/img/legacy/electricitypylone-dcf48d13b7-800.webp 800w, /assets/img/legacy/electricitypylone-dcf48d13b7-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/electricitypylone-dcf48d13b7.jpg" alt="powerline1"></picture>

</div>

<div class="caption" markdown="1">

دکلهای فشار قوی قله زو

</div>

{% endraw %}
