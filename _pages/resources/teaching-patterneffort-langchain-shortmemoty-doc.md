---
layout: legacy_page
title: مستندات ماژول حافظه کوتاه‌مدت LangChain
permalink: /resources/teaching-patterneffort-langchain-shortmemoty-doc/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/patterneffort/LangChain_ShortMemoty_Doc/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

# مستندات ماژول حافظه کوتاه‌مدت LangChain

**نویسنده** :‌ عرفان امام وردی

## فهرست مطالب

<!-- prettier-ignore -->
* TOC
{:toc}

## معرفی

این پروژه یک ماژول **حافظه کوتاه‌مدت** برای استفاده در اپلیکیشن‌های LangChain فراهم می‌کند. حافظه کوتاه‌مدت برای نگهداری موقت تاریخچه مکالمه در طول یک session استفاده می‌شود و به چت‌بات یا عامل هوشمند اجازه می‌دهد به گفتگوهای قبلی دسترسی داشته باشد.

**کاربردهای اصلی:**

- چت‌بات‌هایی که تاریخچه مکالمه را به خاطر می‌سپارند
- عامل‌هایی که از تعاملات قبلی یاد می‌گیرند
- اپلیکیشن‌هایی که به آگاهی از زمینه (context) نیاز دارند

---

## ساختار پروژه

```
LangChain-Short-Memory/
├── config.py                 # تنظیمات (API Key، مدل، پارامترهای حافظه)
├── requirements.txt         # وابستگی‌های پایتون
├── setup.py                 # نصب پکیج
├── src/
│   └── memory/
│       ├── __init__.py      # صادرات کلاس‌های حافظه
│       ├── memory_overview.py   # نمای کلی حافظه و کلاس پایه
│       ├── short_term_memory.py # پیاده‌سازی حافظه‌های کوتاه‌مدت
│       └── pattern_recognition_memory.py # حافظه KNN و K-Means (شناسایی الگو)
├── examples/
│   ├── quick_start.py       # مثال سریع با حافظه Buffer (فارسی)
│   ├── short_term_memory_example.py  # مثال‌های Buffer، Window، Summary
│   └── pattern_recognition_memory_example.py # مثال حافظهٔ شباهت و خوشه‌بندی
├── unit_test/               # تست‌های واحد
│   ├── test_short_term_memory.py
│   └── test_pattern_recognition_memory.py
├── memory_comparison/       # مقایسهٔ خروجی سه نوع حافظه با یک دیتای mock
│   ├── run_memory_comparison.py
│   └── MEMORY_COMPARISON_RESULTS.txt   # خروجی ذخیره‌شده (بعد از اجرای اسکریپت)
└── DOCUMENTATION_FA.md      # مستندات کامل (فارسی، RTL)
```

---

## نصب و راه‌اندازی

### پیش‌نیازها

- پایتون ۳.۸ یا بالاتر
- کلید API شرکت OpenAI (برای استفاده از مدل و مثال‌های واقعی)

### مراحل نصب

۱. **کلون یا ورود به پوشه پروژه:**

```bash
cd LangChain-Short-Memory
```

۲. **ایجاد محیط مجازی (پیشنهادی):**

```bash
python -m venv venv
# ویندوز:
venv\Scripts\activate
# لینوکس/مک:
source venv/bin/activate
```

۳. **نصب وابستگی‌ها:**

```bash
pip install -r requirements.txt
```

یا نصب به صورت پکیج (برای import از `src`):

```bash
pip install -e .
```

۴. **تنظیم API Key:**

- در ریشه پروژه فایل `.env` بسازید.
- خط زیر را اضافه کنید (با کلید واقعی خودتان):

```
OPENAI_API_KEY=sk-...
```

یا در ویندوز به‌صورت موقت در PowerShell:

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

---

## توضیح کد

### ۱. ماژول `memory_overview.py`

- **`MemoryOverview`:** کلاسی که انواع حافظه را معرفی می‌کند و توضیح مفهومی می‌دهد.

  - `get_memory_types()`: لیست انواع حافظه (مثلاً short_term با چهار نوع).
  - `explain_memory()`: متن توضیحی درباره حافظه در LangChain و کاربردها.

- **`BaseMemoryManager`:** کلاس انتزاعی (ABC) برای ساخت مدیر حافظه سفارشی.
  - متدهای اجباری: `save_context`، `load_memory_variables`، `clear`.

