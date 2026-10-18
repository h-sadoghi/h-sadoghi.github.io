---
layout: legacy_page
title: رسم شماتیک مدار
permalink: /resources/teaching-circuiteffort-circuit-schematic-drawing-project/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/circuiteffort/Circuit_Schematic_Drawing_Project/
legacy_group: Circuits and electronics
legacy_dir: rtl
lang: fa
---

{% raw %}

# رسم شماتیک مدار

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/myphoto-7dc33b21ab-480.webp 480w, /assets/img/legacy/myphoto-7dc33b21ab-800.webp 800w, /assets/img/legacy/myphoto-7dc33b21ab-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/myphoto-7dc33b21ab.jpg" alt="_figure1 : Hossein Jahanbanifar_"></picture>

</div>

<div class="caption" markdown="1">

    _figure1 : Hossein Jahanbanifar_

</div>

## فهرست مطالب

<!-- prettier-ignore -->
* TOC
{:toc}

## اطلاعات نویسنده

**نام :** حسین جهانبانی فر

**وابستگی:** گروه مهندسی کامپیوتر، دانشگاه فردوسی مشهد

## مقدمه

در حوزه مهندسی برق و الکترونیک، ترسیم شماتیک مدارها یکی از مراحل بسیار مهم در طراحی و پیاده‌سازی سیستم‌های الکتریکی محسوب می‌شود. شماتیک مدار، نمایش گرافیکی اجزای یک مدار به همراه اتصالات آن‌ها است که با استفاده از نمادهای استاندارد، روابط الکتریکی را به صورت دقیق و قابل فهم بیان می‌کند. این مرحله نه تنها برای مستندسازی پروژه‌های مهندسی ضروری است، بلکه به مهندسان و تکنسین‌ها کمک می‌کند تا پیش از ساخت اجزای فیزیکی مدار، منطق عملکرد و ایرادات احتمالی را شناسایی کنند.

هدف این پروژه، آشنایی با نرم‌افزارهای استاندارد ترسیم شماتیک (مانند Proteus، Altium Designer، OrCAD و KiCad) و کسب مهارت در استفاده صحیح از ابزارهای آن‌ها برای طراحی مدارهای الکترونیکی است.

در نهایت در طول پروژه یکی از نرم افزاری های معرفی شده برای رسم را انتخاب کرده و با محیط کاری آن و شیوه رسم اصولی یک مدار الکتریکی آشنا خواهیم شد.

## انواع نرم افزار ها برای رسم شماتیک

در حوزه طراحی مدارهای الکتریکی، انتخاب نرم‌افزار مناسب نقش مهمی در کیفیت و سرعت کار ایفا می‌کند. چهار نرم‌افزار اصلی که در این زمینه بیشترین استفاده را دارند، شامل Proteus Design Suite، Altium Designer، OrCAD (Cadence) و KiCad هستند.

در ادامه، این نرم‌افزارها براساس شاخص‌هایی همچون کاربرپسندی محیط نرم‌افزار، قدرت و دقت کتابخانه قطعات، توانایی شبیه‌سازی مدار، قابلیت طراحی PCB، و دسترس‌پذیری مورد بررسی قرار می‌گیرند.

### نرم افزار Proteus Design Suite

پروتئوس (Proteus Design Suite) محصول شرکت Labcenter Electronics است که نخستین نسخهٔ آن در دههٔ ۱۹۹۰ عرضه شد. این نرم‌افزار ترکیبی از طراحی شماتیک، شبیه‌سازی مدار و طراحی PCB را در محیطی یکپارچه ارائه می‌دهد. محیط کاربری آن گرافیکی و نسبتاً کاربرپسند است؛ منوها و پنل‌ها به گونه‌ای چیده شده‌اند که دسترسی سریع به ابزارها را فراهم می کنند. کتابخانه قطعات آن بسیار گسترده و دقیق است و شامل مدل‌های شبیه‌سازی برای میکروکنترلرها و آی‌سی‌های مختلف می‌شود. قدرت شبیه‌سازی پروتئوس در اجرای کدهای واقعی میکروکنترلرها بر روی مدار و مشاهدهٔ رفتار فیزیکی-منطقی بسیار مورد توجه واقع شده. طراحی PCB نیز با ابزارهای داخلی و معیارهای صنعتی انجام می‌شود. این نرم‌افزار تجاری است و نسخه کامل آن نیاز به لایسنس دارد، ولی نسخه آزمایشی محدود آن نیز موجود است.

### نرم افزار Altium Designer

