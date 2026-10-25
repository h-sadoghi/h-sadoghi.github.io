# گزارش آزمون Jupyter Book یک‌مخزنی

تاریخ: ۲۰۲۶-۱۰-۲۴

## محیط

- Windows، Python `3.12.6`
- Jupyter Book `1.0.4.post1`
- Sphinx `7.4.7`
- MyST Parser `3.0.1`
- MyST-NB `1.1.2`
- Sphinx Book Theme `1.1.4`
- محیط اختصاصی: `J:/SadoghiSite2/h-sadoghi.github.io/.venv-jupyterbook`

## نتیجهٔ آزمون‌ها

| آزمون                               | نتیجه | شاهد                                                                                                     |
| ----------------------------------- | ----- | -------------------------------------------------------------------------------------------------------- |
| ایجاد venv و نصب pinها              | PASS  | نصب فقط در `.venv-jupyterbook`؛ `pip check` بدون خطا                                                     |
| اجرای مجدد Setup                    | PASS  | پیام `The pinned dependencies are already installed` و خروج 0                                            |
| تست‌های اختصاصی Book Manager        | PASS  | ۱۲ تست با Python محیط Jupyter Book                                                                       |
| تست‌های Site Manager و Book Manager | PASS  | ۵۷ تست با محیط Site Manager؛ جدایی دو venv حفظ شد                                                        |
| YAML و Workflow parsing             | PASS  | تمام Workflowها، دو config، TOC، metadata و registry خوانده شدند                                         |
| Jupyter Book نهایی                  | PASS  | Build بدون warning؛ `execution_mode='off'` در لاگ                                                        |
| Jekyll production build             | PASS  | exit 0 در ۶۹۶٫۸۹۹ ثانیه                                                                                  |
| PurgeCSS محلی                       | PASS  | نسخه 5 روی Windows؛ نسخهٔ جدید 8 در Windows برای مسیر `J:` مشکل ESM داشت، Workflow لینوکس تحت تأثیر نیست |
| Stage ترکیبی                        | PASS  | `index.html` و `_static` زیر `_site/teaching/image-processing/book/`                                     |
| لینک‌های محلی خروجی                 | PASS  | ۱۹۷ HTML، تعداد ۸۰۲۲ لینک داخلی، صفر خطا                                                                 |
| HTTP صفحات اصلی                     | PASS  | هفت URL مربوط به سه صفحهٔ قدیمی، Book و CSS همگی 200                                                     |
| Chrome دسکتاپ                       | PASS  | سه ستون: Navigation چپ، محتوا وسط، TOC راست                                                              |
| Chrome موبایل                       | PASS  | Sidebar به منوی موبایل تبدیل شد؛ `scrollWidth=390` و `clientWidth=390`                                   |
| Preview start/restart/stop          | PASS  | اجرای دوم با پیام اشغال پورت رد شد؛ stop پورت را آزاد کرد؛ restart موفق                                  |
| lock لینوکس                         | PASS  | ۱۰۲ package بررسی شد؛ برای CPython 3.12 هیچ Linux wheel مفقود نبود                                       |
| نبود Repository دوم                 | PASS  | صفر `.git` تو در تو، صفر gitlink و نبود `.gitmodules`                                                    |
| منبع قدیمی Pattern Recognition      | PASS  | ۶۴۹ فایل و سه SHA-256 مبنا بدون تغییر                                                                    |
| Prettier فایل‌های تغییرکرده         | PASS  | پس از format، `prettier --check --ignore-unknown` موفق                                                   |

## آزمون عملی `.md` و `.ipynb`

یک Markdown فارسی/انگلیسی شامل فرمول، کد و تصویر و یک Notebook شامل heading، فرمول، کد و output ذخیره‌شده با خود Book Manager به TOC افزوده شد. Notebook سلولی داشت که در صورت اجرا یک فایل marker می‌ساخت؛ marker ساخته نشد و output ذخیره‌شده در HTML دیده شد. Navigation چپ، TOC راست، تصویر و anchorها در Build دیده شدند.

پس از آزمون، فایل‌های ساختگی، رکوردهای TOC/metadata و تصویر موقت حذف شدند و Book نهایی دوباره Build شد. در سورس و خروجی نهایی هیچ محتوای آزمایشی باقی نمانده است.

## یکپارچه‌سازی URL

مسیرهای زیر در سرور ترکیبی محلی HTTP 200 دادند:

- `http://127.0.0.1:4000/teaching/image-processing/`
- `http://127.0.0.1:4000/teaching/image-processing/gonzalez/`
- `http://127.0.0.1:4000/teaching/image-processing/student-work/`
- `http://127.0.0.1:4000/teaching/image-processing/book/`
- `http://127.0.0.1:4000/teaching/image-processing/book/gonzalez/`
- `http://127.0.0.1:4000/teaching/image-processing/book/student-work/`

Preview مستقیم Book Manager روی `http://127.0.0.1:4100/` نیز HTTP 200 داد. صفحهٔ Jekyll Image Processing دقیقاً یک لینک به Book دارد و سورس خام `courses/` در `_site` کپی نشده است.

## لاگ و Screenshot محلی

این شواهد تولیدی وارد Git نمی‌شوند و در پوشهٔ runtime محلی هستند:

- `.jupyterbook-manager-runtime/jekyll-build.log`
- `.jupyterbook-manager-runtime/book-build-acceptance.log`
- `.jupyterbook-manager-runtime/book-build-final.log`
- `.jupyterbook-manager-runtime/book-desktop.png`
- `.jupyterbook-manager-runtime/book-mobile.png`

هشدارهای Jekyll دربارهٔ excerpt چند سند، citation count خارجی و سه مقصد WebP تکراری از خط پایهٔ قبلی‌اند. Build را متوقف نکردند و به Jupyter Book مربوط نیستند.

## مواردی که عمداً اجرا نشد

- GitHub Actions آنلاین اجرا نشد، زیرا این کار Push را ممنوع کرده است. Workflowها از نظر YAML، ترتیب Build و شرط عدم Deploy در Pull Request به‌صورت محلی آزمون شدند.
- هیچ Push، Merge یا Deploy انجام نشد.
