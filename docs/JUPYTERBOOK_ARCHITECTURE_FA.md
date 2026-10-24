# معماری یک‌مخزنی Jupyter Book برای Image Processing

## مرز مخزن

تنها Repository پروژه همان `J:/SadoghiSite2/h-sadoghi.github.io` است. سورس کتاب در `courses/image-processing/book/` یک پوشهٔ عادی زیر همین ریشه است. هیچ `.git`، remote، submodule، subtree، worktree دائمی یا GitHub Pages جدا برای کتاب وجود ندارد.

مسیر انتخاب‌شده همان پیشنهاد اولیه است، زیرا:

- سورس Jupyter Book را از صفحه‌های Jekyll در `_pages/courses/` جدا نگه می‌دارد؛
- با قرارداد downloadهای موجود در `assets/downloads/courses/image-processing/` تداخل ندارد؛
- برای کتاب درس‌های آینده قابل تعمیم است؛
- کل پوشه را می‌توان در Jekyll `exclude` کرد و فقط خروجی Build را در artifact نهایی قرار داد.

## دو `_config.yml` مستقل

| فایل                                         | مصرف‌کننده              | نقش                                                                   |
| -------------------------------------------- | ----------------------- | --------------------------------------------------------------------- |
| `/_config.yml`                               | Jekyll/al-folio و Ruby  | صفحه‌های سایت، collectionها، پلاگین‌ها، URL و ساخت `_site`            |
| `/courses/image-processing/book/_config.yml` | Jupyter Book 1.x/Sphinx | عنوان کتاب، اجرای خاموش Notebook، قالب سه‌ستونه و repository metadata |

پلاگین `jekyll-jupyter-notebook` در تنظیم Jekyll برای صفحه‌های قبلی است و جایگزین فرمان `jupyter-book build` نمی‌شود. ابزار همیشه مسیر پوشهٔ کتاب را صریح به Jupyter Book می‌دهد تا فایل ریشه اشتباه خوانده نشود.

## سورس و Navigation

```text
courses/image-processing/book/
├── _config.yml              # فقط Jupyter Book
├── _toc.yml                 # ستون چپ و ترتیب فصل‌ها
├── index.md                 # صفحهٔ ورودی کتاب
├── gonzalez/
│   └── index.md
└── student-work/
    └── index.md
```

ستون چپ از `_toc.yml`، ستون وسط از `.md` یا `.ipynb` و ستون راست از headingهای همان صفحه ساخته می‌شود. `execute.execute_notebooks: "off"` مانع اجرای خودکار سلول‌هاست؛ output ذخیره‌شدهٔ Notebook می‌تواند نمایش داده شود.

صفحات Jekyll زیر حفظ شده‌اند و کتاب جایگزین آن‌ها نیست:

- `/teaching/image-processing/`
- `/teaching/image-processing/gonzalez/`
- `/teaching/image-processing/student-work/`

صفحهٔ اول یک پیوند به `/teaching/image-processing/book/` دارد. ZIP/PDFهای فصل Gonzalez همچنان با `_data/teaching_packages.yml` و Site Manager مدیریت می‌شوند. ابزار کتاب برای فایل‌های همراه خود از همان ریشهٔ download سایت استفاده می‌کند و سامانهٔ داده‌ای موازی برای بسته‌های ثبت‌شده نمی‌سازد.

## محیط Python

- نسخهٔ آزموده‌شده: Python 3.12 و Jupyter Book `1.0.4.post1`.
- محیط محلی: `.venv-jupyterbook/`، خارج از Git.
- pinهای مستقیم: `tools/jupyterbook_manager/requirements.txt`.
- constraintهای سازگاری Sphinx/MyST: `tools/jupyterbook_manager/constraints.txt`.
- ورودی CI لینوکس: `tools/jupyterbook_manager/requirements-ci.txt`.
- lock کامل آزموده‌شده در `requirements-lock.txt` ثبت شده است. همین مجموعه برای وجود wheelهای CPython 3.12 لینوکس نیز جداگانه resolve/download می‌شود و CI از آن استفاده می‌کند.

