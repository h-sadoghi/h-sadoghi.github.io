---
layout: legacy_page
title: آموزش Pull Request
permalink: /resources/teaching-patterneffort-pull-request/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/patterneffort/PULL_REQUEST/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

<div markdown="1">

    <img loading="lazy" src="/assets/img/legacy/fum-logo-c752fa7c60.jpg" alt="FUM_LOGO">

</div>

**نویسندگان:** محمدرضا باباگلی، محمدصالح علی اکبری  
دانشجویان ارشد هوش‌ مصنوعی دانشگاه فردوسی مشهد  
آزمایشگاه شناسایی الگو دکتر هادی صدوقی یزدی

# Pull Request

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/pull-request-icon-40cd381d2b-480.webp 480w, /assets/img/legacy/pull-request-icon-40cd381d2b-800.webp 800w, /assets/img/legacy/pull-request-icon-40cd381d2b-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/pull-request-icon-40cd381d2b.png"  alt="pull_request_icon"></picture>

</div>

## مقدمه

**Pull Request (PR)** مفهومی در سیستم‌های کنترل نسخه توزیع‌شده مانند Git است و بیشتر در پلتفرم‌هایی مثل GitHub، GitLab و Bitbucket استفاده می‌شود.

به طور ساده، Pull Request درخواستی است برای اینکه تغییراتی که در یک شاخه (branch) ایجاد کرده‌اید، به شاخه‌ی اصلی پروژه (مثلاً `main` یا `develop`) اضافه شود.

فرآیند معمول به این صورت است:

ابتدا یک branch جدید از شاخه اصلی می‌سازید. سپس تغییرات مورد نظر (مثلاً افزودن یک قابلیت یا اصلاح یک باگ) را اعمال و commit می‌کنید. بعد از آن branch را به مخزن راه‌دور (remote repository) push می‌کنید. در نهایت یک Pull Request ایجاد می‌کنید تا سایر اعضای تیم تغییرات را بررسی کنند.

Pull Request فقط برای ادغام کد نیست، بلکه یک ابزار همکاری است. در آن می‌توان:

- کد را بازبینی (Code Review) کرد
- درباره تغییرات بحث کرد
- تست‌های خودکار (CI) را اجرا کرد
- قبل از ادغام، مشکلات احتمالی را شناسایی کرد

پس از تأیید، تغییرات به شاخه مقصد merge می‌شوند.

Pull Request یعنی این‌که به صاحب یک پروژه بگویید:

«من یک‌سری تغییر در کد انجام داده‌ام. لطفاً بررسی کن و اگر درست بود، آن را به پروژه اصلی اضافه کن.»

فرض کنید چند نفر روی یک پروژه برنامه‌نویسی کار می‌کنند. هر نفر روی یک نسخه جداگانه (branch) کار می‌کند تا به نسخه اصلی آسیب نزند. وقتی کارش تمام شد، مستقیماً کد را وارد نسخه اصلی نمی‌کند. اول یک درخواست می‌فرستد تا بقیه کدش را ببینند، نظر بدهند، و اگر مشکلی نبود آن را تأیید کنند. این درخواست همان Pull Request است.

پس:

- شما تغییر ایجاد می‌کنید
- درخواست می‌دهید تغییرتان بررسی شود
- اگر تأیید شد، به پروژه اصلی اضافه می‌شود

در واقع Pull Request راهی است برای کنترل کیفیت و همکاری تیمی در برنامه‌نویسی.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/pull-request-process-4245e45a7a-480.webp 480w, /assets/img/legacy/pull-request-process-4245e45a7a-800.webp 800w, /assets/img/legacy/pull-request-process-4245e45a7a-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/pull-request-process-4245e45a7a.png" alt="pull-request-process"></picture>

</div>

## آموزش Pull Request برای مشاهده پروژه‌ها در سایت استاد

**گام اول:**

در سال 1404، دانشجویان درس شناسایی الگو، به صورت زیر پروژه خود را در سایت استاد آپلود می‌کردند:

ابتدا یک شخص مخزن استاد را fork (ایجاد شاخهٔ مستقل از یک پروژه در حساب کاربری خود) می‌کند.

سپس دانشجویان دیگر، آن مخرن فورک‌شده را فورک می‌کنند تا این مخزن به مخازن هر دانشجو اضافه شود.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/fork-b40875ded2-480.webp 480w, /assets/img/legacy/fork-b40875ded2-800.webp 800w, /assets/img/legacy/fork-b40875ded2-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/fork-b40875ded2.png" alt="fork"></picture>

</div>

<p class="wp-caption-text">
fork کردن مخزن</p>

