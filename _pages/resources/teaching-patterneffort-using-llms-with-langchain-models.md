---
layout: legacy_page
title: Using LLMs with LangChain models
permalink: /resources/teaching-patterneffort-using-llms-with-langchain-models/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/patterneffort/Using_LLMs_with_LangChain_Models/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

<div class="english-text" markdown="1">

<strong>
  UniForCE
</strong>

</div>

## نویسنده

<strong>مهدیه سادات قاسمی</strong>

## راه‌های ارتباطی

<p align="center">
  <a href="https://github.com/mahdiehgh79"  target="_blank">
    Course illustration
  </a>
</p>

<a href="https://www.um.ac.ir/" target="_blank">
<strong>دانشگاه فردوسی مشهد</strong>
</a>

# Using LLMs with LangChain (Models)

## مقدمه

LLMs (مدل‌های زبان بزرگ) — ابزارهای بسیار قدرتمندی هستند که می‌توانند مانند انسان متن تولید، ترجمه، خلاصه، پاسخ پرسش و … انجام دهند.  
در کنار تولید متن ساده، بسیاری از این مدل‌ها قابلیت‌های پیشرفته‌تر نیز دارند:

- **صدا زدن ابزارها (tool calling)** — مانند فراخوانی پایگاه داده، API یا عملکردهای خارجی و استفاده از نتایج در پاسخ مدل
- **خروجی ساختاریافته (structured output)** — قالب معین برای خروجی، مثلا JSON یا مدل‌های Pydantic
- **چندرسانه‌ای (multimodality)** — توانایی پردازش و بازگرداندن انواع داده فراتر از متن مثل تصویر، صدا، ویدیو و غیره
- **استدلال (reasoning)** — امکان استنتاج چند مرحله‌ای برای نتیجه‌گیری پیچیده‌تر

در چارچوب LangChain، مدل‌ها مغز تصمیم‌گیری عامل (agent) هستند. مدل انتخاب‌شده تأثیر مستقیم بر دقت، توانایی و رفتار کلی agent دارد.

LangChain رابط استانداردی برای مدل‌ها فراهم می‌کند که به شما اجازه می‌دهد بین ارائه‌دهندگان مختلف مدل (providers) جابه‌جا شوید بدون اینکه معماری برنامه‌تان را کامل بازنویسی کنید.

---

## راه‌اندازی اولیه (Basic usage)

مدل‌ها در LangChain دو حالت استفاده دارند:

1. **همراه با agent** — وقتی از agentها استفاده می‌کنید، مدل می‌تواند به‌صورت داینامیک انتخاب شود.
2. **به‌صورت مستقل (standalone)** — برای task هایی مثل تولید متن، طبقه‌بندی، استخراج اطلاعات و غیره بدون agent. رابط یکسان است؛ بنابراین می‌توانید ساده شروع کنید و بعد به agentها مقیاس بدهید.

### نمونه ساده‌ی راه‌اندازی مدل

```python
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-4.1")
response = model.invoke("Why do parrots talk?")
print(response)
```

> در این مثال، init_chat_model برای یکی از ارائه‌دهندگان مدل (مثلاً OpenAI) فراخوانی شده است.

---

## متدهای اصلی (Key methods)

پس از ایجاد مدل، سه روش اصلی برای فراخوانی آن وجود دارد:

| روش           | توضیح                                                                                   |
| ------------- | --------------------------------------------------------------------------------------- |
| `invoke(...)` | ارسال یک پیام یا لیستی از پیام‌ها و دریافت پاسخ کامل                                    |
| `stream(...)` | دریافت خروجی به‌صورت تدریجی در زمان تولید (real-time streaming) — مناسب پاسخ‌های طولانی |
| `batch(...)`  | ارسال چند درخواست هم‌زمان (batch) برای پردازش موازی و افزایش کارایی                     |

> همچنین با `batch_as_completed()` می‌توانید پاسخ‌ها را پس از تکمیل هر درخواست دریافت کنید (ترتیب ممکن است متفاوت باشد).

---

## پارامترهای مدل (Parameters)

پارامترهای استاندارد شامل موارد زیر هستند:

