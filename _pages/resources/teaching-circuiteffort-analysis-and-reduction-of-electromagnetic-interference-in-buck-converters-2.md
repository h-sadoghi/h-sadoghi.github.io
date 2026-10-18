---
layout: legacy_page
title: تحلیل و کاهش تداخل الکترومغناطیسی در مبدل‌های سوئیچینگ ادامه
permalink: /resources/teaching-circuiteffort-analysis-and-reduction-of-electromagnetic-interference-in-buck-converters-2/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/circuiteffort/Analysis_and_reduction_of_electromagnetic_interference_in_buck_converters_2/
legacy_group: Circuits and electronics
legacy_dir: rtl
lang: fa
---

{% raw %}

# تحلیل و کاهش تداخل الکترومغناطیسی در مبدل‌های سوئیچینگ - 2

## فهرست مطالب

<!-- prettier-ignore -->
* TOC
{:toc}

## اطلاعات نویسنده

**نام:** علی طلبی طرق
**وابستگی:** گروه مهندسی کامپیوتر، دانشگاه فردوسی مشهد

## مقدمه

در حالی که "Interference" معمولاً به اشکال غیر عمدی اختلال در ارتباطات بی‌سیم اشاره دارد، "Jamming" به اختلال **عمدی** یا مسدود کردن چنین ارتباطاتی اشاره دارد.
همانطور که از نامش پیداست، آنتن‌های جمینگ (که به آن‌ها "جمر" هم گفته می‌شود) به طور خاص برای اختلال در نویز یا سیگنال‌های رادیویی استفاده می‌شوند.

یکی از رایج‌ترین کاربردهای انواع جمر در پمپ بنزین‌ها است. دلیل اصلی این است که استفاده از موبایل باعث گرم شدن دستگاه شده و در نتیجه خطر آتش‌سوزی را افزایش خواهد داد. پس به لحاظ حفظ امنیت جایگاه، با به کارگیری جمر از انتقال امواج و در نتیجه افزایش گرما جلوگیری میشود.

## بررسی یک نمونه جمر

میتوان با استفاده از چند خازن، ترانزیستور و سلف، یک جمر محدود و تاحدودی بی خطر ساخت. با توجه به نوع عملکرد جمر، روش های بی شماری برای تولید این دستگاه وجود دارد. میتوان برای نمونه چند مدار را بررسی کرد.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/normal-jammer-f20cc06eff-480.webp 480w, /assets/img/legacy/normal-jammer-f20cc06eff-800.webp 800w, /assets/img/legacy/normal-jammer-f20cc06eff-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/normal-jammer-f20cc06eff.png" alt="A Simple Jammer Circuit"></picture>

</div>

/assets/circuiteffort/electromagnetic_interference
#electromagnetic_interference

<div class="caption" markdown="1">

_تصویر 1: مدار جمر_

</div>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/high-voltage-jammer-6d6ec55d9d-480.webp 480w, /assets/img/legacy/high-voltage-jammer-6d6ec55d9d-800.webp 800w, /assets/img/legacy/high-voltage-jammer-6d6ec55d9d-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/high-voltage-jammer-6d6ec55d9d.png" alt="High Voltage Jammer"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 2: جمر با قابلیت تولید ولتاژ بالاتر_

</div>

در این بحث به سنتز مدار جمر با ولتاژ بالاتر خواهیم پرداخت. به این منظور تجهیزات مدنظر بدین صورت خواهد بود:

- سه عدد خازن با ظرفیت 22 پیکوفاراد
- یک عدد خازن با ظرفیت 68 پیکوفاراد
- منبع ولتاژ - 5 تا 30 ولت
- یک عدد مقاومت 10 کیلواهم
- یک عدد کویل با قطر 2.5 سانتی متر، قطر سیم 0.4 میلی متر و 65 دور
- یک عدد ترانزیستور 2SC2078 با نام تجاری NTE152

نکته: تمامی خازن ها سرامیکی با ظرفیت ولتاژی 500 ولت هستند.
نکته: توان مصرفی مقاومت 0.5 وات بوده و مقاومت تلرانس 5 درصدی (طلایی) خواهد داشت.
نکته: NTE152 نام تحاری ترانزیستور مورد استفاده بوده و استففاده از موارد مشابه مشکلی نخواهد داشت.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/t1-transistor-d5cfe13f26-480.webp 480w, /assets/img/legacy/t1-transistor-d5cfe13f26-800.webp 800w, /assets/img/legacy/t1-transistor-d5cfe13f26-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/t1-transistor-d5cfe13f26.png" alt="Details"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 3: نکات تجهیزات و جزئیات ترانزیستور_

</div>

با توجه به تجهیزات مورد استفاده، مدار باید به صورت زیر باشد:

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/full-circuit-bcc27311e1-480.webp 480w, /assets/img/legacy/full-circuit-bcc27311e1-800.webp 800w, /assets/img/legacy/full-circuit-bcc27311e1-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/full-circuit-bcc27311e1.png" alt="Full Circuit"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 4: شماتیک کامل مدار جمر_

</div>

نکته: فرکانس دریافتی از مدار به ابعاد و ویژگی های سیم پیچ و ظرفیت خازن ها بستگی دارد.

## نحوه عملکرد مدار

