# قرارداد عمومی انتشار فصل / متن درس در Jupyter Book

**تنها پیش‌نیاز:** شناسهٔ درس در `tools/jupyterbook_manager/books.yml` ثبت شده باشد. ابزار به Data Mining محدود نیست. هیچ Push خودکاری اجرا نمی‌شود. **ثبت یک درس کاملاً جدید** (ساخت مسیر و قرارگرفتن در فهرست سایت) وظیفهٔ جداگانهٔ مدیر سایت است؛ ایجاد صفحهٔ درس به معنی ثبت درس نیست.

## ورودی اول: ZIP مستقل فصل

در ریشهٔ ZIP، این اجزا را قرار دهید و هیچ پوشهٔ اضافی در بالا اضافه نکنید:

```text
chapterNN.md
chapter_meta.json
images/
downloads/
```

نمونهٔ متادیتا برای یکی از درس‌های **از قبل ثبت‌شده** (شناسه و مسیر دقیق را مطابق books.yml تعیین کنید):

```json
{
  "schema_version": "standalone-chapter-package-1.0",
  "course_id": "data-mining",
  "entry": "chapter09.md",
  "destination_path": "courses/data-mining/book/course-notes/chapter-09.md",
  "title": "خوشه‌بندی پیشرفته",
  "update_existing": false,
  "images": ["images/fig09_01.png"],
  "downloads": ["downloads/example.py"]
}
```

در متن Markdown، MyST Figure باید **مسیر منبع داخل ZIP** را بنویسد:

````md
```{figure} images/fig09_01.png
:width: 90%

توضیح فارسی شکل
```

[دانلود کد](downloads/example.py)
````

مسیر تصویر هنگام انتشار به `chapter-09-assets/images/fig09_01.png` تبدیل می‌شود. لینک دانلود نسبی `downloads/example.py` به آدرس عمومی مناسب همان درس تبدیل می‌شود. لینک‌های مطلق موجود نیز فقط اگر با مسیر مجاز آن صفحه سازگار باشند پذیرفته می‌شوند. همهٔ فایل‌های ارجاع‌شده باید داخل ZIP باشند. تصاویر و فایل‌هایی که واقعاً در متن معرفی نشده‌اند نیز می‌توانند داخل بسته باشند، اما تنها دانلودهای لینک‌شده به مخزن عمومی منتقل می‌شوند.

## ورودی دوم: یک فایل Markdown ساده

برای متنی که PDF، داده یا تصویر ندارد، نیازی به ZIP نیست. فایل `lesson.md` را ذخیره و شناسهٔ درس ثبت‌شده را به عنوان آرگومان دوم بدهید:

```bat
"J:\SadoghiSite2\h-sadoghi.github.io\RUN_ANY_COURSE.cmd" "J:\Documents\lesson.md" image-processing
```

اگر پوشه‌های `images/` یا `downloads/` کنار همان فایل Markdown باشند، ابزار می‌تواند ارجاعات آن را هم وارد کند. برای جلوگیری از ابهام، هر پوشهٔ دانلود باید شامل فایل‌های با نام یکتا باشد. صفحهٔ موجود بدون `update_existing=true` و `--allow-update` بازنویسی نمی‌شود؛ ورودی `.md` ساده برای افزودن صفحهٔ جدید است.

## اجرای عمومی برای تمام درس‌های ثبت‌شده

```bat
"J:\SadoghiSite2\h-sadoghi.github.io\RUN_ANY_COURSE.cmd" "J:\mycourse\MyChapter.zip"
```

برای نمایش پیش‌نویس بدون نوشتن در مخزن:

```bat
py -3.12 "J:\SadoghiSite2\h-sadoghi.github.io\tools\universal_course_publisher.py" --repo "J:\SadoghiSite2\h-sadoghi.github.io" --source "J:\mycourse\MyChapter.zip" --validate-only
```

**پاسخ موفق:** `[COMMIT VERIFIED]`. سپس فقط `Push origin` در GitHub Desktop را بزنید. انتشار سایت توسط GitHub Actions انجام می‌شود و موفقیت Build سایت باید جداگانه بررسی شود. سایر فایل‌های از پیش Stageشده در Commit اختصاصی این ابزار وارد نمی‌شوند.

## دامنه و محدودیت

- مناسب تمام درس‌هایی است که در **Jupyter Book registry** مخزن ثبت شده‌اند؛ صرفاً ایجاد یک پوشهٔ جدید برای ثبت درس جدید کافی نیست.
- نیازمند Python 3.12 و Git/GitHub Desktop محلی است؛ به شبکه، token یا API نیاز ندارد.
- قالب اصلی برای MyST Markdown است. `.docx`، `.pdf` یا `.tex` را به طور خودکار به صفحات Jupyter Book تبدیل نمی‌کند.
- فایل `_toc.yml` با درج ورودی زیر والد موجود (مثلاً `course-notes/index`) یا در `chapters:` به روز می‌شود؛ فایل CSS یا پیکربندی کتاب بازنویسی نمی‌شود.
- برای ZIP جدید، **محتوای علمی، فرمول‌های MyST و صحت ادعاها** را ابزار تأیید نمی‌کند؛ فقط صحت قرارداد، مسیرها، محتوای اولیهٔ فایل‌ها و ثبت Git کنترل می‌شود.
- CI علاوه بر بررسی لینک‌های عمومی در Commit، دانلودهای معرفی‌شده در فهرست ناشر عمومی را در `_site` کپی می‌کند. اگر سرویس سایت/ثبت درس متفاوت باشد، لازم است یک بار تنظیمات عمومی همان سایت برقرار شود.
