# قرارداد مستقل بسته‌های فصل Data Mining

**مالک قرارداد:** فایل `tools/data_mining_oneclick.py` در مخزن Git سایت.

برای فصل جدید (مثلاً ۰۷)، فقط یک ZIP با محتویات زیر کافی است:

```text
chapter07.md
chapter_meta.json
images/fig07_01.png
images/...
downloads/DataMining_Chapter07.pdf
downloads/DataMining_Chapter07_TEX_PDF_SOURCE.zip
downloads/chapter07_examples.py
downloads/chapter07_examples.ipynb
...
```

محتویات ZIP باید بدون پوشهٔ اضافی در ریشه باشد (یک پوشهٔ `ChapterNN` نیز قابل تشخیص است). `chapter_meta.json` باید `course_id: "data-mining"`، شمارهٔ فصل، `entry`، `destination_path`، و فهرست `images` و `downloads` را داشته باشد.

در **متن اولیهٔ فصل**، مسیر MyST شکل باید نسبی باشد، مثلاً:

~~~text
```{figure} images/fig07_01.png
:width: 90%

توضیح شکل
```
~~~

ابزار، مسیر تصاویر را فقط هنگام استقرار به `chapter-07-assets/images/` تبدیل می‌کند. لینک فایل‌های دانلود باید دقیقاً به `/assets/downloads/courses/data-mining/course-notes/chapter-07/FILE` اشاره کنند و همان `FILE` داخل `downloads/` ZIP موجود باشد. کلیهٔ لینک‌های عمومی داخل همان فایل Markdown و فهرست `downloads` فراداده باید منطبق باشند.

## روش مستقل از چت

۱. ZIP فصل جدید را دانلود کنید؛ لازم نیست آن را Extract کنید.

۲. در ویندوز، ZIP را روی `RUN_DATA_MINING_ONECLICK.cmd` واقع در **ریشهٔ مخزن سایت** Drag & Drop کنید. یا آن را به‌صورت `ChapterNN.zip` یا `DataMining_ChapterNN_ONECLICK_FINAL.zip` داخل Inbox بگذارید و CMD را دوبارکلیک کنید.

۳. برنامه تمام تصاویر، فراداده، کد و فایل‌های لینک‌شده را پیش از تغییر مخزن بررسی می‌کند؛ سپس Markdown/تصاویر/TOC را برای فصل جدید می‌نویسد و دانلودها را در مسیر واقعی `assets/downloads` قرار می‌دهد.

۴. اگر محیط `.venv-jupyterbook` موجود باشد، ساخت کتاب به‌طور محلی آزمایش می‌شود.

۵. برنامه فایل‌های فصل را در Git index آماده می‌کند. تنها در صورت واردکردن کلمهٔ `COMMIT` یک Commit محلی می‌سازد که **هم متن و هم همهٔ فایل‌های لینک‌شده** را شامل می‌شود. این Commit از نظر وجود فایل‌های مقصد و محتوا کنترل می‌شود.

۶. در GitHub Desktop فقط **Push** کنید. برنامه هرگز خودش Push نمی‌کند.

**فصل‌های قبلی بازنویسی نمی‌شوند** مگر با گزینهٔ صریح `--allow-update` و `update_existing=true` در فراداده. برنامه در اجرای تکراری، پوشهٔ دانلودهای همان فصل را کنترل می‌کند؛ حتی اگر فایل روی هارد موجود ولی هنوز در Git ثبت نشده باشد.

## آزمون و عیب‌یابی

```bat
py -3.12 tools\data_mining_oneclick.py --repo . --source C:\path\Chapter07.zip --validate-only
```

اگر پیام `[VALIDATED]` نمایش داده شود، همهٔ لینک‌های MyST و فایل‌های دانلود ذکرشده در ZIP با قرارداد بسته سازگارند. آزمون ساخت نهایی Jupyter Book و موفقیت GitHub Pages همچنان پس از Commit/Push در CI انجام می‌شود.

این ابزار هیچ تنظیم CSS، Jekyll، GitHub Actions یا محتوای فصول پیشین را تغییر نمی‌دهد و از نصب کتابخانهٔ Python اضافی برای مرحلهٔ اعتبارسنجی و واردکردن استفاده نمی‌کند.