در این مدار به جای استفاده از دو سیم پیچ و نیاز به رزونانس، دو مدار القاگر تعبیه شده است. این دو مدار هر کدام ظرفیت 22+68 پیکوفارادی داشته و نیاز به رزونانس رو برای فعالیت مدار از بین میبرد.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/oscillating-circuits-capacity-f5274e224a-480.webp 480w, /assets/img/legacy/oscillating-circuits-capacity-f5274e224a-800.webp 800w, /assets/img/legacy/oscillating-circuits-capacity-f5274e224a-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/oscillating-circuits-capacity-f5274e224a.png" alt="Capacity"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 5: ظرفیت مدارهای القاگر_

</div>

به صورت دقیق تر، مدار های به این شکل خواهند بود:

- مدار القاگر یک

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/oscillating-circuit-1-a61e19d36d-480.webp 480w, /assets/img/legacy/oscillating-circuit-1-a61e19d36d-800.webp 800w, /assets/img/legacy/oscillating-circuit-1-a61e19d36d-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/oscillating-circuit-1-a61e19d36d.png" alt="1st Oscillator"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 6: مدار القاگر شماره یک_

</div>

- مدار القاگر دو

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/oscillating-circuit-2-68fe8107a4-480.webp 480w, /assets/img/legacy/oscillating-circuit-2-68fe8107a4-800.webp 800w, /assets/img/legacy/oscillating-circuit-2-68fe8107a4-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/oscillating-circuit-2-68fe8107a4.png" alt="2nd Oscillator"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 7: مدار القاگر شماره دو_

</div>

آنتن جمر به نقطه میان دو مدارالقاگر متصل میشود. به دلیل القای الکترومغناطیس حاصل از القاگر ها، amplitude بالا و بالاتر رفته و به همین دلیل ولتاژ در نقطه اتصال آنتن به مدار در ادامه آنقدر بالا خواهد بود که شدت میدان را به حدی بالا ببرد تا موج الکترومغناطیس حاصل از آنتن توانایی بهم ریختگی و ایجاد آشفتگی در امواج را داشته باشد.
به همین علت است که توصیه میشود تمام خازن ها، استقامت دی‌الکتریک مشابه و بسیار بالایی داشته باشند تا دچار شکست نشوند.

## نتایج استفاده از جمر

با اینکه قدرت این جمر کم و به نوعی بی خطر محسوب میشود، اما استفاده از جمر ها میتواند نتایج نامطلوبی را از قبیل از بین رفتن مدارات و تجهیزات دستگاه های الکترونیکی، تداخل در امواج حساس و ... را به همراه داشته باشد. پس توصیه میشود در تولید و نهایتا در استففاده از مدار های جمر این موارد مدنظر قرار گیرد.

در نمونه های زیر میتوان تاثیر این مدار جمر را روی لامپ و یک ماشین حساب دیجیتالی مشاهده کرد.

- تاثیر مدار جمر روی لامپ

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/jammer-and-lamp-8db525f7f5-480.webp 480w, /assets/img/legacy/jammer-and-lamp-8db525f7f5-800.webp 800w, /assets/img/legacy/jammer-and-lamp-8db525f7f5-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/jammer-and-lamp-8db525f7f5.png" alt="Lamp"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 8: روشن شدن لامپ در اثر امواج الکترومغناطیس حاصل از مدار_

</div>

- تاثیر مدار جمر روی ماشین حساب

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/jammer-and-calc-1-9b186fb2ea-480.webp 480w, /assets/img/legacy/jammer-and-calc-1-9b186fb2ea-800.webp 800w, /assets/img/legacy/jammer-and-calc-1-9b186fb2ea-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/jammer-and-calc-1-9b186fb2ea.png" alt="Calculator - 1"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 9: آشفتگی و از بین رفتن داده ها در ماشین حساب در اثر امواج الکترومغناطیس حاصل از مدار - 1_

</div>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/jammer-and-calc-2-f021c8c547-480.webp 480w, /assets/img/legacy/jammer-and-calc-2-f021c8c547-800.webp 800w, /assets/img/legacy/jammer-and-calc-2-f021c8c547-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/jammer-and-calc-2-f021c8c547.png" alt="Calculator - 2"></picture>

</div>

<div class="caption" markdown="1">

_تصویر 10: آشفتگی و از بین رفتن داده ها در ماشین حساب در اثر امواج الکترومغناطیس حاصل از مدار - 2_

</div>

## نتیجه

در دومین فاز از پروژه تداخل الکترومغناطیسی، به بررسی ساخت و عملکرد یک جمر ساده با استفاده از مدارهای القاگر و اجزای الکترونیکی خاص پرداخته شد. نتایج نشان داد که جمر با استفاده از اجزای مختلف مانند خازن‌ها، ترانزیستور و کویل قادر است سیگنال‌ها را قطع کرده و موج‌های الکترومغناطیسی تولید کند که می‌تواند اختلالات قابل توجهی در سیستم‌های الکترونیکی ایجاد کند. با این حال، باید توجه داشت که استفاده از چنین دستگاه‌هایی ممکن است منجر به آسیب به تجهیزات حساس الکترونیکی یا ایجاد تداخل در سیستم‌های دیگر شود، بنابراین طراحی و استفاده از این مدارها باید با دقت و احتیاط انجام گیرد.

## منابع

- https://www.sciencedirect.com/topics/engineering/jammer
- https://www.sciencedirect.com/topics/engineering/jamming
- https://www.sciencedirect.com/science/article/pii/S2542660520301359
- https://jemengineering.com/blog-an-introduction-to-jammers/
- https://www.sbg-systems.com/glossary/jammer/
- https://www.youtube.com/watch?v=mFbi3Aqn8m8&list=PLOWaPB-Ur3Jia_XOV7TWTkMxqi7_J9rz0
  {% endraw %}
