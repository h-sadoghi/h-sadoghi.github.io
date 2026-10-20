# گزارش آزمون Sadoghi Local Jekyll Content Manager

تاریخ: ۲۰۲۶-۱۰-۱۹؛ به‌روزرسانی پیش‌نمایش Jekyll: ۲۰۲۶-۱۰-۲۰

شاخه: `feature/local-jekyll-manager-mvp-20261019`

مبنای شاخه: `0f366dce12dc69e29c3cfb73e74de1227ce1ff35`

پوشهٔ آزمون و شواهد: `J:\SadoghiSite2\site_manager_audit_20261019`

## نتیجه

MVP در مخزن واقعی نصب شده و مسیر یک‌کلیکی، API، Preview، diff، ذخیرهٔ تأییدشده، پشتیبان، جست‌وجو، ویرایش و اعتبارسنجی کار می‌کنند. هیچ فایل محتوایی موجود، مقاله، تصویر، navigation یا theme در جریان ساخت و آزمون تغییر نکرده است. تغییر `_config.yml` فقط ابزار و گزارش‌های محلی را از خروجی عمومی Jekyll مستثنا می‌کند.

## آزمون‌های خودکار

فرمان:

```powershell
.\.site-manager-venv\Scripts\python.exe -m pytest tools\site_manager\tests -q
```

نتیجهٔ اولیه: `18 passed in 1.30s`. پس از افزودن مدیریت فرایند Jekyll، اجرای نهایی `21 passed in 0.96s`، exit code صفر بود.

سناریوهای پوشش‌داده‌شده:

- Markdown فارسی همراه دو تصویر و نام فایل دارای فاصله؛ Preview هیچ فایلی را تغییر نداد.
- Import واقعی multipart از فرم مرورگر با `DFT.md` و دو تصویر.
- پست draft با نام تاریخ‌دار و `published: false`.
- پروژه، منبع و مدخل خودکار `_data/legacy_resources.yml`.
- جلوگیری از overwrite، عنوان تکراری، route ناشناخته و مسیر خارج از مخزن.
- حفظ permalink، کد fenced، فرمول و Liquid هنگام ویرایش.
- ویرایش fragment پروفایل بدون افزودن front matter ناخواسته.
- رد تصویر جعلی که محتوایش با پسوند سازگار نیست.
- تشخیص کلید، DOI و عنوان/سال تکراری در BibTeX.
- ذخیره فقط با `confirm=True` و ساخت manifest پشتیبان.
- صفحهٔ اصلی، جست‌وجوی JSON و پیش‌نمایش سریع Markdown در Flask.
- اجرای Jekyll با `--unpublished`، استفادهٔ مجدد از PID موجود، توقف کامل فرایند و تشخیص اشغال پورت 4000.

## کنترل مخزن واقعی

فرمان اعتبارسنجی `SiteManager.validate()` روی کل محتوای فعلی:

```text
quick_validation_ok=True errors=0 warnings=0
```

کنترل مستقل بانک مقاله با Pybtex و parser داخلی:

```text
pybtex_entries=216 custom_entries=216
bibliography_duplicate_issues=[]
```

exit code صفر؛ زمان ۲٫۱۷۸ ثانیه. Log: `repository-validation.log`.

Preview واقعی یک یادداشت فارسی «Teaching > Signals and Systems» این چهار تغییر را بدون نوشتن تولید کرد:

1. فایل Markdown زیر `_pages/resources/`؛
2. دو تصویر زیر `assets/img/content/<slug>/`؛
3. یک مدخل افزوده در `_data/legacy_resources.yml` با diff محدود به شش خط.

مسیر PDF به‌طور جداگانه `assets/pdf/content/<slug>/` است. تصاویر در مسیر ورودی ImageMagick موجود سایت قرار می‌گیرند.

## قالب‌بندی، syntax و اجرای یک‌کلیکی

