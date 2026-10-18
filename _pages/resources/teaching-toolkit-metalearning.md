---
layout: legacy_page
title: فرایادگیری
permalink: /resources/teaching-toolkit-metalearning/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/toolkit/MetaLearning/
legacy_group: Research toolkit
legacy_dir: rtl
lang: fa
---

{% raw %}

# فرا یادگیری (Meta-Learning)

🤔 متا یادگیری = یادگیریِ چگونه یاد گرفتن

متا یادگیری = تمرین روی کارهای متعدد با داده کم، تا یاد بگیریم برای کارهای جدید با داده کم چطور سریع یاد بگیریم.

نکته کلیدی: هدف متا یادگیری به‌روزرسانی پارامترهای مدل نیست، بلکه به‌روزرسانی فرایند یادگیری مدل است!

آیا درست فهمیدم؟

فرض که دیتا ست mnist داریم و می خواهیم این روش را بکار بندیم

task
ها را اموزش شبکه ای روی جفت کلاسها می دانیم لذا چندین نمونه که کلاس 1 و 2 هستند
تسک دوم مثلا کلاس 2 و 5 به تعداد 20 تا و ... اینها می شوند دیتا ست ما که شبکه می آموزد

حالا کارکتر A, B
را با
support set
این که در اختیار قرار می دهند مثلا 15 نمونه می دهیم به همان شبکه قبلی که تا بحال آموزش دیده روی Mnist
و اموزش می بیند و
حالا اماده ایم که
query
داده شود تا ببینیم چقدر توانا هستیم

🎯 چه زمانی از متا یادگیری استفاده کنم؟
✅ وقتی که:

- کارهای مشابه اما متفاوت زیاد دارید

- برای هر کار داده کمی دارید

- می‌خواهید روی کارهای جدید سریع سازگار شوید

🎯 چه زمانی از متا یادگیری استفاده نکنم؟
❌ وقتی که:

- فقط یک کار دارید

- داده کافی دارید

- نیاز به یادگیری یک چیز خاص دارید

فرا یادگیری را می‌توان از چندین دیدگاه تعریف کرد. دو دیدگاه اصلی را بررسی می‌کنیم:

- الف) **توزیع وظایف (Task Distribution)**
- ب) **بهینه‌سازی دو سطحی (Bilevel Optimization)**

---

## ۱. چارچوب ریاضی

فرا یادگیری را می‌توان به عنوان یک مسئله بهینه‌سازی روی توزیع وظایف \( \mathcal{T} \) تعریف کرد:

\[
\min*{\omega} \mathbb{E}*{\mathcal{T} \sim p(\mathcal{T})} \mathcal{L}(D; \omega)
\]

که در آن:

- \( \omega \) **فرادانش (Meta-Knowledge)** است.
- \( \mathcal{T} = \{D, L\} \) شامل یک مجموعه‌داده \( D \) و یک تابع هزینه \( L \) است.

---

## ۲. مراحل فرا یادگیری

در فرایند فرا یادگیری دو گام اصلی وجود دارد:

### الف) **فرا-یادگیری (Meta-Training)**

در این مرحله، از مجموعه‌داده‌های منبع (source) استفاده می‌شود:

\[
D*{\text{source}} = \{(D*{\text{source train}}, D*{\text{source val}})^{(i)}\}*{i=1}^{S}
\]

- \( D\_{\text{source train}} \) مجموعه پشتیبان (**Support Set**)
- \( D\_{\text{source val}} \) مجموعه پرسش (**Query Set**)

### ب) **فرا-آزمون (Meta-Testing)**

در این مرحله، روی مجموعه‌داده‌های هدف (target) ارزیابی انجام می‌شود:

\[
D*{\text{target}} = \{(D*{\text{target train}}, D*{\text{target test}})^{(i)}\}*{i=1}^{G}
\]

- \( D\_{\text{target train}} \) مجموعه پشتیبان (**Support Set**)
- \( D\_{\text{target test}} \) مجموعه پرسش (**Query Set**)

---

## ۳. تفاوت با روش‌های کلاسیک یادگیری ماشین

برخلاف روش‌های معمول یادگیری ماشین، در فرا یادگیری هر مجموعه‌داده نیاز به طراحی دقیق دارد و ساختار وظایف (tasks) به گونه‌ای تنظیم می‌شود که شبیه به سناریوی تست نهایی باشد.

---

## ۴. مفهوم k-way n-shot

در تنظیم فرا یادگیری، **k-way n-shot** به معنای استفاده از \( k \) کلاس مختلف و \( n \) نمونه از هر کلاس در مجموعه پشتیبان (support set) مرحله فرا-آزمون است.

---

## ۵. نمودار مفهومی فرا یادگیری

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/meta1-b9da100965-480.webp 480w, /assets/img/legacy/meta1-b9da100965-800.webp 800w, /assets/img/legacy/meta1-b9da100965-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/meta1-b9da100965.jpg" alt="meta1"></picture>

</div>

<div class="caption" markdown="1">

    فرا-یادگیری

</div>

{% endraw %}