### ۲. ماژول `short_term_memory.py`

کلاس اصلی: **`ShortTermMemoryManager`** (همه متدها `@staticmethod`).

| متد                                                            | خروجی                             | کاربرد                                                                    |
| -------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------- |
| `create_buffer_memory(...)`                                    | `ConversationBufferMemory`        | ذخیره **همه** پیام‌های مکالمه                                             |
| `create_window_memory(k=5, ...)`                               | `ConversationBufferWindowMemory`  | ذخیره فقط **آخرین k** پیام                                                |
| `create_summary_memory(llm, ...)`                              | `ConversationSummaryMemory`       | ذخیره **خلاصه** مکالمه (با LLM)                                           |
| `create_summary_buffer_memory(llm, max_token_limit=2000, ...)` | `ConversationSummaryBufferMemory` | ترکیب بافر + خلاصه؛ بعد از رسیدن به حد توکن، پیام‌های قدیمی خلاصه می‌شوند |

**پارامترهای مشترک (در همه):**

- `return_messages`: اگر `True` باشد، آبجکت پیام برمی‌گردد؛ وگرنه رشته.
- `memory_key`: کلید ذخیره حافظه در زنجیره (پیش‌فرض: `"history"`).

کد LangChain مربوط به هر نوع حافظه از `langchain.memory` import شده و فقط با پارامترهای مناسب ساخته و برگردانده می‌شود.

### ۳. فایل `config.py`

- بارگذاری `.env` با `load_dotenv()`.
- کلاس **`Config`:**
  - `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_TEMPERATURE`
  - `DEFAULT_MEMORY_KEY`, `DEFAULT_WINDOW_SIZE`, `DEFAULT_MAX_TOKEN_LIMIT`
- `Config.validate()`: بررسی وجود `OPENAI_API_KEY`.
- `Config.get_llm_config()`: دیکشنری تنظیمات مدل برای استفاده در LLM.

### ۴. مثال‌ها

- **`quick_start.py`:**  
  ایجاد حافظه Buffer و نمایش آن. **بدون API Key:** فقط حافظه با چند تبادل شبیه‌سازی‌شده پر و محتوای آن نمایش داده می‌شود. **با API Key:** اتصال به `ConversationChain` و مکالمه واقعی با مدل.

- **`short_term_memory_example.py`:**  
  **بدون API Key:** تابع `example_without_api_key()` اجرا می‌شود (نمایش save/load حافظه). با API Key می‌توان یکی از مثال‌های Buffer، Window یا Summary را uncomment کرد.

- **`pattern_recognition_memory_example.py`:**  
  مثال حافظهٔ مبتنی بر شباهت (KNN)، خوشه‌بندی (K-Means) و حافظهٔ پنجره‌ای (آخرین K). با یا بدون API Key قابل اجرا است (بدون Key فقط بخش ذخیره/بارگذاری و خروجی حافظه نشان داده می‌شود).

---

## انواع حافظه

| نوع                  | کلاس                              | ویژگی                                                              |
| -------------------- | --------------------------------- | ------------------------------------------------------------------ |
| **Buffer**           | `ConversationBufferMemory`        | همه پیام‌ها؛ ساده؛ با مکالمه طولانی حجیم می‌شود.                   |
| **Window**           | `ConversationBufferWindowMemory`  | فقط آخرین k پیام؛ کنترل حجم؛ ممکن است زمینه قدیمی از دست برود.     |
| **Summary**          | `ConversationSummaryMemory`       | فقط خلاصه مکالمه؛ مناسب مکالمات بلند؛ نیاز به LLM برای خلاصه‌سازی. |
| **Summary + Buffer** | `ConversationSummaryBufferMemory` | تا حد توکن مشخص بافر؛ بعد خلاصه؛ تعادل بین زمینه و حجم.            |

### خلاصهٔ نحوهٔ کار SummaryMemory

در **ConversationSummaryMemory** خلاصه‌سازی با **مدل زبانی (LLM)** انجام می‌شود: هر بار که تاریخچه به‌روز می‌شود، در صورت نیاز متن مکالمه (یا بخش جدید آن) به LLM داده می‌شود و از آن **یک خلاصهٔ متنی** درخواست می‌شود؛ این خلاصه ذخیره می‌شود و به‌جای کل تاریخچه به پرامپت مدل داده می‌شود تا هم حجم کم شود هم زمینهٔ کلی حفظ شود.

