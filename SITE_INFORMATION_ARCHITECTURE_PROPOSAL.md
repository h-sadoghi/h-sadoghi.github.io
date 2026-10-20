# پیشنهاد معماری اطلاعات سایت

تاریخ ممیزی: ۲۰۲۶-۱۰-۱۹

مبنای Git: `0f366dce12dc69e29c3cfb73e74de1227ce1ff35` (نسخهٔ reviewed مربوط به PR #4)

وضعیت این سند: **صرفاً پیشنهاد؛ هیچ جابه‌جایی، حذف، redirect یا تغییر navigation انجام نشده است.**

## موجودی واقعی

اسکن بازگشتی محتوای Jekyll این موارد را پیدا کرد:

| نوع واقعی                     |  تعداد | محل                                                       |
| ----------------------------- | -----: | --------------------------------------------------------- |
| صفحات منبع مستقل              |    ۱۲۵ | `_pages/resources/*.md`                                   |
| سایر صفحات و fragmentها       |     ۵۶ | `_pages/*.md`                                             |
| پست وبلاگ                     |      ۸ | `_posts/*.md`                                             |
| پروژه                         |     ۱۲ | `_projects/*.md`                                          |
| خبر کوتاه                     |      ۳ | `_news/*.md`                                              |
| رکورد انتشار                  |    ۲۱۶ | `_bibliography/papers.bib`                                |
| مدخل فهرست کتابخانه           |    ۱۳۱ | `_data/legacy_resources.yml`                              |
| رکورد پژوهش دانشجویی          |     ۷۴ | `_data/student_research.yml`؛ ۶۰ کارشناسی ارشد و ۱۴ دکتری |
| موضوع پژوهشی                  | ۵ گروه | `_data/research_topics.yml`                               |
| fragment پروفایل مورد استفاده |     ۳۹ | ارجاع‌شده از `_pages/profiles.md`                         |
| فایل تصویر در `assets/img`    |   ۱۰۷۰ | همهٔ زیرشاخه‌های `assets/img/`                            |

فهرست سطری ۲۰۴ فایل Markdown در `SITE_INFORMATION_ARCHITECTURE_INVENTORY.csv` ثبت شده است. هیچ خطای parse front matter و هیچ permalink تکراری یافت نشد. بانک BibTeX نیز کلید، DOI یا زوج عنوان/سال تکراری ندارد.

## نگاشت صفحات و خانهٔ canonical پیشنهادی

| صفحه یا خانوادهٔ فعلی                | دستهٔ ترجیحی                       | خانهٔ canonical که باید حفظ شود                              | ریسک تکرار یا redirect                                                                             |
| ------------------------------------ | ---------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| `/` از `_pages/about.md`             | Home / About / Contact             | `/`                                                          | Contact اکنون بخشی از About است؛ صفحهٔ جدا لازم نیست مگر با تصمیم مالک.                            |
| `/cv/`                               | Home / CV                          | `/cv/`                                                       | کم؛ URL موجود حفظ شود.                                                                             |
| `/publications/`                     | Research / Publications            | `/publications/`                                             | تنها بانک canonical مقالات، `_bibliography/papers.bib` است.                                        |
| `/research-topics/`                  | Research / themes                  | `/research-topics/`                                          | نمای موضوعی است و نباید رکورد مقاله را تکرار کند.                                                  |
| `/projects/` و ۱۲ فایل `_projects`   | Research / Projects                | `/projects/` و URL هر پروژه                                  | شش مدخل «Engineering projects» در Library ممکن است توضیح تکمیلی باشند؛ ادغام فقط پس از تطبیق مالک. |
| `/repositories/`                     | Research / software                | `/repositories/`                                             | کم؛ می‌تواند cross-link از Projects داشته باشد.                                                    |
| `/people/` و ۳۹ fragment             | People & Students / People         | `/people/`                                                   | fragmentها صفحهٔ مستقل نیستند؛ ابزار در ویرایش، نبود front matter را حفظ می‌کند.                   |
| `/student-research/` و ۷۴ رکورد داده | People & Students / thesis archive | `/student-research/`                                         | تاریخچه است و نباید با وضعیت فعلی افراد یکی فرض شود.                                               |
| `/laboratory-gallery/`               | People & Students / history        | `/laboratory-gallery/`                                       | cross-link از People کافی است.                                                                     |
| `/teaching/`                         | Teaching / courses                 | `/teaching/`                                                 | پنج پیوند دورهٔ بیرونی و Library مکمل‌اند؛ محتوا کپی نشود.                                         |
| ۷۶ مدخل آموزشی در Library            | Teaching / notes                   | URL مستقل هر منبع زیر `/resources/`                          | canonical همان صفحهٔ منبع است؛ Teaching فقط باید پیوند بدهد.                                       |
| `/presentations/` و ۱۶ ارائه         | Library / presentations            | `/presentations/` به‌عنوان index؛ URL هر منبع به‌عنوان محتوا | فهرست از `_data/legacy_resources.yml` تولید می‌شود.                                                |
| `/resources/` و ۱۳۱ مدخل داده        | Library                            | `/resources/` به‌عنوان index                                 | منبع جدید باید هم فایل و هم مدخل داده داشته باشد؛ ابزار این دو diff را با هم نشان می‌دهد.          |
| `/blog/` و ۸ پست                     | News / Blog                        | `/blog/` و permalink هر پست                                  | با `_news` یکی نشود؛ پست، محتوای بلند است.                                                         |
| `/news/` و ۳ خبر                     | News / announcements               | `/news/`                                                     | صفحه در navigation اصلی نیست؛ تصمیم نمایش آن با مالک است.                                          |
| `_pages/dropdown.md`                 | Navigation utility                 | بدون URL مستقل                                               | Publication، Projects و Blog را دوباره در منو فهرست می‌کند؛ حذف یا نگهداری نیازمند تأیید مالک است. |
| `/404.html`                          | System                             | `/404.html`                                                  | redirect یا reclassification لازم نیست.                                                            |

## موارد نیازمند تصمیم مالک

1. `cv` و `presentations` هر دو `nav_order: 5` دارند. ترتیب نهایی منو باید صریح انتخاب شود.
2. صفحهٔ dropdown سه پیوندی را که در منوی اصلی هم هستند تکرار می‌کند. حذف آن یک تغییر navigation است و در این مرحله انجام نشد.
3. دو جفت عنوان تکراری پیدا شد، اما hash و محتوا یکسان نیستند؛ بنابراین حذف یا redirect خودکار امن نیست:
   - «رفتار منابع ولتاژ در حالت موازی»: `teaching-circuiteffort-paralellvoltagesource.md` و `teaching-circuiteffort-realparalellvoltagesource.md`
   - «چگونه پروژه درسی خود را در زمانی کوتاه آماده کنیم»: `teaching-dataengcourse-numpy-subsection.md` و `teaching-toolkit-howconsproject.md`
4. افزودن کارت یک فرد به `/people/`، افزودن رکورد به آرشیو پایان‌نامه و تغییر navigation ساختاری‌اند. ابزار برای این مسیرها هشدار می‌دهد و آن تغییرها را خودکار انجام نمی‌دهد.

## رفتار ایمن ابزار بر اساس این معماری

- کاربر یکی از routeهای موجود در `tools/site_manager/content_routes.yml` را انتخاب می‌کند؛ route ناشناخته رد می‌شود.
- پست‌ها و پروژه‌ها به collection واقعی خود می‌روند. منابع آموزشی، ارائه و کتابخانه زیر `_pages/resources/` ذخیره می‌شوند.
- برای هر منبع جدید، مدخل متناظر `_data/legacy_resources.yml` در همان Preview نشان داده می‌شود تا صفحه orphan نباشد.
- مقاله فقط به `_bibliography/papers.bib` اضافه می‌شود و تعارض کلید، DOI و عنوان/سال پیش از نوشتن متوقف می‌شود.
- permalink موجود در ویرایش عادی تغییر نمی‌کند. هیچ تغییر ساختاری در `_config.yml`، theme، collection یا navigation انجام نمی‌شود.

پس از تأیید مالک می‌توان یک کار جداگانه برای مرتب‌سازی navigation، تعیین تکلیف چهار منبع هم‌عنوان و تصمیم دربارهٔ News/Dropdown تعریف کرد. این MVP عمداً آن تصمیم‌ها را اعمال نمی‌کند.
