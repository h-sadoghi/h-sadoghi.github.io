---
layout: legacy_page
title: fast_rag_ui
permalink: /resources/teaching-patterneffort-fast-rag-ui/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/patterneffort/fast_rag_ui/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

# fast rag ui

**نویسنده**: محمد صالح علی اکبری

<img loading="lazy" alt="fast_rag_ui — illustration 1" src="https://quera.org/media/CACHE/images/public/avatars/8e111895562e470888dde40a0018e0eb/f93253aa8612f91a5a7b7f9d25cfabd4.jpg" />

<a href="https://github.com/mohammadsaleh40" target = "_blank">
Course illustration

Course illustration
</a>

دانشجوی مقطع کارشناسی ارشد

دانشکده: مرکز آموزش الکترونیکی

رشته: مهندسی کامپیوتر گرایش هوش مصنوعی و رباتیک

<iframe src="https://www.aparat.com/video/video/embed/videohash/jjn0ibz/vt/frame"

        allowFullScreen="true"


        width="1024" height="576"


        style="max-width: 100%; border: none;">

</iframe>

## فلسفه ایجاد fast_rag_ui

انتقال اطلاعات و دانش به مناطق کم برخوردار معمولا منافع مادی آنچنانی ندارند. پروژه‌هایی مثل <a href="https://wiki.iiab.io/go/Main_Page" target = "_blank">اینترنت در یک جعبه (Internet-in-a-Box (IIAB) )</a>یکی از راهکارهایی هست که معمولا مطرح می‌شود. این برای شرایطی است که هیچ اینترنتی در آن محیط نباشد. اما فرض کنید اینترنت وجود دارد ولی با سرعتی به شدت کم. برای این شرایط چه راهکاری دارید؟ اگر یک دانش‌آموز علاقه مند به یادگیری می‌خواست از سیستم RAG شما برای یادگیری خودش کمک بگیره ولی سرعت اینترنتی در حد 10KB/s اگر داشت چطور می‌خواد از دانشی که شما جمع آوری کردین استفاده کنه؟

### هدف کلی این پروژه

سیستم‌های RAG مختلف با امکانات مختلفی ساخته می‌شود ولی همه آن‌ها برای رسیدن به استفاده عمومی نیازمند یک ui با قابلیت تعریف حساب کاربری برای افراد مختلف و ذخیره تاریخچه گفت‌وگو برای کاربران است. در این پروژه هدف این است که یک ui ساده برای کاربری مبتدی طراحی شود که کاربری خیلی درگیر انتخاب گزینه‌های مختلف نشه و در پشت این ui ساده یا به صورت هوشمند یا به صورت شخصی سازی شده توسط ادمین این سیستم RAG تعاملات مناسبی با کاربر انجام بده. به عنوان مثال اگر نیاز به سرچ است خود سیستم تشخیص بده که برای پاسخ دادن به اون سؤال باید در اینترنت سرچ کنه.

## معماری کلی ui

در این پروژه برای مدیریت درخواست‌های بین کاربر و سرور از faast api کمک گرفته شده. قسمت front end با jinja2 مدیریت می‌شه. برای ذخیره اطلاعات کاربران و گفت و گوهاشون از دیتابیس mysql روی همان سروری که پروژه در حال اجرا هست استفاده می‌شه. برای ارتباط برقرار کردن با ارائه دهنده‌های api مدل‌های زبانی از کتابخانه LangChain کمک گرفتیم.

## شروع آماده‌سازی و نصب نرم‌افزارها روی سرور

در این مرحله سرور لینوکسی خود را برای اجرای سیستم RAG آماده می‌کنیم. لطفاً دستورات را به ترتیب و با دقت وارد کنید.

### ۱. به‌روزرسانی سرور

ابتدا لیست نرم‌افزارهای سرور را به‌روز می‌کنیم تا مطمئن شویم آخرین نسخه‌ها را دریافت می‌کنیم:

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. نصب دیتابیس (MySQL)

سیستم برای ذخیره اطلاعات چت‌ها به دیتابیس نیاز دارد. دستور زیر MySQL را نصب می‌کند:

```
sudo apt install -y mysql-server mysql-client

```

پس از نصب، وارد محیط MySQL می‌شویم:

```bash
sudo mysql
```

حالا باید دیتابیس و کاربر مخصوص برنامه را بسازیم. دستورات زیر را خط‌به‌خط در محیط MySQL کپی و اجرا کنید:

> **توجه:** در خط سوم، به جای `'salam'` یک رمز عبور قوی انتخاب کنید و آن را جایی یادداشت کنید.