---

## حافظه‌های مبتنی بر شناسایی آماری الگو

برای ارتباط پروژه با درس **شناسایی آماری الگو**، دو نوع حافظهٔ اضافی در ماژول `pattern_recognition_memory` پیاده‌سازی شده‌اند (وابستگی: **scikit-learn**):

| نوع                           | کلاس                    |                                          |
| ----------------------------- | ----------------------- | ---------------------------------------- |
| **حافظهٔ مبتنی بر شباهت**     | `SimilarityBasedMemory` | KNN، شباهت کسینوسی، استخراج ویژگی TF-IDF |
| **حافظهٔ مبتنی بر خوشه‌بندی** | `ClusteringBasedMemory` | K-Means، مرکز خوشه، فاصله تا centroid    |
| **حافظهٔ معمولی (پنجره)**     | `WindowBasedMemory`     | —؛ فقط آخرین K تبادل                     |

- **SimilarityBasedMemory:** به‌جای «آخرین k پیام»، **k تبادلِ مرتبط‌ترین** با ورودی فعلی (با شباهت کسینوسی در فضای TF-IDF) برمی‌گرداند.
- **ClusteringBasedMemory:** تبادل‌ها با K-Means خوشه‌بندی می‌شوند؛ فقط تبادل‌های **خوشهٔ نزدیک** به سؤال فعلی به عنوان تاریخچه بارگذاری می‌شوند.
- **WindowBasedMemory:** حافظهٔ معمولی؛ همیشه **آخرین K تبادل** را برمی‌گرداند (بدون sklearn).

استفاده (یکی از سه حالت):

```python
from src.memory import PatternRecognitionMemoryManager
memory = PatternRecognitionMemoryManager.create_similarity_memory(k=5)
# یا: PatternRecognitionMemoryManager.create_clustering_memory(n_clusters=3)
# یا: PatternRecognitionMemoryManager.create_window_memory(k=5)
```

### نحوهٔ محاسبهٔ بردار از روی پیام و محاسبهٔ فاصله (KNN و Clustering)

هر دو حافظهٔ **شباهت (KNN)** و **خوشه‌بندی (K-Means)** از یک روش مشترک برای تبدیل متن به بردار استفاده می‌کنند؛ بعد در مرحلهٔ بازیابی، معیار فاصله/شباهت متفاوت است.

#### ۱. پیش‌پردازش متن

قبل از استخراج ویژگی، متن نرمال می‌شود:

- حذف فاصله‌های اضافه و trim کردن ابتدا و انتها (`re.sub(r"\s+", " ", text.strip())`).
- محدود کردن طول به حداکثر ۲۰۰۰ کاراکتر تا بردارها خیلی پراکنده نشوند.

> ```python
> def _normalize_text(text: str) -> str:
>     if not text or not isinstance(text, str):
>         return ""
>     text = re.sub(r"\s+", " ", text.strip())
>     return text[:2000]  # محدودیت طول
> ```

#### ۲. استخراج بردار (فضای ویژگی TF-IDF)

- **نمای هر تبادل:** برای هر تبادل ذخیره‌شده، یک متن ترکیبی ساخته می‌شود: «پیام کاربر + پاسخ دستیار» (با فاصله)، سپس همان نرمال‌سازی اعمال می‌شود.
- **ساخت فضای واژگانی:** با **TfidfVectorizer** (کتابخانه scikit-learn):
  - **max_features=500:** حداکثر ۵۰۰ عبارت با بیشترین فراوانی در کلاس‌بندی می‌مانند (بعد بردارها در فضای ۵۰۰ بعدی هستند).
  - **stop_words="english":** کلمات ایست انگلیسی حذف می‌شوند (برای متن فارسی می‌توان در توسعهٔ بعدی لیست ایست واژهٔ فارسی گذاشت).
  - **ngram_range=(1, 2):** هم تک‌کلمه (unigram) و هم دوکلمهٔ پشت‌سرهم (bigram) به عنوان ویژگی استفاده می‌شوند.