- `model`: نام یا شناسه مدل مشخص (مثلاً "gpt-4.1")
- `api_key`: کلید احراز هویت (برای provider هایی که نیاز به API key دارند)
- `temperature`: کنترل تصادفی بودن خروجی — مقدار بالاتر پاسخ خلاقانه‌تر، مقدار پایین‌تر پاسخ قطعی‌تر
- `max_tokens`: محدودیت تعداد توکن‌ها در خروجی
- `timeout`: حداکثر زمان (ثانیه) برای منتظر ماندن پاسخ مدل
- `max_retries`: تعداد تلاش برای درخواست مجدد در صورت خطا

> ارائه‌دهندگان مختلف ممکن است پارامترهای خاص خود را نیز داشته باشند، مانند `use_responses_api` در ChatOpenAI.

---

## فراخوانی مدل (Invocation)

### invoke()

ارسال یک پیام یا لیستی از پیام‌ها (مکالمه):

```python
from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("Translate: I love programming.")
]

response = model.invoke(conversation)
print(response)  # خروجی: ترجمه یا پاسخ مناسب
```

- در مدل‌های سنتی (non-chat LLM) خروجی به صورت رشته (string) است
- در chat-model های LangChain خروجی به‌صورت پیام (message object) باز می‌گردد

### stream()

برای دریافت پاسخ به‌صورت تدریجی در زمان تولید:

```python
for chunk in model.stream("Write a long story about AI"):
    print(chunk)
```

### batch()

زمانی که می‌خواهید چند درخواست جداگانه را به مدل بدهید:

```python
responses = model.batch([
    "Translate: I love AI",
    "Translate: Hello world"
])
```

> می‌توان با `max_concurrency` تعداد درخواست‌های هم‌زمان را محدود کرد.

---

## صدا زدن ابزارها (Tool calling)

مدل می‌تواند ابزارهایی که تعریف می‌کنید، فراخوانی کند. ابزارها می‌توانند توابع یا coroutine باشند که عملیات متفاوت انجام می‌دهند (مثلاً فراخوانی API، اجرای کد، پرس‌وجوی پایگاه داده).

### مراحل tool calling

1. **تعریف ابزار** با دکوراتور `@tool` یا به شکل مورد قبول LangChain
2. **Bind کردن ابزارها به مدل**:
   ```python
   model_with_tools = model.bind_tools([tool1, tool2])
   ```
3. **اجرای loop بین ابزار و مدل** تا رسیدن به پاسخ نهایی

> در agentها این چرخه به صورت خودکار انجام می‌شود، در حالت standalone باید خودتان مدیریت کنید.

مزایا:

- دسترسی مدل به داده واقعی
- انجام محاسبات و فراخوانی API
- کاهش hallucination

---

## خروجی ساختاریافته (Structured Output)

مثال با Pydantic:

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str = Field(..., description="Movie title")
    year: int = Field(..., description="Release year")
    director: str = Field(..., description="Director name")

model_with_structure = model.with_structured_output(Movie)
response = model_with_structure.invoke("Provide details about the movie Inception")
print(response)
```

مزایا:

- خروجی Typed و ساختاریافته
- راحت‌تر پارس و اعتبارسنجی می‌شود
- مناسب ذخیره در پایگاه داده یا تبدیل به JSON

> گزینه `include_raw=True` برای داشتن خروجی parsed و پیام خام مفید است.

---

## مدل‌های پشتیبانی‌شده (Supported Models)

- OpenAI
- Anthropic
- Google Gemini
- AWS Bedrock
- Mistral
- Cohere
- Local Models (بسته به پشتیبانی provider)

---

## مباحث پیشرفته (Advanced Topics)

- Model Profiles
- Multimodal Models
- Reasoning Models
- Local Models
- Prompt caching
- Server-side tool use, Rate limiting, Proxy, Token usage

---

## نکات مهم و توصیه‌ها

- تازه‌کارها: با invoke() و حالت standalone شروع کنید
- برای قابلیت‌های پیچیده: tool calling، structured output، batch
- انتخاب مدل مناسب برای کار خاص ضروری است
- طراحی اولیه باید امکان ارتقا به agent و toolها را داشته باشد

---

## جمع‌بندی

LangChain با رابط استاندارد خود امکان استفاده همزمان از قابلیت‌های مختلف LLMها مانند:

- Tool Calling
- Structured Output
- Streaming
- Batching

را فراهم می‌کند و برای پروژه‌های ساده تا Agentهای پیچیده و production-ready مناسب است.

---

## منابع

- [صفحه رسمی Models در مستندات LangChain](https://docs.langchain.com/docs/models)
- [GitHub LangChain](https://github.com/hwchase17/langchain)
  {% endraw %}
