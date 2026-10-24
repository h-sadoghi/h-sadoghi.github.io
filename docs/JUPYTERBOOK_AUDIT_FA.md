# ممیزی Jupyter Book و مخزن اصلی

تاریخ ممیزی: ۲۰۲۶-۱۰-۲۴

## وضعیت Git پیش از تغییر

- ریشهٔ تنها مخزن: `J:/SadoghiSite2/h-sadoghi.github.io`
- شاخهٔ مبنا هنگام شروع: `feature/image-processing-three-pages-20261021`
- HEAD مبنا: `a96abb8f30a9385a178cf7503dcbca1964433806`
- شاخهٔ کاری جدید: `feature/jupyterbook-one-repo-20261024`
- `origin/master`: `a1bca1bdf47915f51f095c65a7838f96fca7336c`
- شاخهٔ کاری دو Commit محلی `1446d03` و `a96abb8` را روی `origin/master` حفظ می‌کند.
- `origin` و `upstream` هر دو به `https://github.com/h-sadoghi/h-sadoghi.github.io.git` اشاره می‌کنند.
- هیچ Submodule، ورودی gitlink یا `.git` تو در تو پیدا نشد.
- فایل دستور این کار ورودی محلی است و عمداً وارد Commit نمی‌شود.

## مخزن Jekyll/al-folio

- `_config.yml` ریشه، تنظیم Jekyll است و افزونهٔ Ruby با نام `jekyll-jupyter-notebook` دارد. این افزونه Jupyter Book نیست.
- Build/Deploy اصلی در `.github/workflows/deploy.yml` ابتدا Ruby 3.2.2 و ImageMagick را آماده می‌کند، سپس `bundle exec jekyll build` را اجرا و تنها `_site` را منتشر می‌کند.
- Workflow در Pull Request همان Build را انجام می‌دهد ولی مرحلهٔ Deploy به‌صراحت اجرا نمی‌شود.
- پوشهٔ `tools/` و ابزار Site Manager در خروجی Jekyll مستثنی هستند. پیش از این کار، `courses/` وجود نداشت و مستثنی نشده بود.
- Site Manager از محیط محلی `.site-manager-venv` استفاده می‌کند. این محیط از محیط جدید Jupyter Book مستقل می‌ماند.
- سه نشانی موجود و فایل‌های منبعشان تأیید شدند:
  - `/teaching/image-processing/` ← `_pages/courses/image-processing.md`
  - `/teaching/image-processing/gonzalez/` ← `_pages/courses/image-processing-gonzalez.md`
  - `/teaching/image-processing/student-work/` ← `_pages/courses/image-processing-student-work.md`
- ZIP/PDFهای Gonzalez در `_data/teaching_packages.yml` و آثار دانشجویان در `_data/teaching_student_works.yml` ثبت می‌شوند. فایل‌ها زیر `assets/downloads/courses/...` قرار می‌گیرند.

## منبع قدیمی Pattern Recognition (فقط خواندنی)

- مسیر بررسی‌شده: `D:/Part 3/Students_EXT/PhDStudent/Sadoghi/SadoghiSite/PatternRecognition_S`
- شمار کل فایل‌ها با خروجی قدیمی `_build`: ۶۴۹ فایل، در مجموع ۵۷٬۴۵۵٬۰۲۲ بایت.
- `_toc.yml` از `format: jb-book`، ریشهٔ `pattern_recognition.ipynb` و ساختار `chapters`/`sections` استفاده می‌کند.
- `_config.yml` اجرای Notebook را روی `force` گذاشته، لوگو، favicon، BibTeX و preprocessor سفارشی `hide_all_cells.HideAllCellsPreprocessor` را اعلام می‌کند.
- فایل `hide_all_cells.py` یا بستهٔ محلی متناظر در منبع پیدا نشد. کتاب جدید به این preprocessor ناقص وابسته نمی‌شود.
- کلید `latex` در `_config.yml` قدیمی دو بار تعریف شده است؛ YAML معمولی مقدار اول را با دومی می‌پوشاند. طبق دستور، فایل قدیمی تغییر نکرد.
- `requirements.txt` قدیمی فقط `jupyter-book`, `matplotlib`, `numpy` را بدون نسخه pin کرده است. نسخهٔ دقیق محیط سازنده در فایل‌ها ثبت نشده و محیط مجازی همراه پروژه نیست. خروجی قدیمی قالب Sphinx Book Theme را نشان می‌دهد، اما از آن نمی‌توان نسخهٔ دقیق Jupyter Book را با اطمینان استخراج کرد.
- `jupyter-book` روی PATH عمومی این رایانه نصب نبود. نسخهٔ قدیمی از همین پوشه اجرا یا تغییر داده نشد.

### اثر انگشت منبع قدیمی پیش از کار

| فایل               | SHA-256                                                            |
| ------------------ | ------------------------------------------------------------------ |
| `_config.yml`      | `07F868B4EE27314980F97C7199D79641241765E8CB0C212F010E7618F68ACFF6` |
| `_toc.yml`         | `890EDE66674724404CC0C1CF93E6C4F1314DC1D8FB6FDC29453E63FCCF26D7B2` |
| `requirements.txt` | `7D5DF3A8E5BC43701C8CD393C26A713531D01FD290E3E5E6EBC7995AED999BA2` |

## انتخاب فنی تأییدشده

- Pythonهای 3.11، 3.12 و 3.13 نصب‌اند؛ Python 3.12.6 نسخهٔ فعال و گزینهٔ اول محیط جداگانه است.
- نسخهٔ 1.x موجود در PyPI، `jupyter-book==1.0.4.post1` است. نصب و Build عملی آن در محیط `.venv-jupyterbook` معیار pin نهایی خواهد بود.
- سورس کتاب در `courses/image-processing/book/` قرار می‌گیرد. این مسیر با صفحات Jekyll و مسیر downloadهای موجود تداخل ندارد و همهٔ فایل‌ها زیر همان `git rev-parse --show-toplevel` باقی می‌مانند.
- اجرای پیش‌فرض Notebookها `off` خواهد بود. Import، اعتبارسنجی، Build و Preview عادی هیچ سلولی را اجرا نمی‌کنند.
- خروجی ساخته‌شدهٔ کتاب داخل Git نگهداری نمی‌شود. در Build ترکیبی، Jekyll ابتدا `_site` را می‌سازد و سپس خروجی Book به `_site/teaching/image-processing/book/` کپی می‌شود.