`SETUP_JUPYTERBOOK.cmd` idempotent است: اگر نسخه‌های اصلی درست باشند دوباره نصب نمی‌کند، سپس `pip check` و نسخه Jupyter Book را کنترل می‌کند.

## ابزار مدیریت

`tools/jupyterbook_manager/` یک برنامهٔ argparse و منوی تعاملی فارسی دارد:

- `books` و `tree`: شناخت مسیرهای واقعی و ساختار YAML؛
- `validate`: YAML، TOC، فایل‌ها، Notebook، لینک محلی، مسیر و مخزن تو در تو؛
- `add`: افزودن `.md`/`.ipynb` موجود به TOC با Dry-run؛
- `move`: تغییر ترتیب یا عنوان بدون حذف محتوا؛
- `asset`: افزودن امن تصویر/PDF/ZIP و لینک Markdown؛
- `build`: Build بدون اجرای Notebook؛
- `preview`/`stop`: سرور مستقل روی پورت 4100؛
- `stage`: اتصال خروجی کتاب به `_site` پس از آخرین Build Jekyll.

نوشتن فقط با `--apply` یا تأیید دقیق `YES` انجام می‌شود. تغییر چندفایلی پشتیبان دارد، با فایل موقت و `os.replace` نوشته می‌شود و در خطا rollback می‌شود. برنامه Commit یا Push ندارد.

## ترتیب Build و انتشار واحد

Workflow اصلی با این ترتیب کار می‌کند:

```text
checkout
→ Ruby/Bundler + Python 3.12
→ ImageMagick
→ bundle exec jekyll build        # _site ساخته/پاک‌سازی می‌شود
→ PurgeCSS                        # آخرین تغییر عمومی Jekyll
→ jupyter-book build courses/image-processing/book
→ manager stage ... --site-dir _site
→ verify index.html + _static
→ link check (در PR)
→ یک artifact از _site
→ deploy فقط برای push به master/main
```

در Pull Request مرحلهٔ Deploy موجود به‌علت شرط `github.event_name != 'pull_request'` اجرا نمی‌شود. هیچ Workflow دوم برای انتشار کتاب ساخته نشده است.

Jekyll پوشهٔ `courses/` را exclude می‌کند، پس Markdown، Notebook، `_toc.yml` و `_config.yml` کتاب به‌صورت خام یا تکراری وارد سایت نمی‌شوند. Stage بعد از Jekyll، تمام `_static` و `_images` ساخته‌شده را زیر `_site/teaching/image-processing/book/` کپی می‌کند.

دو فایل `sbt-webpack-macros.html` و `webpack-macros.html` قالب‌های Jinja زمان Build هستند، صفحهٔ runtime نیستند و دارای `{{ pathto(...) }}` حل‌نشده‌اند. Stage فقط همین دو فایل غیرقابل‌انتشار را از کپی `_static` حذف می‌کند تا link checker آن‌ها را با صفحهٔ واقعی اشتباه نگیرد؛ CSS، JavaScript، فونت و تصویرهای runtime حفظ می‌شوند.

## URLهای محلی و نهایی

- Preview مستقیم کتاب: `http://127.0.0.1:4100/`
- Jekyll محلی: `http://127.0.0.1:4000/`
- Site Manager: `http://127.0.0.1:8765/`
- مسیر نهایی کتاب در سایت واحد: `https://h-sadoghi.github.io/teaching/image-processing/book/`

لینک بازگشت کتاب به `/teaching/image-processing/` مطلق از ریشهٔ همین دامنه است. PDF/ZIP نیز با URL ریشه‌ای `/assets/downloads/courses/...` به artifact واحد اشاره می‌کنند.

## تفاوت با Pattern Recognition قدیمی

منبع قدیمی الگوی `jb-book` را تأیید کرد، اما `execute_notebooks: force` داشت، دو کلید `latex` تکراری داشت، نسخه‌ها را pin نکرده بود و به preprocessor موجودنبودۀ `hide_all_cells` اشاره می‌کرد. معماری جدید ساختار Navigation سازگار را نگه می‌دارد، ولی اجرای خودکار و وابستگی ناقص را منتقل نمی‌کند.
