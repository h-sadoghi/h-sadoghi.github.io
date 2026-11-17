# قرارداد ثابت کارخانهٔ محتوای دروس — نسخه ۱

این ابزار برای **تمام درس‌های از قبل ثبت‌شده** در `tools/jupyterbook_manager/books.yml` مشترک است و فایل برنامهٔ موجود `tools/universal_course_publisher.py` را برای انتقال به Git استفاده می‌کند. ابزار مستقل از چت است.

## رابط ثابت CMD

- `RUN_COURSE_FACTORY.cmd NEW data-mining 12 "عنوان فصل"` فضای نگارش فصل ۱۲ را **خارج از Git** می‌سازد.
- `RUN_COURSE_FACTORY.cmd "C:\path\to\Chapter12"` از فایل Markdown موجود PDF فارسی با XeLaTeX می‌سازد، ZIP بسته‌بندی می‌کند، کنترل می‌کند و با تأیید `COMMIT` یک Commit محلی ایجاد می‌کند.
- `RUN_COURSE_FACTORY.cmd "C:\path\to\Chapter12_ONECLICK.zip"` بستهٔ آماده را کنترل و در Git محلی منتشر می‌کند، بدون استخراج و بدون بازنویسی PDF.
- `RUN_COURSE_FACTORY.cmd CHECK "C:\path\to\Chapter12_ONECLICK.zip"` فقط کنترل می‌کند؛ Git تغییر نمی‌کند.

## اجزای فضای نگارش / ZIP

```text
chapterNN.md
chapter_meta.json
images/
downloads/
```

در فایل `chapter_meta.json`، `course_id` باید یکی از شناسه‌های موجود در `books.yml` باشد. مسیر `destination_path` باید زیر همان کتاب باشد. فصل موجود بدون فعال‌شدن آگاهانهٔ `update_existing` جایگزین نمی‌شود. **نوشتهٔ علمی را ابزار خودکار نمی‌سازد**: ابتدا آن را به کمک روش تألیف دلخواه (نویسنده، Codex، Claude یا ChatGPT) در Markdown بنویسید.

## PDF فارسی و وابستگی‌ها

اگر ورودی پوشهٔ نگارش باشد، ابزار از `Pandoc` برای تبدیل MyST Markdown به LaTeX و از `XeLaTeX` و بستهٔ `xepersian` برای PDF استفاده می‌کند. `Amiri` و `DejaVu Sans` قلم‌های پیش‌فرض‌اند؛ اگر قلم دیگری در سیستم نصب است، قبل از اجرا در CMD از `set "COURSE_PERSIAN_FONT=..."` استفاده کنید. استفاده از ZIP آماده به Pandoc/XeLaTeX نیازی ندارد چون PDF قبلاً در آن است.

در تبدیل PDF، بلوک‌های ` ```{figure}` به تصویر Pandoc تبدیل می‌شوند؛ بررسی نهایی PDF با مدرس الزامی است. همهٔ دستورهای MyST ممکن است در چاپ دقیقاً همان ظاهر Jupyter Book را نداشته باشند؛ برای PDF دارای صفحه‌بندی خاص می‌توانید سورس مستقل TeX در ZIP بگذارید و PDF را پیشاپیش بسازید.

## مرزهای تضمین

«Commit محلی تأیید شد» با «GitHub Pages منتشر شد» یکی نیست. پس از `Push origin` اجرای `Deploy site`، `Prettier` و `Check for broken links` باید سبز باشند. برنامه هیچ Push، دسترسی حساب کاربری یا فراخوانی LLM مخفی انجام نمی‌دهد. ابزار ابتدا خود بسته را کنترل می‌کند؛ بررسی علمی، دقت منابع و کیفیت آموزشی مسئولیت مرحلهٔ تألیف است.