- **محاسبهٔ وزن TF-IDF:** برای هر سند (هر تبادل) وزن هر عبارت = (فراوانی در آن سند) × (معکوس فراوانی در کل اسناد). خروجی یک بردار تنک (sparse) برای هر تبادل است.
- **بردار پیام فعلی کاربر:** وقتی کاربر پیام جدید می‌فرستد، همان **vectorizer** (که قبلاً روی همهٔ تبادل‌های ذخیره‌شده fit شده) با **transform** روی متن پیام فعلی اعمال می‌شود تا بردار پیام در **همان فضای ۵۰۰ بعدی** به دست آید. یعنی پیام کاربر و هر تبادل قبلی در یک فضای مشترک هستند و قابل مقایسه‌اند.

> ```python
> # متن هر تبادل = human + ai (نرمال‌شده)
> texts = [_normalize_text(f"{item['human']} {item['ai']}") for item in self.buffer]
> self._vectorizer = TfidfVectorizer(max_features=500, stop_words="english", ngram_range=(1, 2))
> self._vectors = self._vectorizer.fit_transform(texts)
> # بردار پیام فعلی کاربر:
> q = self._vectorizer.transform([current])
> ```

خلاصه: **هر پیام یا تبادل = یک بردار در فضای TF-IDF با ۵۰۰ بعد (و n-gramهای ۱ و ۲).**

#### ۳. KNN (حافظهٔ مبتنی بر شباهت)

- **ورودی:** بردار پیام فعلی `q` (از مرحلهٔ بالا) و ماتریس بردارهای همهٔ تبادل‌های قبلی `_vectors`.
- **معیار شباهت:** **شباهت کسینوسی** (cosine similarity) بین `q` و هر بردار تبادل:
  - **فرمول:** `sim(q, v) = (q · v) / (‖q‖ × ‖v‖)`  
    یعنی حاصل‌ضرب داخلی دو بردار تقسیم بر حاصل‌ضرب نرم آن‌ها. مقدار بین ۱ (هم‌جهت) و ۰ (عمود).
- **محاسبه در کد:** `cosine_similarity(q, self._vectors).ravel()` یک آرایه به طول تعداد تبادل‌ها برمی‌گرداند؛ هر درایه شباهت آن تبادل به پیام فعلی است.
- **انتخاب k نزدیک‌ترین:** با `np.argsort(sim)` اندیس‌ها بر اساس شباهت صعودی مرتب می‌شوند؛ **آخرین k اندیس** (بیشترین شباهت) انتخاب و به ترتیب نزولی شباهت برگردانده می‌شوند. این k تبادل به عنوان «تاریخچهٔ مرتبط» به مدل داده می‌شوند.

> ```python
> q = self._vectorizer.transform([current])
> sim = cosine_similarity(q, self._vectors).ravel()
> n = min(self.k, len(self.buffer))
> top_indices = np.argsort(sim)[-n:][::-1]
> # top_indices = اندیس k تبادل با بیشترین شباهت کسینوسی
> ```

یعنی در KNN از **شباهت کسینوسی** به‌عنوان معیار نزدیکی استفاده می‌شود، نه فاصلهٔ اقلیدسی.

#### ۴. Clustering (حافظهٔ مبتنی بر خوشه‌بندی K-Means)

- **آموزش:** روی بردارهای همهٔ تبادل‌های ذخیره‌شده (همان بردارهای TF-IDF) الگوریتم **K-Means** با `n_clusters` خوشه اجرا می‌شود. هر تبادل به یک خوشه نسبت داده می‌شود و مرکز (centroid) هر خوشه محاسبه می‌شود.
- **فاصله در K-Means:** داخل K-Means معمولاً **فاصلهٔ اقلیدسی** بین بردار هر نقطه و مرکز خوشه‌ها استفاده می‌شود. هر نقطه به خوشه‌ای که **مرکز آن نزدیک‌تر** است نسبت داده می‌شود.
- **ورودی جدید (پیام فعلی کاربر):** بردار `q` همان‌طور که بالا توضیح داده شد با همان `vectorizer` ساخته می‌شود.
- **انتساب به خوشه:** با `kmeans.predict(q)` نزدیک‌ترین مرکز خوشه به بردار `q` پیدا می‌شود و شمارهٔ آن خوشه (label) برمی‌گردد.
- **بازیابی:** همهٔ تبادل‌هایی که **label** آن‌ها برابر با این خوشه است به عنوان تاریخچه برگردانده می‌شوند. یعنی فقط تبادل‌های هم‌خوشه با پیام فعلی به مدل داده می‌شوند.