```sql
CREATE DATABASE rag_chat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'rag_user'@'localhost' IDENTIFIED BY 'salam';

GRANT ALL PRIVILEGES ON rag_chat_db.* TO 'rag_user'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

با دستور `EXIT` از محیط MySQL خارج می‌شوید.

### ۳. دریافت کدهای پروژه

ابتدا مطمئن می‌شویم که `git` نصب است و سپس کدهای پروژه را دانلود می‌کنیم:

```bash
sudo apt install -y git
git clone https://github.com/mohammadsaleh40/fast_rag_ui.git
cd fast_rag_ui
```

### ۴. تنظیمات محیطی (فایل .env)

برنامه برای اجرا به تنظیماتی مثل کلیدهای API و رمز دیتابیس نیاز دارد. این اطلاعات را در فایلی به نام `.env` ذخیره می‌کنیم.

دستور زیر فایل را می‌سازد و باز می‌کند:

```bash
nano .env
```

محتویاتی که باید در فایل '.env' قرار داد به شرح زیر است. ابتدا API keyهایی که از google studio دریافت کردید را قرار می‌دهید. سپس اطلاعات مربوط به دیتا بیس و مدلی که معمولا قرار هست استفاده بشه. اگر هنگام تعریف کاربر دیتابیس رمزی غیر از 'salam' مشعص کردید در اینجا نیز آن را تعویض کنید.

```
GOOGLE_API_KEY_1=YOUR_GOOGLE_API_KEY
GOOGLE_API_KEY_2=YOUR_GOOGLE_API_KEY
GOOGLE_API_KEY_3=YOUR_GOOGLE_API_KEY
GOOGLE_API_KEY_4=YOUR_GOOGLE_API_KEY
GOOGLE_API_KEY_5=YOUR_GOOGLE_API_KEY

# تنظیمات دیگر
DB_HOST=localhost
DB_USER=rag_user
DB_PASSWORD=salam
DB_NAME=rag_chat_db
MODEL_NAME=gemma-3-27b-it
HOST=0.0.0.0
PORT=8083
DEBUG=True
```

> **راهنمای ذخیره در Nano:**
>
> 1. کلیدهای `Ctrl + O` را بزنید و سپس `Enter` را فشار دهید (برای ذخیره).
> 2. کلیدهای `Ctrl + X` را بزنید (برای خروج).

### ۵. نصب پیش‌نیازهای پایتون

برای اجرای کدهای پایتونی، ابزارهای لازم را نصب کرده و یک محیط مجازی می‌سازیم تا تداخلی با سایر برنامه‌های سرور نداشته باشد:

```bash
sudo apt install -y python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
```

> بعد از دستور آخر، باید عبارت `(venv)` را در ابتدای خط ترمینال خود ببینید.

حالا `pip` را آپدیت و کتابخانه‌های پروژه را نصب می‌کنیم:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### ۶. ساخت جداول دیتابیس

کدهای پروژه جداول مورد نیاز را داخل دیتابیسی که قبلاً ساختیم ایجاد می‌کنند:

```bash
python3 database_setup.py
```

### ۷. اجرای برنامه

برنامه را با دستور زیر اجرا می‌کنیم. این دستور پورت 8083 را برای دسترسی باز می‌کند:

```bash
uvicorn main:app --host 0.0.0.0 --port 8083
```

> **نکته:** تا زمانی که این پنجره ترمینال باز است، برنامه در حال اجراست. اگر ترمینال را ببندید، برنامه متوقف می‌شود.

### ۸. باز کردن پورت در فایروال (مهم)

اگر از فایروال اوبونتو (UFW) استفاده می‌کنید، باید پورت 8083 را باز کنید تا بتوانید از طریق مرورگر به سرور وصل شوید:

```bash
sudo ufw allow 8083
```

_(اگر از پنل‌های ابری مثل AWS یا DigitalOcean استفاده می‌کنید، باید پورت 8083 را در تنظیمات Security Group آن‌ها نیز باز کنید.)_

### ۹. ساخت اولین کاربر

بعد از شروع برنامه چون کاربری فعال نکردیم نمی‌توانیم وارد محیط chat بشیم. برای این کار باید کاربر در سیستم ثبت‌نام کنیم. با دستورات زیر در ترمینال خود سرور یا دستگاه شخصی خودمون می‌تونیم کاربر تعریف کنیم. به پارامترهای مثال زیر دقت کنید. ما ip سرور username، email, password و «نام و نام خانوادگی» کاربر را در این دستور تعریف می‌کنیم. pasword و username مهم هستند چون برای ورود به این اطلاعات نیاز داریم. فعلا امکان استفاده از گزینه فراموشی رمز عبور یا حذف کاربر را هنوز تعریف نکردیم.

```
curl -X POST http://<IP سرور مثل 12.34.56.78>:8083/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"soltan","email":"masood@example.com","password":"mas789123","full_name":"ali"}'
```

برای اینکه برنامه شما پس از ریستارت شدن سرور به صورت خودکار اجرا شود و اگر به هر دلیلی متوقف شد، دوباره راه‌اندازی شود، باید آن را به عنوان یک **سرویس سیستمی (Systemd Service)** تعریف کنید.

این بخش را می‌توانید به انتهای فایل آموزش قبلی اضافه کنید.

---

## تنظیم اجرای خودکار سرویس (Systemd)

تا اینجا برنامه را به صورت دستی اجرا کردیم. اگر سرور ریستارت شود یا ترمینال بسته شود، برنامه متوقف می‌شود. برای حل این مشکل، برنامه را به عنوان یک سرویس دائمی ثبت می‌کنیم.

### ۱. توقف اجرای دستی برنامه

اگر هنوز دستور `uvicorn` از مرحله قبل در حال اجرا است، باید آن را متوقف کنید تا پورت 8083 آزاد شود.
در ترمینالی که برنامه در آن اجرا می‌شود، کلیدهای `Ctrl + C` را بزنید.

### ۲. پیدا کردن مسیرهای دقیق

برای تعریف سرویس، نیاز به مسیر دقیق پوشه پروژه و مسیر پایتون داخل محیط مجازی داریم. دستورات زیر را وارد کنید و خروجی آن‌ها را جایی یادداشت کنید:

```bash
# نمایش مسیر کامل پوشه فعلی
pwd

