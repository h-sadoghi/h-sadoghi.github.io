# راهنمای سادهٔ Jupyter Book

این ابزار کتاب Image Processing را در **همان مخزن سایت** مدیریت می‌کند. پوشهٔ `courses/image-processing/book/` یک پوشهٔ عادی است؛ Repository، remote یا GitHub Pages جداگانه ندارد. ابزار Commit و Push انجام نمی‌دهد.

## راه‌اندازی یک‌باره

1. روی `SETUP_JUPYTERBOOK.cmd` دوبار کلیک کنید.
2. پس از پایان نصب، `RUN_JUPYTERBOOK_MANAGER.cmd` را اجرا کنید.

محیط Python فقط در `.venv-jupyterbook` ساخته می‌شود. Python عمومی، Ruby، Bundler و محیط Site Manager تغییر نمی‌کنند. Build عادی Notebookها را اجرا نمی‌کند؛ فقط خروجی‌های ذخیره‌شدهٔ امن آن‌ها را نمایش می‌دهد.

اگر روزی اجرای کد لازم بود، دستور جداگانهٔ `execute-copy` فقط پس از عبارت تأیید `EXECUTE` یک کپی را در `.jupyterbook-manager-runtime/` اجرا می‌کند. نتیجه خودکار وارد سورس یا سایت نمی‌شود. Notebook کد است و با سطح دسترسی کاربر اجرا می‌شود؛ فقط فایل مورد اعتماد خودتان را اجرا کنید.

## افزودن فصل اول Gonzalez با منو

1. فایل واقعی فصل را با پسوند `.md` یا `.ipynb` آماده کنید.
2. `RUN_JUPYTERBOOK_MANAGER.cmd` را اجرا و گزینهٔ «افزودن فایل» را انتخاب کنید.
3. مسیر فایل را وارد کنید.
4. برای مسیر مقصد مثلاً `gonzalez/chapter-01.md` و برای فصل والد `gonzalez/index` را وارد کنید.
5. Preview و Diff را بخوانید. تا وقتی دقیقاً `YES` وارد نکنید چیزی نوشته نمی‌شود.
6. گزینهٔ Validate و سپس Build را اجرا کنید.
7. Preview کتاب در `http://127.0.0.1:4100/` باز می‌شود. این پورت با Jekyll روی 4000 و Site Manager روی 8765 تداخل ندارد.

معادل همان کار در CMD:

```bat
RUN_JUPYTERBOOK_MANAGER.cmd add --file "D:\My Course Files\chapter-01.md" --destination "gonzalez/chapter-01.md" --parent "gonzalez/index"
```

عنوان و توضیح کوتاه اختیاری با `--title` و `--description` ثبت می‌شوند. توضیح در فایل جانبی `_content.yml` می‌ماند تا schema استاندارد `_toc.yml` تغییر نکند.

دستور بالا Dry-run است. پس از بررسی Diff، برای ذخیره `--apply` را به انتهای همان دستور اضافه کنید.

## افزودن دستی و یادگیری `_toc.yml`

1. فایل را در `courses/image-processing/book/gonzalez/` کپی کنید؛ مثلاً `chapter-01.ipynb`.
2. در `courses/image-processing/book/_toc.yml` زیر ورودی `gonzalez/index` این دو خط را با تورفتگی درست اضافه کنید:

```yaml
- file: gonzalez/index
  sections:
    - file: gonzalez/chapter-01
```

پسوند `.md` یا `.ipynb` در `file` اختیاری است و در این پروژه حذف می‌شود. هر مسیر باید یکتا و واقعاً موجود باشد.

3. اجرا کنید:

```bat
RUN_JUPYTERBOOK_MANAGER.cmd validate
BUILD_IMAGE_PROCESSING_BOOK.cmd
```

## تصاویر، PDF و ZIP

برای افزودن امن یک فایل همراه و درج لینک آن در صفحهٔ Markdown:

```bat
RUN_JUPYTERBOOK_MANAGER.cmd asset --file "D:\My Course Files\figure-01.png" --page "gonzalez/chapter-01"
RUN_JUPYTERBOOK_MANAGER.cmd asset --file "D:\My Course Files\chapter-01.zip" --page "gonzalez/chapter-01"
```

ابتدا فقط Preview نمایش داده می‌شود؛ پس از بازبینی، `--apply` اضافه کنید. تصاویر داخل سورس Book قرار می‌گیرند. PDF/ZIP از همان قرارداد سایت و زیر `assets/downloads/courses/image-processing/jupyter-book/` استفاده می‌کنند. ZIP استخراج یا اجرا نمی‌شود، مسیرهای داخلی آن بررسی می‌شوند و ZIP/PDF بیش از ۵۰ مگابایت پذیرفته نمی‌شود؛ تصاویر از محدودیت ۳۲ مگابایتی Site Manager پیروی می‌کنند. بسته‌های فصل Gonzalez که با Site Manager ثبت می‌شوند همچنان در `_data/teaching_packages.yml` و صفحهٔ Gonzalez باقی می‌مانند؛ این ابزار آن سامانه را جایگزین نمی‌کند.

## دستورهای روزمره

```bat
RUN_JUPYTERBOOK_MANAGER.cmd books
RUN_JUPYTERBOOK_MANAGER.cmd tree
RUN_JUPYTERBOOK_MANAGER.cmd validate
RUN_JUPYTERBOOK_MANAGER.cmd build --clean
RUN_JUPYTERBOOK_MANAGER.cmd preview
RUN_JUPYTERBOOK_MANAGER.cmd stop
```

دستور `build --clean` ابتدا کل خروجی قبلی `_build/` را حذف می‌کند تا صفحه‌های قدیمی در انتشار بعدی باقی نمانند. پس از Build سایت اصلی، دستور `stage` تمام خروجی استاندارد Jupyter Book را بدون حذف یا تغییر فایل‌ها در `_site/teaching/image-processing/book/` کپی و برابری فایل‌های مبدأ و مقصد را کنترل می‌کند. همین مرحله فایل خالی `_site/.nojekyll` را نیز می‌سازد تا GitHub Pages پوشه‌های استاندارد `_static` و `_sources` را دوباره با Jekyll حذف نکند.

اجرای اختیاری و جدا از Build برای یک Notebook مورد اعتماد:

```bat
RUN_JUPYTERBOOK_MANAGER.cmd execute-copy --file "gonzalez/chapter-01" --acknowledge-risk EXECUTE
```

برای تغییر ترتیب یک فصل در همان بخش:

```bat
RUN_JUPYTERBOOK_MANAGER.cmd move --file "gonzalez/chapter-01" --position 1
```

این دستور هم ابتدا Dry-run است و برای ذخیره به `--apply` نیاز دارد. پشتیبان هر تغییر در `.jupyterbook-manager-backups/` نگهداری می‌شود و این پوشه وارد Git نمی‌شود.

## مسیر فایل‌های فنی

- تنظیم کتاب: `courses/image-processing/book/_config.yml`
- فهرست چپ: `courses/image-processing/book/_toc.yml`
- عنوان/توضیح مدیریتی: `courses/image-processing/book/_content.yml`
- صفحهٔ ورودی: `courses/image-processing/book/index.md`
- برنامه: `tools/jupyterbook_manager/`
- ثبت کتاب‌ها: `tools/jupyterbook_manager/books.yml`
- وابستگی‌ها: `tools/jupyterbook_manager/requirements.txt`
- خروجی محلی موقت: `courses/image-processing/book/_build/html/`
- مسیر نهایی در سایت واحد: `/teaching/image-processing/book/`

اگر عملیات شکست بخورد، ابزار قبل از نوشتن خطا را اعلام می‌کند. در نوشتن چندفایلی، فایل‌های نوشته‌شده بازگردانده می‌شوند. مسیرهای خارج از مخزن، symlink، نام تکراری، Notebook نامعتبر و ZIP ناامن پذیرفته نمی‌شوند.