- `python -m compileall -q tools\site_manager`: exit code صفر.
- `git diff --check`: exit code صفر.
- Prettier روی همهٔ فایل‌های پشتیبانی‌شدهٔ تغییرکرده: موفق، exit code صفر، ۲٫۸۸۸ ثانیه. Log: `prettier.log`.
- `RUN_SITE_MANAGER.cmd` با همان venv واقعی اجرا شد؛ درخواست HTTP به `http://127.0.0.1:8765/` پاسخ `200` و عنوان درست گرفت.
- سرور فقط به `127.0.0.1:8765` bind می‌شود.
- Ruby+Devkit `3.3.12-1`، Bundler `2.5.7` و ImageMagick `7.1.2-34 Q16-HDRI` در مسیر کاربر نصب و کنترل شدند. `bundle check` موفق است و platform ویندوز `x64-mingw-ucrt` به lockfile افزوده شد.
- پیش‌نمایش Jekyll واقعی از دکمه/API ابزار اجرا شد، روی `127.0.0.1:4000` به حالت `ready` رسید و پس از آزمون توقف و اجرای مجدد با PID `16844` روشن ماند.
- صفحهٔ آزمایشی `published: false` در `/resources/teaching-signals-signal-test-20261019/` پاسخ 200 داد. دو تصویر PNG آن نیز پاسخ 200 با اندازه‌های 60,805 و 93,609 بایت دادند.
- اجرای تکراری همان PID را با `reused: true` نگه داشت. توقف آزمایشی، PID و listener پورت 4000 را کامل حذف کرد؛ اجرای بعدی دوباره موفق شد.

## بازبینی تصویری

صفحهٔ آزمایشی با `webbrowser` در Google Chrome باز شد و عنوان پنجرهٔ واقعی مرورگر `آزمایش سیگنال سینوسی و انتقال زمانی | Hadi Sadoghi Yazdi` کنترل شد. پاسخ‌های HTTP صفحه و هر دو تصویر نیز مستقل بررسی شدند. رابط Computer Use این نشست ابزار callable نداشت؛ شاهد تصویری پیشین رابط Flask همچنان موجود است.

شاهد: `J:\SadoghiSite2\site_manager_audit_20261019\SITE_MANAGER_HOME.png` (۶۵٬۴۶۶ بایت).

## فایل‌های تغییرکرده

- زیرساخت اجرا: `RUN_SITE_MANAGER.cmd`، `.gitignore` و بخش exclude در `_config.yml`.
- بستهٔ ابزار: ۲۳ فایل زیر `tools/site_manager/` شامل router، importer، asset handler، front matter، bibliography، validator، inspector، manager، Flask UI، قالب‌ها، تنظیم route، راهنما و tests.
- معماری اطلاعات: `SITE_INFORMATION_ARCHITECTURE_PROPOSAL.md` و موجودی ۲۰۴ سطری `SITE_INFORMATION_ARCHITECTURE_INVENTORY.csv`.
- همین گزارش آزمون.

فایل `SADOGHI_LOCAL_JEKYLL_MANAGER_SPEC.md` ورودی کاربر است، حفظ شده و در این پیاده‌سازی تغییر نکرده است.

## محدودیت‌های صادقانه

- برای شروع سریع authoring، فایل موقت `.site-manager-runtime/jekyll-preview.yml` فقط در پیش‌نمایش محلی تبدیل انبوه WebP، دریافت منابع خارجی، badgeهای شبکه‌ای و تبدیل notebook نمونه را غیرفعال می‌کند. `_config.yml` و رفتار build عمومی تغییر نکرده‌اند.
- افزودن کارت People، رکورد ساختاری پایان‌نامه و تغییر navigation عمداً خودکار نشده‌اند و به تصمیم جداگانهٔ مالک نیاز دارند.
- ابزار local-only است؛ Commit، Push، PR، Merge و Deploy ندارد.