> ```python
> self._vectorizer = TfidfVectorizer(...)
> self._vectors = self._vectorizer.fit_transform(texts)
> self._kmeans = KMeans(n_clusters=..., random_state=42, n_init=10)
> self._kmeans.fit(self._vectors)
> # برای پیام فعلی:
> q = self._vectorizer.transform([current])
> label = self._kmeans.predict(q)[0]
> indices = [i for i in range(len(self.buffer)) if self._kmeans.labels_[i] == label]
> ```

خلاصه: **بردار = TF-IDF با ۵۰۰ ویژگی و n-gram (1,2)**؛ در **KNN** معیار نزدیکی = **شباهت کسینوسی** و انتخاب k بیشترین شباهت؛ در **Clustering** معیار = **فاصلهٔ اقلیدسی تا مرکز خوشه** و انتخاب خوشهٔ نزدیک‌ترین، سپس برگرداندن همهٔ اعضای آن خوشه.

---

## نحوه اجرا

### اجرای مثال سریع (فارسی)

از ریشه پروژه:

```bash
python examples/quick_start.py
```

خروجی شامل: ایجاد حافظه، ساخت زنجیره، چند تبادل کاربر/دستیار و در پایان محتوای `memory.buffer` است.

### اجرای مثال‌های حافظه (انگلیسی)

۱. فایل `examples/short_term_memory_example.py` را باز کنید.
۲. در انتهای فایل، یکی از خطوط زیر را از حالت comment خارج کنید:

```python
example_buffer_memory()
# example_window_memory()
# example_summary_memory()
```

۳. اجرا:

```bash
python examples/short_term_memory_example.py
```

### اجرای مثال حافظهٔ شناسایی الگو

```bash
python examples/pattern_recognition_memory_example.py
```

(بدون API Key فقط بخش ذخیره/بارگذاری و خروجی حافظه اجرا می‌شود.)

### اجرای تست‌های واحد

با **unittest** (از ریشه پروژه):

```bash
python -m pytest unit_test/ -v
```

یا مستقیم با ماژول تست:

```bash
python -m unittest unit_test.test_short_term_memory -v
python -m unittest unit_test.test_pattern_recognition_memory -v
```

یا اجرای مستقیم فایل تست:

```bash
python unit_test/test_short_term_memory.py
python unit_test/test_pattern_recognition_memory.py
```

**تست‌ها به API Key نیاز ندارند** (برای Summary از Mock استفاده شده؛ تست‌های pattern recognition اصلاً مدل صدا نمی‌زنند).

برای اجرای تست با گزارش پوشش (coverage):

```bash
pip install pytest-cov
pytest unit_test/ -v --cov=src.memory
```

نتایج مقایسهٔ حافظه‌ها با دیتای mock در **`memory_comparison/MEMORY_COMPARISON_RESULTS.txt`** ذخیره می‌شود (بعد از اجرای `python memory_comparison/run_memory_comparison.py`).

### مقایسهٔ خروجی سه نوع حافظه (دیتای mock یکسان)

اسکریپت **`memory_comparison/run_memory_comparison.py`** یک مکالمهٔ mock ثابت به هر سه حافظه (پنجره، KNN، خوشه‌بندی) می‌دهد و با یک سؤال از هر کدام تاریخچه را بارگذاری می‌کند؛ خروجی در **`memory_comparison/MEMORY_COMPARISON_RESULTS.txt`** ذخیره می‌شود.

```bash
python memory_comparison/run_memory_comparison.py
```

#### Mock اولیه (مکالمهٔ ورودی)

همان ۶ تبادلی که به هر سه حافظه داده می‌شود:

| #   | کاربر                        | دستیار                                               |
| --- | ---------------------------- | ---------------------------------------------------- |
| 1   | I love Python programming    | Python is great for beginners and experts.           |
| 2   | What about machine learning? | Python has excellent ML libraries like scikit-learn. |
| 3   | The weather is nice today    | Yes, a good day to go outside.                       |
| 4   | Will it rain tomorrow?       | The forecast says it might rain in the evening.      |
| 5   | I had pizza for lunch        | Pizza is always a good choice.                       |
| 6   | Do you like Python?          | Yes, Python is very popular for data science.        |

#### کوئری ورودی کاربر

سؤالی که برای بارگذاری حافظه از هر سه روش استفاده می‌شود:

```
"Tell me more about Python and programming."
```

#### نتایج مقایسه (خروجی هر روش)

**پارامترها:** `k=3` برای پنجره و KNN، `n_clusters=3` برای خوشه‌بندی.

- **حافظهٔ پنجره‌ای (Window)** — معیار: آخرین K تبادل (بدون توجه به سؤال)

```
Human: Will it rain tomorrow?
AI: The forecast says it might rain in the evening.
Human: I had pizza for lunch
AI: Pizza is always a good choice.
Human: Do you like Python?
AI: Yes, Python is very popular for data science.
```

- **حافظهٔ مبتنی بر شباهت (KNN)** — معیار: K تبادلِ مرتبط‌ترین با سؤال (شباهت کسینوسی)

```
Human: I love Python programming
AI: Python is great for beginners and experts.
Human: Do you like Python?
AI: Yes, Python is very popular for data science.
Human: What about machine learning?
AI: Python has excellent ML libraries like scikit-learn.
```

- **حافظهٔ مبتنی بر خوشه‌بندی (K-Means)** — معیار: تبادل‌های هم‌خوشه با سؤال

```
Human: I love Python programming
AI: Python is great for beginners and experts.
Human: What about machine learning?
AI: Python has excellent ML libraries like scikit-learn.
Human: Do you like Python?
AI: Yes, Python is very popular for data science.
```

مقایسهٔ بالا نشان می‌دهد: **Window** همیشه آخرین ۳ تبادل را برمی‌گرداند (آب‌وهوا، غذا، پایتون). **KNN** و **خوشه‌بندی** هر دو تبادل‌های مرتبط با برنامه‌نویسی و پایتون را ترجیح داده‌اند؛ ترتیب و تعداد تبادل‌ها بسته به معیار شباهت و خوشه متفاوت است.

---

## پیکربندی

- **متغیرهای محیطی (یا `.env`):**

  - `OPENAI_API_KEY`: برای **مکالمه واقعی با مدل** لازم است؛ اجرای مثال‌ها و **تست‌ها بدون آن** ممکن است (مثال‌ها در حالت بدون Key فقط بخش حافظه را نشان می‌دهند).
  - `OPENAI_MODEL`: مثلاً `gpt-3.5-turbo`.
  - `OPENAI_TEMPERATURE`: مثلاً `0.7`.

- **مقادیر پیش‌فرض در `config.py`:**
  - `DEFAULT_MEMORY_KEY = "history"`
  - `DEFAULT_WINDOW_SIZE = 5`
  - `DEFAULT_MAX_TOKEN_LIMIT = 2000`

استفاده در کد:

```python
from config import Config
Config.validate()
llm_config = Config.get_llm_config()
```

---

## گسترش و توسعه در آینده

|                          | ایدهٔ گسترش در پروژه                                                           |
| ------------------------ | ------------------------------------------------------------------------------ |
| **نظریهٔ تصمیم بیزی**    | قانون تصمیم برای «چه زمانی خلاصه کنیم» با دو کلاس و ویژگی‌هایی مثل تعداد توکن. |
| **کاهش ابعاد (PCA/LDA)** | کاهش بعد بردارهای تبادل با PCA و نگه‌داشتن مؤلفه‌های اصلی.                     |
| **مدل مخلوط گوسی (GMM)** | خوشه‌بندی نرم به‌جای K-Means سخت.                                              |
| **مارکوف پنهان (HMM)**   | مدل کردن دنبالهٔ نوع پیام و پیش‌بینی برای انتخاب بخش حافظه.                    |
| **SVM**                  | طبقه‌بندی موضوع هر تبادل و بازیابی فقط تبادل‌های هم‌موضوع.                     |

---

## جمع‌بندی

با این ماژول می‌توانید با فراخوانی **`ShortTermMemoryManager`** یا **`PatternRecognitionMemoryManager`** یکی از انواع حافظه (Buffer، Window، Summary، Summary+Buffer، یا KNN/خوشه‌بندی/پنجره) را انتخاب کنید، به `ConversationChain` وصل کنید و مکالمه دارای حافظه داشته باشید. همهٔ توضیحات، نحوهٔ اجرا، تست و ارتباط با درس شناسایی آماری الگو در این سند (DOCUMENTATION_FA.md) گردآوری شده است.
{% endraw %}
