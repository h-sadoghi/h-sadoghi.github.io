---
layout: legacy_page
title: "بررسی چارچوب LangChain: توسعه برنامه‌های مبتنی بر مدل‌های زبانی بزرگ"
permalink: /resources/teaching-patterneffort-exploring-the-langchain-framework/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/patterneffort/Exploring_the_LangChain_Framework/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

# LangChain

**عنوان پروژه:** بررسی چارچوب <span dir="ltr">LangChain</span>  
**نام دانشجو:** فرخنده خوشنود  
**مقطع:** دانشجوی مجازی هوش مصنوعی، دانشگاه فردوسی مشهد

---

## مقدمه

مدل‌های زبانی بزرگ (<span dir="ltr">LLMs</span>) مانند <span dir="ltr">GPT</span> امکان تولید متن، پاسخ به سوالات و حتی تولید کد را فراهم کرده‌اند.  
اما استفاده مستقیم از این مدل‌ها برای ساخت یک سیستم واقعی، چالش‌هایی مانند مدیریت حافظه، اتصال به ابزارها و طراحی جریان کاری دارد.

<span dir="ltr">LangChain</span> چارچوبی است که این فرایند را ساده می‌کند و امکان ساخت برنامه‌های مبتنی بر مدل‌های زبانی را فراهم می‌کند.

---

## چرا <span dir="ltr">LangChain</span>؟

- ساده‌سازی توسعه برنامه‌های مبتنی بر <span dir="ltr">LLM</span>
- امکان اتصال به ابزارها و دیتابیس‌ها
- پشتیبانی از مدل‌های مختلف (<span dir="ltr">OpenAI</span>، <span dir="ltr">DeepSeek</span>، <span dir="ltr">Anthropic</span> و ...)
- معماری ماژولار و قابل گسترش

---

## معماری کلی

LangChain از مؤلفه‌های مختلفی تشکیل شده است:

| مؤلفه                                | توضیح                   |
| ------------------------------------ | ----------------------- |
| <span dir="ltr">Chat Models</span>   | اجرای مدل‌های گفتگو     |
| <span dir="ltr">Tools</span>         | اجرای ابزارهای خارجی    |
| <span dir="ltr">Memory</span>        | حفظ تاریخچه مکالمه      |
| <span dir="ltr">Retrievers</span>    | بازیابی اطلاعات         |
| <span dir="ltr">Vector Stores</span> | ذخیره بردارهای امبدینگ  |
| <span dir="ltr">Embeddings</span>    | تبدیل متن به بردار عددی |

این معماری باعث می‌شود بتوان بخش‌های مختلف را به‌صورت ترکیبی استفاده کرد.

---

## مدل‌های گفتگو (<span dir="ltr">Chat Models</span>)

مدل‌های گفتگو به جای دریافت یک متن خام، لیستی از پیام‌ها را دریافت می‌کنند:

- <span dir="ltr">system</span> → تعیین رفتار مدل
- <span dir="ltr">human</span> → پیام کاربر
- <span dir="ltr">assistant</span> → پاسخ مدل

---

## مثال کد: اتصال به <span dir="ltr">OpenAI</span>

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o",
    api_key="YOUR_KEY"
)

messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Explain LangChain in two sentences")
]

response = model.invoke(messages)
print(response.content)
```

### توضیح بخش‌های کد

| بخش                                     | توضیح                 |
| --------------------------------------- | --------------------- |
| <span dir="ltr">ChatOpenAI</span>       | ساخت شیء مدل          |
| <span dir="ltr">messages</span>         | تعریف پیام‌های مکالمه |
| <span dir="ltr">invoke</span>           | ارسال درخواست         |
| <span dir="ltr">response.content</span> | دریافت خروجی مدل      |

---

## <picture><source type="image/webp" srcset="/assets/img/legacy/image1-e14b19e1e0-480.webp 480w, /assets/img/legacy/image1-e14b19e1e0-800.webp 800w, /assets/img/legacy/image1-e14b19e1e0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/image1-e14b19e1e0.jpg"  alt="author_attribution_problems"></picture>

## استفاده از <span dir="ltr">DeepSeek</span> در <span dir="ltr">LangChain</span>

### نصب کتابخانه

```bash
pip install -qU langchain-deepseek
```

### تنظیم <span dir="ltr">API Key</span>

```python
import getpass
import os

if not os.getenv("DEEPSEEK_API_KEY"):
    os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your API key: ")
```

### ساخت مدل

```python
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0
)
```

### فراخوانی مدل

```python
messages = [
    ("system", "Translate English to French"),
    ("human", "I love programming")
]

ai_msg = llm.invoke(messages)
print(ai_msg.content)
```

---

## کاربردها

| کاربرد            | توضیح                                            |
| ----------------- | ------------------------------------------------ |
| چت‌بات            | پاسخ‌گویی خودکار به کاربران                      |
| سیستم پرسش و پاسخ | استخراج پاسخ از داده‌ها                          |
| اتصال به دیتابیس  | ترکیب <span dir="ltr">AI</span> با اطلاعات واقعی |
| تولید محتوا       | نوشتن متن، مقاله و کد                            |
| دستیار هوشمند     | اجرای وظایف چندمرحله‌ای                          |

---

## نتیجه‌گیری

<span dir="ltr">LangChain</span> یکی از مهم‌ترین چارچوب‌ها برای توسعه سریع برنامه‌های مبتنی بر مدل‌های زبانی است.  
با استفاده از آن می‌توان مدل‌های مختلف را به‌راحتی ترکیب کرد، ابزارها را متصل نمود و سیستم‌های هوشمند واقعی ایجاد کرد.
{% endraw %}