التیوم دیزاینر محصول شرکت Altium Limited است که نخستین بار به‌عنوان Protel در دههٔ ۱۹۸۰ عرضه شد و بعدها نام آن تغییر یافت. این نرم‌افزار یکی از پیشرفته‌ترین ابزارهای موجود برای طراحی شماتیک و PCB است که به‌طور ویژه در صنایع هوافضا، مخابرات و تجهیزات پیشرفته استفاده می‌شود. محیط کاربری آن کاربرپسند با رابط گرافیکی مدرن و قابلیت شخصی‌سازی است. کتابخانه‌ها دقیق، کامل و شامل مدل‌های سه‌بعدی هستند. شبیه‌سازی مدار به صورت داخلی و همچنین اتصال به ابزارهای خارجی قابل انجام است. از طراحی PCB پشتیبانی کرده و مدل‌سازی سه‌بعدی در آن بسیار پیشرفته است. این نرم‌افزار تجاری بوده و با مجوز سالیانه عرضه می‌شود

### نرم افزار OrCAD (Cadence)

اورکد (OrCAD) محصول شرکت Cadence Design Systems است که از دههٔ ۱۹۸۰ توسعه می‌یابد و برای طراحی شماتیک، شبیه‌سازی و PCB در سطح حرفه‌ای کاربرد دارد. محیط کاربری آن بسیار قدرتمند بوده و مناسب کاربران حرفه‌ای و تیم‌های مهندسی است، بنابراین نسبت به نرم‌افزارهای آموزشی پیچیده‌تر به نظر می‌رسد. کتابخانه‌ها دقیق و گسترده‌اند و استانداردهای پیشرفتهٔ صنعتی را پوشش می‌دهند. شبیه‌سازی مدارها با دقت بالا و امکانات تحلیل سیگنال و رفتار گذرا انجام می‌شود. طراحی PCB در آن مطابق نیازهای صنعتی و چندلایه قابل انجام است. نرم‌افزار تجاری بوده و نیاز به خرید مجوز دارد.

### نرم افزار KiCad

کی‌کد (KiCad) نرم‌افزار متن‌باز و رایگان است که از سال ۱۹۹۲ توسعه یافته و اکنون تحت مدیریت تیم بین‌المللی و حمایت CERN عرضه می‌شود. حوزهٔ اصلی استفادهٔ آن طراحی شماتیک و PCB برای پروژه‌های متن‌باز، دانشگاهی و تجاری است.این نرم افزار پنل‌های طراحی، کتابخانه قطعات و نمایش سه‌بعدی برد را به‌طور یکپارچه ارائه می‌دهد. کتابخانه‌ها دقیق و قابل توسعه هستند و کاربران می‌توانند آن‌ها را شخصی‌سازی یا کتابخانه‌های خارجی به آنها اضافه کنند. شبیه‌سازی مدار به‌طور کامل داخلی نیست، ولی امکان اتصال به ابزارهای شبیه‌ساز خارجی مثل SPICE وجود دارد. ابزار طراحی PCB کاملاً حرفه‌ای با پشتیبانی از لایه‌های متعدد و استانداردهای صنعتی ارائه شده است.

### نرم افزار Fritzing

فرتیزینگ یک نرم‌افزار رایگان و متن‌باز است که از سال ۲۰۰۹ برای آموزش و طراحی نمونه‌های اولیه عرضه شده است. تمرکز آن بر نمایش شماتیک، بردبرد و PCB در قالب گرافیکی ساده است. محیط کاربری آن کاملاً کاربرپسند و مناسب مبتدیان است؛ ابزارها و کتابخانه‌ها ساده ولی دقیق برای قطعات رایج هستند. شبیه‌سازی واقعی ندارد و بیشتر نمایش مدار و طرح‌برد است. طراحی PCB قابل انجام است ولی برای کاربردهای صنعتی محدودیت دارد

در ادامه نحوه نصب ، فعال سازی و کار با نرم افزار پروتئوس به عنوان یکی از محبوب ترین ابزار های رسم شماتیک مدار را یاد خواهیم گرفت

## نصب و راه اندازی پروتئوس