# نمایش مسیر فایل اجرایی uvicorn در محیط مجازی
which uvicorn
```

_مثال:_ خروجی دستور اول ممکن است `/home/ubuntu/fast_rag_ui` و خروجی دستور دوم `/home/ubuntu/fast_rag_ui/venv/bin/uvicorn` باشد.

### ۳. ساخت فایل سرویس

با دستور زیر یک فایل تنظیمات برای سرویس می‌سازیم:

```bash
sudo nano /etc/systemd/system/fast-rag.service
```

محتویات زیر را داخل فایل کپی کنید. **توجه:** در خطوطی که مشخص شده، باید مسیرهایی که در مرحله قبل یادداشت کردید را جایگزین کنید.

```ini
[Unit]
Description=Fast RAG UI Service
After=network.target

[Service]
# نام کاربری سرور خود را به جای ubuntu بنویسید (دستور whoami نام کاربری را نشان می‌دهد)
User=ubuntu
Group=ubuntu

# مسیر پوشه پروژه (خروجی دستور pwd)
WorkingDirectory=/home/ubuntu/fast_rag_ui

# مسیر فایل اجرایی uvicorn داخل محیط مجازی (خروجی دستور which uvicorn)
ExecStart=/home/ubuntu/fast_rag_ui/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8083

# تنظیمات restart خودکار
Restart=always
RestartSec=5

# متغیرهای محیطی (اختیاری - اگر کد شما فایل .env را خودکار لود نمی‌کند)
# Environment="PATH=/home/ubuntu/fast_rag_ui/venv/bin"

[Install]
WantedBy=multi-user.target
```

> **راهنمای ذخیره در Nano:**
>
> 1. کلیدهای `Ctrl + O` را بزنید و سپس `Enter` را فشار دهید.
> 2. کلیدهای `Ctrl + X` را بزنید.

### ۴. فعال‌سازی و اجرای سرویس

حالا به سیستم اطلاع می‌دهیم که فایل سرویس جدید را بخواند و آن را فعال کنیم:

```bash
# بارگذاری مجدد تنظیمات سیستم
sudo systemctl daemon-reload

# فعال‌سازی سرویس برای اجرای خودکار هنگام روشن شدن سرور
sudo systemctl enable fast-rag

# اجرای سرویس
sudo systemctl start fast-rag
```

### ۵. بررسی وضعیت سرویس

برای اطمینان از اینکه سرویس بدون خطا اجرا شده است، دستور زیر را بزنید:

```bash
sudo systemctl status fast-rag
```

اگر همه چیز درست باشد، باید عبارت `Active: active (running)` را با رنگ سبز ببینید.

### ۶. مشاهده لاگ‌های برنامه

برای دیدن خروجی‌های برنامه (مثلاً خطاهای احتمالی یا لاگ‌های اتصال) از دستور زیر استفاده کنید:

```bash
# مشاهده لاگ‌ها به صورت زنده
sudo journalctl -u fast-rag -f
```

برای خروج از حالت زنده، کلیدهای `Ctrl + C` را بزنید.

### ۷. مدیریت سرویس در آینده

برای کنترل سرویس می‌توانید از دستورات زیر استفاده کنید:

```bash
# توقف سرویس
sudo systemctl stop fast-rag

# راه‌اندازی مجدد سرویس (مثلاً بعد از آپدیت کدها)
sudo systemctl restart fast-rag

# غیرفعال کردن اجرای خودکار هنگام روشن شدن سرور
sudo systemctl disable fast-rag
```

### نکته مهم درباره آپدیت کردن برنامه

اگر بعداً کدهای پروژه را از گیت‌هاب آپدیت کردید (`git pull`)، حتماً باید سرویس را ریستارت کنید تا تغییرات اعمال شود:

```bash
sudo systemctl restart fast-rag
```

{% endraw %}