اکنون شما یک کپی مستقل از مخزن روی سرور گیت‌هاب در اکانت خود دارید.
(می‌توانید از مخزن را در بخش Repositories حساب خود مشاهده کنید.)

**کاربرد اصلی fork:**

معمولاً زمانی استفاده می‌شود که می‌خواهید در یک پروژهٔ عمومی تغییر ایجاد کنید، بدون اینکه به مخزن اصلی دسترسی مستقیم (write access) داشته باشید. شما fork می‌کنید، تغییرات را روی نسخهٔ خود اعمال می‌کنید، سپس یک Pull Request به مخزن اصلی ارسال می‌کنید.

**گام دوم:**

اکنون وارد مخزن فورک‌شده بروید و پوشه teaching را پیدا کنید.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/teaching-folder-fa526b85db-480.webp 480w, /assets/img/legacy/teaching-folder-fa526b85db-800.webp 800w, /assets/img/legacy/teaching-folder-fa526b85db-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/teaching-folder-fa526b85db.png" alt="teaching_folder"></picture>

</div>

<p class="wp-caption-text">
پوشه teaching</p>

سپس وارد پوشه patterneffort شوید.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/patterneffort-a3aa3ce2a7-480.webp 480w, /assets/img/legacy/patterneffort-a3aa3ce2a7-800.webp 800w, /assets/img/legacy/patterneffort-a3aa3ce2a7-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/patterneffort-a3aa3ce2a7.png" alt="patterneffort"></picture>

</div>

<p class="wp-caption-text">
پوشه patterneffort</p>

**اکنون در این پوشه فایل .md خود را بارگزاری کنید.**

**گام سوم:**
در این مرحله شما باید تصاویری که در فایل مارک‌داون استفاده کردید را در پوشه assets آپلود کنید.

در مخزن، دنبال پوشه assets بگردید.
سپس در پوشه assets، وارد پوشه paterneffort شوید

پوشه مناسب با پروژه خود را ایجاد کنید و فایل‌های تصویری خود را در آن پوشه آپلود کنید.

**نکته:**
در فایل مارک‌داون این مقاله که در حال مطالعه آن هستید، خط زیر وجود دارد:

```
permalink: /teaching/studenteffort/patterneffort/PULL_REQUEST/
```

این یعنی در پوشه assets، باید فایل‌های تصاویر این مارک‌داون، در پوشه PULL_REQUEST باشد.

**گام چهارم:**
در این گام، در صفحه اول مخزن، بر روی گزینه Sync fork بزنید، سپس، گزینه Open pull request را بزنید.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/sync-fork-e0b5acbc2d-480.webp 480w, /assets/img/legacy/sync-fork-e0b5acbc2d-800.webp 800w, /assets/img/legacy/sync-fork-e0b5acbc2d-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/sync-fork-e0b5acbc2d.png" alt="sync_fork"></picture>

</div>

<p class="wp-caption-text">
انجام pull request</p>

در صفحه باز شده روی create pull request کلیک کنید.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/create-pull-request-05539ac31b-480.webp 480w, /assets/img/legacy/create-pull-request-05539ac31b-800.webp 800w, /assets/img/legacy/create-pull-request-05539ac31b-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/create-pull-request-05539ac31b.png" alt="create_pull_request"></picture>

</div>

<p class="wp-caption-text">
create pull request</p>

در مرحله بعد (مهم) شما باید عنوان و یک دلیل را مشخص کنید که تغییری که می‌خواهید بدهید در رابطه با چه چیزی هست.
برای مشخص کردن دلیل باید یکی از سه موارد داده شده را از کامنت در بیاورید. برای مثال در تصویر زیر گزینه دوم از کامنت در آمده است:

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/title-reason-187be673f7-480.webp 480w, /assets/img/legacy/title-reason-187be673f7-800.webp 800w, /assets/img/legacy/title-reason-187be673f7-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/title-reason-187be673f7.png" alt="title_reason"></picture>

</div>

<p class="wp-caption-text">
افزودن عنوان و دلیل</p>

کمی اسکرول کنید و پایین بیاید، برای تایید اینکه می‌خواهید pull request انجام دهید باید تمام بلوک زیر را پاک کنید:

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/confirm-ff9624068a-480.webp 480w, /assets/img/legacy/confirm-ff9624068a-800.webp 800w, /assets/img/legacy/confirm-ff9624068a-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/confirm-ff9624068a.png" alt="confirm"></picture>

</div>

<p class="wp-caption-text">
پاک کردن بلوک برای تایید انجام pull request</p>

در نهایت روی گزینه create pull request کلیک کنید تا درخواست شما توسط مدیر قبول شود.

در صورت تایید مدیر، سپس تایید استاد، می‌توانید پروژه خود را در سایت استاد ببینید.
{% endraw %}