این نرم افزار هر چند متن باز نیست و مقداری محدودیت دارد ولی بدلیل محبوبیت آن در بین نرم افزارهای طراحی و رسم شماتیک تصمیم گرفتیم که آموزش کار با این نرم افزار را ارائه دهیم.
می توانید برای تهیه پروتئوس، از سایت مرجع نرم افزار و از این [لینک](https://www.labcenter.com/downloads/) اقدام کنید

روش دیگر و ساده تر برای دانلود نرم افزار ، مراجعه به سایتgeeksforgeeks می باشد که لینک دانلود پروتئوس رو در اختیار کاربران قرار داده که از این [لینک](https://www.geeksforgeeks.org/installation-guide/how-to-download-and-install-proteus-software-on-windows/) قابل دسترسی است.
در این پروژه قصد داریم روش نصب و راه اندازی این نرم افزار محبوب را از این سایت به شما آموزش دهیم.

بعد از اینکه به سایت مراجعه کردید بر روی گزینه دانلود که در صفحه قرار داده شده کلیک کنید
منتظر بمانید که پوشه حاوی نرم افزار بطور کامل دانلود شود.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/proteus-download-1-31886994e7-480.webp 480w, /assets/img/legacy/proteus-download-1-31886994e7-800.webp 800w, /assets/img/legacy/proteus-download-1-31886994e7-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/proteus-download-1-31886994e7.jpg" alt="_figure 2: Download Proteus_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 2: Download Proteus_

</div>

بعد از اینکه فایل زیپ نرم افزار دانلود شد، ان را در مسیر دلخواه خودمان در سیستم از حالت فشرده خارج می کنیم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/proteus-extract-2-fdcc83927c-480.webp 480w, /assets/img/legacy/proteus-extract-2-fdcc83927c-800.webp 800w, /assets/img/legacy/proteus-extract-2-fdcc83927c-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/proteus-extract-2-fdcc83927c.jpg" alt="_figure3:Extrant Proteus_"></picture>

</div>

<div class="caption" markdown="1">

    _figure3:Extrant Proteus_

</div>

طبق تصویر زیر وارد پوشه میشویم و با کلیک بر روی فایل .exe نرم افزار اقدام به نصب آن میکنیم

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/proteus-extract-3-aa41f11a71-480.webp 480w, /assets/img/legacy/proteus-extract-3-aa41f11a71-800.webp 800w, /assets/img/legacy/proteus-extract-3-aa41f11a71-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/proteus-extract-3-aa41f11a71.jpg" alt="_figure4 : Extract proteus2_"></picture>

</div>

<div class="caption" markdown="1">

    _figure4 : Extract proteus2_

</div>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/proteus4-d2c347e081-480.webp 480w, /assets/img/legacy/proteus4-d2c347e081-800.webp 800w, /assets/img/legacy/proteus4-d2c347e081-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/proteus4-d2c347e081.jpg" alt="_figure 5 : Install Proteus_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 5 : Install Proteus_

</div>

مراحل نصب رو طبق راهنما جلو رفته و در آخر صبر میکنیم که فرایند نصب در مسیر مورد نظر کامل شود. به دلیل سهولت این مرحله از بعضی قسمت های آن عبور میکنیم. این قسمت ابهام و پیچیدگی خاصی ندارد.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/proteus-8-b9d98e1665-480.webp 480w, /assets/img/legacy/proteus-8-b9d98e1665-800.webp 800w, /assets/img/legacy/proteus-8-b9d98e1665-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/proteus-8-b9d98e1665.jpg" alt="_figure 6 : Install Protues 2_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 6 : Install Protues 2_

</div>

در نهایت با تکمیل فرایند نصب در مسیر مورد نظر ، روی دکمه Finish کلیک کرده. پروتئوس در سیستم ما نصب شد و حالا میتوانیم وارد آن شویم و از آن استفاده کنیم

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/proteus9-04c98c3e13-480.webp 480w, /assets/img/legacy/proteus9-04c98c3e13-800.webp 800w, /assets/img/legacy/proteus9-04c98c3e13-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/proteus9-04c98c3e13.jpg" alt="_figure 7 : Install Protues 3_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 7 : Install Protues 3_

</div>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/uuproteus-10-81c45e7573-480.webp 480w, /assets/img/legacy/uuproteus-10-81c45e7573-800.webp 800w, /assets/img/legacy/uuproteus-10-81c45e7573-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/uuproteus-10-81c45e7573.jpg" alt="_figure 8: Install Protues 4_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 8: Install Protues 4_

</div>

با ورود به نرم افزار تصویر زیر را میبینیم که ابتدا ورود به محیط نرم افزار است.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/protescomplted-99e81a5d42-480.webp 480w, /assets/img/legacy/protescomplted-99e81a5d42-800.webp 800w, /assets/img/legacy/protescomplted-99e81a5d42-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/protescomplted-99e81a5d42.jpg" alt="_figure 9 : End of Installaion_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 9 : End of Installaion_

</div>

.

مثلا از نوار بالا می توانیم بخش های مربوط به ایجاد فایل ، ادیت ، نما، ابزارها، دیزاین، گراف ، کتابخانه قطعات،و ... را مشاهده کرد. برای ساختن پروژه کافی است که مانند زیر روی بخش New Project کلیک کنیم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-15-22-35-39-6aa769675a-480.webp 480w, /assets/img/legacy/photo-2025-10-15-22-35-39-6aa769675a-800.webp 800w, /assets/img/legacy/photo-2025-10-15-22-35-39-6aa769675a-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-15-22-35-39-6aa769675a.jpg" alt="_figure 10 : Start Project_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 10 : Start Project_

</div>

پنجره New Project Wizard باز می شود. همان طور که مشاهده می شود باید اسمی روی پروژه خود و مسیری در سیستم برای ذخیره آن قرار دهیم

<div dir="rtl" markdown="1">

<strong>پیشنهاد می شود که با تنظیمات پیش فرض خود پروتئوس اقدام به نصب کنید </strong>

</div>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-15-22-36-29-ab17e48bf3-480.webp 480w, /assets/img/legacy/photo-2025-10-15-22-36-29-ab17e48bf3-800.webp 800w, /assets/img/legacy/photo-2025-10-15-22-36-29-ab17e48bf3-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-15-22-36-29-ab17e48bf3.jpg" alt="_figure 11 : New Project_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 11 : New Project_

</div>

در پنجره باز شده زیر ، یک قالب برای شروع پروژه شماتیک خود انتخاب میکنیم. مثلا طبق موارد نمایش داده شده می توانیم، نوع قالب بندی صفحه را بصورت افقی یا Landscape قرار دهیم. بصورت عمودی یا portrait قرار دهیم. یا در آخر یک قالب آماده با تنظیمات نمونه سیستم بسازیم. حالت Sample Design. پروژه را با حالت پیش فرض سیستم یعنی default جلو می بریم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-15-22-53-41-2-2ac2e16b77-480.webp 480w, /assets/img/legacy/photo-2025-10-15-22-53-41-2-2ac2e16b77-800.webp 800w, /assets/img/legacy/photo-2025-10-15-22-53-41-2-2ac2e16b77-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-15-22-53-41-2-2ac2e16b77.jpg" alt="_figure 12 : Select Template_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 12 : Select Template_

</div>

در پنجره بعدی از ما خواسته می شود که برای طراحی چاپی با همان PCB بردی را از میان موارد لیست شده انتخاب کنیم. ولی چون در این پروژه هدف ما یادگیری طراحی شماتیک است با حالت Don't create a PCB layout ادامه می دهیم

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-16-07-46-34-a00369ce12-480.webp 480w, /assets/img/legacy/photo-2025-10-16-07-46-34-a00369ce12-800.webp 800w, /assets/img/legacy/photo-2025-10-16-07-46-34-a00369ce12-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-16-07-46-34-a00369ce12.jpg" alt="_figure 13 : Select Template for PCB_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 13 : Select Template for PCB_

</div>

در مرحله آخر از ما خواسته می شود که مشخص کنیم که پروژه ما شامل کد برنامه نویسی (Firmware) و یا نمودار منطقی برای میکروکنتلر ها (Flowchart) باشد یا خیر. با حالت پیش فرض یعنی No firmware Project ادامه میدهیم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-16-07-46-28-3fd3b2d28d-480.webp 480w, /assets/img/legacy/photo-2025-10-16-07-46-28-3fd3b2d28d-800.webp 800w, /assets/img/legacy/photo-2025-10-16-07-46-28-3fd3b2d28d-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-16-07-46-28-3fd3b2d28d.jpg" alt="_figure 14 : Firmware Selection_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 14 : Firmware Selection_

</div>

حالا پروژه ما ساخته شده. دقت شود که در این پروژه فقط میخواهیم که حالت شماتیک مدار را بررسی کنیم نه PCB .

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-16-07-46-22-0fc76b6974-480.webp 480w, /assets/img/legacy/photo-2025-10-16-07-46-22-0fc76b6974-800.webp 800w, /assets/img/legacy/photo-2025-10-16-07-46-22-0fc76b6974-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-16-07-46-22-0fc76b6974.jpg" alt="_figure 15 : Start Project_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 15 : Start Project_

</div>

## شرح محیط طراحی شماتیک

در بخش Schematic Capture پروتئوس، محیطی وجود دارد که میتوانیم مدار را بصورت شماتیک رسم کنیم. حالا میخواهیم بیشتر با این قسمت آشنا شویم.

نوار بالای این صفحه شامل دکمه ها و آیکون های اصلی است. کاربرد این بخش عبارت است از
ایجاد، باز و ذخیره کردن پروژه ها(New , Open , Save ) - ابزار های بزرگ نمایی و جابجایی دید در مدار (Zoom In , Zoom Out) ابزارهای اضافه کردن سیم ، لیبل ، منبع تغذیه - گزینه های Simulation برای توقف یا اجرای مدار

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-16-07-46-18-54bef54f21-480.webp 480w, /assets/img/legacy/photo-2025-10-16-07-46-18-54bef54f21-800.webp 800w, /assets/img/legacy/photo-2025-10-16-07-46-18-54bef54f21-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-16-07-46-18-54bef54f21.jpg" alt="_figure 16 : Main ToolBar_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 16 : Main ToolBar_

</div>

بخش دوم نوار ابزار سمت چپ است که که شامل ابزارهای کاربردی طراحی است
قسمت های مهم آن شامل Selection Tool برای انتخاب قطعات. Component Mode برای انتخاب قطعات از کتابخانه text lable mode برای نوشتن توضیحات کنار قطعات ، Terminals mode برای تعیین ورودی ، خروجی ، زمین ،VCC و دیگر ابزار هایی که بسته به اهداف پیاده سازی ما ممکن است مورد استفاده قرار گیرند.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-16-09-59-19-d51cb0084e-480.webp 480w, /assets/img/legacy/photo-2025-10-16-09-59-19-d51cb0084e-800.webp 800w, /assets/img/legacy/photo-2025-10-16-09-59-19-d51cb0084e-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-16-09-59-19-d51cb0084e.jpg" alt="_figure 17 : Devices Panel 1_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 17 : Devices Panel 1_

</div>

بخش سوم پنجره دستگاه هاست که وقتی روی P(pick devices) کلیک میکنیم پنجره ای برای ما باز میشود که اسم قطعات، مدل و مشخصات ان ها نمایش داده شده است. این قسمت همان جعبه قطعات است که می توان از داخل ان انواع ترانزیستور ها، مقاومت ها، دیود ها و ... را انتخاب نمود. با کلیک روی Library و زدن روی گزینه pick devices هم میتوان به این قسمت دسترسی پیدا کرد. برای انتخاب قطعه مورد نظر فقط کافی است نام قطعه را در نواری که در تصویر مشخص شده وارد کرده و جستجو کنیم.
گاهی ممکن است که قطعه ای در دسترس نباشد. مثل بعضی سنسور ها یا Arduino . تحت این شرایط می شود که کتابخانه های مربوطه را دانلود کرد و در مسیر نصب نرم افزار کپی کرده. پروتئوس رو بسته و مجدد پروژه را راه اندازی کرده تا کتابخانه قطعه مورد نظر را شناسایی کند.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-16-09-59-167-54541df640-480.webp 480w, /assets/img/legacy/photo-2025-10-16-09-59-167-54541df640-800.webp 800w, /assets/img/legacy/photo-2025-10-16-09-59-167-54541df640-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-16-09-59-167-54541df640.jpg" alt="_figure 18 : Devices Panel 2_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 18 : Devices Panel 2_

</div>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-155500-842a37cfd2-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-155500-842a37cfd2-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-155500-842a37cfd2-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/screenshot-2025-10-17-155500-842a37cfd2.png" alt="_figure 19 : Devices Panel 3_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 19 : Devices Panel 3_

</div>

و دو بخش آخر محیط شماتیک Schematic sheet و Status Bar هستن. در بخش اول که به شکل صفحه ای مشبک است، طراحی مدار صورت میگیرد. یعنی قطعات بعد از اینکه انتخاب می شوند در این محیط قرار گرفته و ارتباطات میان انها توسط سیم بهم برقرار می شود. و در آخر، بخش پایین که می توان در آن مختصات مکان نما که با x و y معلوم شده است را مشاهده کرد.و سمت چپ نام شیت فعلی و پیام های هشدار و خطا هنگام طراحی یا شبیه سازی مدار ، دکمه های شروع و توقف شبیه سازی قابل مشاهده می باشد.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/photo-2025-10-16-15-47-01-b19a69fb74-480.webp 480w, /assets/img/legacy/photo-2025-10-16-15-47-01-b19a69fb74-800.webp 800w, /assets/img/legacy/photo-2025-10-16-15-47-01-b19a69fb74-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/photo-2025-10-16-15-47-01-b19a69fb74.jpg" alt="_figure 20 : Shematic Area_"></picture>

</div>

<div class="caption" markdown="1">

    _figure 20 : Shematic Area_

</div>

در فاز بعدی پروژه به طراحی چند مدار الکتریکی ساده می پردازیم و در حین طراحی به معرفی بعضی اصول و استاندارد های طراحی اشاره خواهیم کرد.

## نحوه طراحی شماتیک مدارهای الکتریکی

قصد داریم مداری ساده با مقاومت ، ال ای دی ، منبع تغذیه، دیود در محیط پروتئوس بسازیم. طبق روش های گفته شده ابتدا پروژه ای جدید می سازیم. سپس از جعبه قطعات(pick tools)نام لاتین هر کدام از ابزار ها را در نوار جستجو تایپ میکنیم. برای مقاومت res برای دیود diode برای منبع تغذیه battery برای ال ای دی LED . سپس روی ok کلیک کرده تا ابزار ها همانند تصویر زیر در پنجره ابزار ها قرار گیرند.
در طول پروژه سعی می شود نکات و اصول مورد نیازی که لازم است هنگام طراحی رعایت شود را ذکر کنیم

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-132413-3dcee79ed9-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-132413-3dcee79ed9-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-132413-3dcee79ed9-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 21: Select Tools_" src="/assets/img/legacy/screenshot-2025-10-17-132413-3dcee79ed9.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 21: Select Tools_

</div>

سپس هر کدام را انتخاب کرده و روی صفحه قرار میدهیم. مانند یک drag کردن ساده.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-135503-9b895c58e0-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-135503-9b895c58e0-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-135503-9b895c58e0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 22: Drag Tools To Area_" src="/assets/img/legacy/screenshot-2025-10-17-135503-9b895c58e0.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 22: Drag Tools To Area_

</div>

هنوز مدار کامل نشده. کافی است که المان ها را با سیم بهم متصل کنیم. هر المانی دو سر مثبت و منفی دارد. باید توجه کرد که سر مثبت المان ها به سر مثبت باتری و سر منفی انها با سیم به سر منفی منبع تغذیه متصل شود. روی یک سر المان کلیک کرده تا شکل سیم ظاهر شود . سپس با حفظ قطبیت به هم متصل می کنیم.
دقت شود که سیم ها فقط در جهت افقی یا عمودی امتداد می یابند نه مورب.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-142831-a280d2aa45-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-142831-a280d2aa45-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-142831-a280d2aa45-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 23: Drawing Circuit_" src="/assets/img/legacy/screenshot-2025-10-17-142831-a280d2aa45.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 23: Drawing Circuit_

</div>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-142917777-b5662f3629-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-142917777-b5662f3629-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-142917777-b5662f3629-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 24: Drawing Circuit 2_" src="/assets/img/legacy/screenshot-2025-10-17-142917777-b5662f3629.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 24: Drawing Circuit 2_

</div>

ممکن است وقتی از مدار اجرا میگیریم، ال ای دی روشن نشود. این چند حالت میتواند داشته باشد.

1- جهت دیود مخالف جریان عبوری باشد

2- مقدار مقاومت به قدری زیاد است که مانع از عبور جریان میشود

3- ال ای دی برای روشن شدن به مقدار ولتاژی بیشتر از ولتاژ باتری نیاز دارد

کام به گام بررسی میکنیم . ابتدا دو بار روی ال ای دی راست کلیک کرده تا مشخصات آن رو ببینیم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-144903-98b6c04772-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-144903-98b6c04772-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-144903-98b6c04772-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 25: Drawing Circuit 3_" src="/assets/img/legacy/screenshot-2025-10-17-144903-98b6c04772.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 25: Drawing Circuit 3_

</div>

با توجه به شکل متوجه می شویم که این ال ای دی برای روشن شدن به حداقل ولتاژ 2.2 ولت(ولتاژ آستانه) احتیاج دارد. پس باید از جعبه قطعات باتری ای با ولتاژ بالاتر انتخاب کنیم. دقت شود که وقتی مدار در حالت فعال قرار دارد نمی توان هیچ کدام از اجزای مدار را تغییر داد. بلکه باید روی گزینه stop که با نماد مربع درنوار status قرار گرفته کلیک کرده سپس اقدام به برداشتن یا جایگزین کردن اجزای مدار کرد.

البته می توان برای شناسایی ارور های هنگام طراحی به بخش پیام ها درنوار پایین مراجعه کرد

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-143104-68ec69be67-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-143104-68ec69be67-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-143104-68ec69be67-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 26: Handling Errors_" src="/assets/img/legacy/screenshot-2025-10-17-143104-68ec69be67.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 26: Handling Errors_

</div>

برای حذف المان ها کافی است روی ان ها راست کلیک کرده و روی گزینه delete در پنجره ای که باز می شود کلیک کنیم. می بینیم که المان به همراه سیم های متصل به آن به سادگی حذف خواهند شد.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-153006-0dbc6aae92-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-153006-0dbc6aae92-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-153006-0dbc6aae92-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 27: Deleting Elements_" src="/assets/img/legacy/screenshot-2025-10-17-153006-0dbc6aae92.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 27: Deleting Elements_

</div>

از قسمت جعبه قطعات یک مقاومت 1 کیلو اهمی و یک منبع تغذیه 9 ولتی انتخاب می کنیم و مانند شکل زیر دوباره مدار رو می بندیم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-155410-cbbd56ccc0-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-155410-cbbd56ccc0-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-155410-cbbd56ccc0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 28: Replace Elements In Circuit_" src="/assets/img/legacy/screenshot-2025-10-17-155410-cbbd56ccc0.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 28: Replace Elements In Circuit_

</div>

حالا روی دکمه run the simulation در نوار پایین کلیک میکنیم. مشاهده میکنیم که LED روشن می شود.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-155430-a29d95025f-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-155430-a29d95025f-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-155430-a29d95025f-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 29:  Turning On The LED_" src="/assets/img/legacy/screenshot-2025-10-17-155430-a29d95025f.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 29:  Turning On The LED_

</div>

حالا اگر جهت دیود در مدار را برعکس کنیم یعنی سیم ها رو به دیگر قطب های آن متصل کنیم. اگر روی دکمه اجرا کلیک کنیم، می بینیم که ال ای دی روشن نمی شود.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-161004-bd3dc2e8e4-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-161004-bd3dc2e8e4-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-161004-bd3dc2e8e4-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 30:  Unable To Turning On The LED_" src="/assets/img/legacy/screenshot-2025-10-17-161004-bd3dc2e8e4.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 30:  Unable To Turning On The LED_

</div>

از همین قسمت متوجه می شویم که دیود ها یک سو کننده های جریان هستند یعنی جریان در مدار را تنها از یک سو عبور می دهند.

گاهی ممکن است در طراحی اشتباهاتی رخ دهد. از قبیل اتصال یک سیم اشتباه به ترمینال یک از المان های مدار. در این شرایط کافی است با نگهداری هم زمان کلید های Ctrl و z تغییرات رو به حالت (های) قبل بازگردانیم.

اگر دقت کنیم می بینم که این المان ها دو پرچسب(lable) دارند. بالایی Part Id نام دارد که برای مقاومت با R و برای دیود با D مشخص میشوند. هر چند طبق تصویر زیر می توانیم این مقادیر پیش فرض را به دلخواه خودمان تغییر دهیم.
برای تغییر مقدار هر پرچسب کافی است روی آن کلیک کنیم

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-161935-94cd54aec8-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-161935-94cd54aec8-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-161935-94cd54aec8-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 31:  Element&#x27;s Lables_" src="/assets/img/legacy/screenshot-2025-10-17-161935-94cd54aec8.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 31:  Element's Lables_

</div>

بر چسب پایینی مربوط به مقدار است که با part value مشخص می شود. نکته حائز اهمیت در این بخش این است که میتوان این مقادیر را تغییر داد. مثلا طبق تصویر زیر به جای مقاومت 1 کیلو اهمی ما مقدار 0.25 کیلو اهم را وارد کردیم.

حالا اگر دوباره مدار رو راه اندازی کنیم، می بینیم که مقدار روشنایی LED نسبت به حالت قبلی بیشتر شد!

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-162052-170f28fe60-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-162052-170f28fe60-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-162052-170f28fe60-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 32:  Element&#x27;s Lables 2_" src="/assets/img/legacy/screenshot-2025-10-17-162052-170f28fe60.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 32:  Element's Lables 2_

</div>

در مرحله اخر روی گزینه save project از نوار بالا کلیک کرده تا پروژه ذخیره شود.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/screenshot-2025-10-17-165029-d677725d73-480.webp 480w, /assets/img/legacy/screenshot-2025-10-17-165029-d677725d73-800.webp 800w, /assets/img/legacy/screenshot-2025-10-17-165029-d677725d73-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 33:  save project_" src="/assets/img/legacy/screenshot-2025-10-17-165029-d677725d73.png"></picture>

</div>

<div class="caption" markdown="1">

    _figure 33:  save project_

</div>

حال می خواهیم مدار دیگری را با روش های اموخته شده رسم کنیم که کمی پیچیده تر از این مدار ازمایش قیل است.

میخواهیم با بستن یک مدار، یک سون سگمنت را روشن کنیم
در ابتدا یک پروژه در مسیر دلخواه خود می سازیم. وسایل مورد نیاز ما: یک سون سگمنت آند مشترک، 7 عدد مقاومت به ازای 7 LED سون سگمنت، یک دیکودر یا IC آند مشترک که در ایجا 7447 است. ترمینال Vcc و زمین و ۴ سوویچ برای تولید اعداد باینری بین 0 تا 9

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/capture-ac7ec4a9c0-480.webp 480w, /assets/img/legacy/capture-ac7ec4a9c0-800.webp 800w, /assets/img/legacy/capture-ac7ec4a9c0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 34:  Seven Segment_" src="/assets/img/legacy/capture-ac7ec4a9c0.jpg"></picture>

</div>

<div class="caption" markdown="1">

    _figure 34:  Seven Segment_

</div>

حالا که ابزار های لازم را در اختیار داریم، کافی است که اتصالات لازم را برقرار کنیم. ابتدا یک سر هر سوویچ را به زمین و سر دیگر انها رو به همین ترتیب طبق شکل زیر به ترمینال Vcc وصل می کنیم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/capture2-71ef419d98-480.webp 480w, /assets/img/legacy/capture2-71ef419d98-800.webp 800w, /assets/img/legacy/capture2-71ef419d98-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 35:  Seven Segment 1_" src="/assets/img/legacy/capture2-71ef419d98.jpg"></picture>

</div>

<div class="caption" markdown="1">

    _figure 35:  Seven Segment 1_

</div>

3 ورودی کنترلی سون سگمنت را ( LT , RBI , BI) به ولتاژ مثبت باتری وصل کنیم. قسمت مشترک هر سوویچ را به ورودی های دیکودر به ترتیب از A تا D وصل میکنیم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/capture3-a038b257ad-480.webp 480w, /assets/img/legacy/capture3-a038b257ad-800.webp 800w, /assets/img/legacy/capture3-a038b257ad-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 36:  Seven Segment 2_" src="/assets/img/legacy/capture3-a038b257ad.jpg"></picture>

</div>

<div class="caption" markdown="1">

    _figure 36:  Seven Segment 2_

</div>

حال در گام بعدی 7 خروجی دیکودر را به ترتیب به ورودی های a تا g سون سگمنت متصل می کنیم. چون سون سگمنت آند مشترک است، پایه مشترک را به Vcc وصل می کنیم.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/capture4-a0efd79221-480.webp 480w, /assets/img/legacy/capture4-a0efd79221-800.webp 800w, /assets/img/legacy/capture4-a0efd79221-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 37:  Seven Segment 3_" src="/assets/img/legacy/capture4-a0efd79221.jpg"></picture>

</div>

<div class="caption" markdown="1">

    _figure 37:  Seven Segment 3_

</div>

حالا که مدار کامل شد کافی است که با سوویچ ها ورودی بدهیم. می خواهیم عدد 1 را روی سون سگمنت نشان دهیم.به ترتیب زیر اقدام می کنیم:

SW 1 --> Vcc

SW 2 --> GND

SW 3 --> GND

SW 4 --> GND

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/capture5-6604c1c6d7-480.webp 480w, /assets/img/legacy/capture5-6604c1c6d7-800.webp 800w, /assets/img/legacy/capture5-6604c1c6d7-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 38:  Seven Segment 4_" src="/assets/img/legacy/capture5-6604c1c6d7.jpg"></picture>

</div>

<div class="caption" markdown="1">

    _figure 38:  Seven Segment 4_

</div>

برای نمایش عدد 3، سوویچ ها رو به ترتیب زیر وصل می کنیم:

SW 1 = Vcc

SW 2 = Vcc

SW 3 = GND

SW 4 = GND

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/capture6-c9bee79155-480.webp 480w, /assets/img/legacy/capture6-c9bee79155-800.webp 800w, /assets/img/legacy/capture6-c9bee79155-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 39:  Seven Segment 5_" src="/assets/img/legacy/capture6-c9bee79155.jpg"></picture>

</div>

<div class="caption" markdown="1">

    _figure 39:  Seven Segment 5_

</div>

و برای نمایش عدد 8 :

SW 1 = GND

SW 2 = GND

SW 3 = GND

SW 4 = Vcc

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/capture7-1460bf3dfb-480.webp 480w, /assets/img/legacy/capture7-1460bf3dfb-800.webp 800w, /assets/img/legacy/capture7-1460bf3dfb-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="_figure 40:  Seven Segment 6_" src="/assets/img/legacy/capture7-1460bf3dfb.jpg"></picture>

</div>

<div class="caption" markdown="1">

    _figure 40:  Seven Segment 6_

</div>

## نتیجه گیری

در این پروژه انواع ابزار های رایج رسم شماتیک مدار را نظیر پروتئوس ، کیکد، اورکد و آلتیوم را از نظیر کاربری محیط نرم افزار ، کتابخانه قطعات ، امکان طراحی PCB و .. بررسی کردیم. در بخش دوم پروژه یاد گرفتیم که چگونه پروتئوس را نصب و راه اندازی کنیم . با محیط کار آن آشنا شدیم ، اینکه چگونه از جعبه قطعات ، ابزاری را انتخاب یا در صورت نبود آن ، کتابخانه اش را به پروتئوس اضافه کنیم و در فاز آخر پروژه با ترسیم دو مدار الکتریکی سعی شد که بعضی از نکات مهم و اصولی در مورد طراحی را بیاموزیم.

## منابع

<div markdown="1">

<a href="https://www.labcenter.com" 
     target="_blank">
https://www.labcenter.com
</a>

</div>

<div markdown="1">

<a href="https://fritzing.org/learning/" 
     target="_blank">
https://fritzing.org/learning/
</a>

</div>

<div markdown="1">

<a href="https://www.altium.com/documentation" 
     target="_blank">
https://www.altium.com/documentation
</a>

</div>

<div markdown="1">

<a href="https://www.cadence.com/en_US/home/tools/pcb-design-and-analysis/orcad.html" 
     target="_blank">
https://www.cadence.com/en_US/home/tools/pcb-design-and-analysis/orcad.html
</a>

</div>

<div markdown="1">

<a href="https://docs.kicad.org/" 
     target="_blank">
https://docs.kicad.org
</a>

</div>

<div markdown="1">

<a href="https://theengineeringmindset.com/the-basics-of-diodes-explained/" 
     target="_blank">
https://theengineeringmindset.com/the-basics-of-diodes-explained
</a>

</div>

<div markdown="1">

<a href="https://www.electronics-tutorials.ws/blog/7-segment-display-tutorial.html" 
    target="_blank">
https://www.electronics-tutorials.ws/blog/7-segment-display-tutorial.html
</a>

</div>

<div markdown="1">

<a href="https://www.geeksforgeeks.org/installation-guide/how-to-download-and-install-proteus-software-on-windows/" 
    target="_blank">
https://www.geeksforgeeks.org/installation-guide/how-to-download-and-install-proteus-software-on-windows/
</a>

</div>

{% endraw %}
