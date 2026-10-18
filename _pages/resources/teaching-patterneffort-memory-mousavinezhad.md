---
layout: legacy_page
title: تاریخچه گفت و گو در LangChain
permalink: /resources/teaching-patterneffort-memory-mousavinezhad/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/patterneffort/Memory_Mousavinezhad/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

## {% raw %}

<p>

<p> نویسنده : عرفان موسوی نژاد</p>
</p>
<p>
دانشگاه فردوسی مشهد - دانشکده مهندسی - گروه هوش مصنوعی
</p>

### تاریخچه گفت و گو

ساده‌ترین راه نگهداری تاریخچه‌ی یک مکالمه این است که تمام پیام‌های ردوبدل‌شده بین کاربر و مدل را ذخیره کنیم و وقتی‌ که کاربر دستور جدیدی وارد می‌کند، پیام‌های پیشین را نیز همراه با آن به مدل ورودی دهیم تا مدل بتواند در راستای همان مکالمه‌ای که تاکنون داشته پاسخ خود را تولید کند. برای این کار کلاسی به‌نام `ChatMessageHistory` تعریف شده است که عملکرد بسیار ساده‌ای دارد. کافیست با استفاده از تابع `add_user_message()` پیام کاربر را به‌شکل یک `HumanMessage` تاریخچه/حافظه اضافه کنیم. پیام تولیدشده توسط مدل را نیز می‌توانیم با استفاده از تابع `add_ai_message()` به‌صورت یک `AIMessage` ذخیره کنیم. توجه داشته باشید که تمام پیام‌ها به‌صورت درون-حافظه‌ای (In-Memory) ذخیره می‌شوند یعنی اتفاقی که در پس‌زمینه در حال رخ دادن است شبیه به این است یک لیست پایتون وجود دارد و صرفاً در حال اضافه‌کردن پیام به آن لیست هستید.

```python
from langchain_community.chat_message_histories import ChatMessageHistory

history = ChatMessageHistory()
history.add_user_message("این جمله رو به فرانسوی ترجمه کن: من عاشق برنامه‌نویسی‌ام")
history.add_ai_message("J'adore la programmation.")
```

برای دسترسی به پیام‌های ذخیره‌شده می‌توانیم از خصوصیت `messages` این شیء استفاده کنیم.

```python
history.messages
```

حال بیایید یک مدل گفت‌وگوی ساده همراه با حافظه‌ای از جنس `ChatMessageHistory` را پیاده‌سازی کنیم. طبق معمول ابتدا کلید API خود را تنظیم می‌کنیم.

```python
import getpass
import os
os.environ["COHERE_API_KEY"] = getpass.getpass()
```

در ادامه به‌کمک `ChatCohere` یک مدل گفت‌وگو می‌سازیم. همچنین یک شیء از کلاس `ChatMessageHistory` ایجاد کرده و در متغیر `history` نگهداری می‌کنیم. از آن‌جا که قصد داریم برنامه‌ی ما به‌صورت مداوم اجرا شود و از کاربر ورودی بگیرد، در یک حلقه‌ی بی‌نهایت (تا زمانی‌که کاربر `0` وارد کند) از کاربر پیام وی را دریافت می‌کنیم، آن را به تاریخچه اضافه می‌کنیم، سپس خروجی مدل را تولید کرده و به‌صورت زنده به کاربر نمایش می‌دهیم (Stream) و در نهایت پیام خروجی مدل را نیز به تاریخچه اضافه می‌کنیم.

```python
from langchain_cohere import ChatCohere
from langchain_community.chat_message_histories import ChatMessageHistory

chat_model = ChatCohere(model='command-r-plus', temperature=0.2)
history = ChatMessageHistory()

while (True):

    # Get user message
    user_message = input('پیام خود را بنویسید ... (برای خروج 0 را بزنید)\n')

    # Exit the loop if the user enters '0'
    if (user_message == '0'):
        break
    else:
        print('User:',user_message, '\n')

        history.add_user_message(user_message)

        model_message = ''
        print('AI: ', end='')
        for chunk in chat_model.stream(history.messages):
            model_message =  model_message+ chunk.content
            print(chunk.content, end="", flush=True)
        print('\n')

        history.add_ai_message(model_message)
```

با اجرای کد بالا مشاهده می‌کنید که مدل به‌خوبی نام فرد و همچنین قانون بازی را به یاد دارد؛ زیرا در هر بار درخواست به مدل، تمام پیام‌های پیشین نیز در قالب دستور گنجانده شده است.

---

### مدیریت خودکار تاریخچه

دیدیم که چگونه می‌توان با استفاده از `ChatMessageHistory` پیام‌های پیشین کاربر و مدل را ذخیره کرده و در ادامه‌ی گفت‌وگو از آن‌ها استفاده کنیم. نکته‌ی قابل توجه درباره‌ی این کلاس این است که توسعه‌دهندگان باید به‌صورت دستی تاریخچه‌ی پیام‌های کاربر و مدل را مدیریت کرده و به این حافظه وارد کنند و درج خودکار در حافظه اتفاق نمی‌افتد. در فریم‌ورک `LangChain` یک ماژول (یا به‌بیان تخصصی‌تر یک Wrapper) با نام `RunnableWithMessageHistory` برای زنجیره‌های `LCEL` طراحی شده است که این فرآیند درج و خوانش از حافظه را به‌صورت خودکار مدیریت می‌کند.

<picture><source type="image/webp" srcset="/assets/img/legacy/runnablewithmessagehistory-583d6e7c4f-480.webp 480w, /assets/img/legacy/runnablewithmessagehistory-583d6e7c4f-800.webp 800w, /assets/img/legacy/runnablewithmessagehistory-583d6e7c4f-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" alt="تاریخچه گفت و گو در LangChain — illustration 1" src="/assets/img/legacy/runnablewithmessagehistory-583d6e7c4f.jpg"></picture>

به‌احتمال زیاد در کار با مدل‌های مختلفی نظیر Chat GPT مشاهده کرده‌اید که می‌توانید گفت‌وگوهای مختلفی را آغاز کرده و وقتی‌که وارد حساب خود می‌شوید لیستی از مکالمات قدیمی خود را مشاهده خواهید کرد که می‌توانید به آن‌ها ادامه دهید. در واقع به‌ازای هر گفت‌وگوی شما یک تاریخچه‌ی جدا در پایگاه‌داده ثبت شده که هنگام طرح یک پرسش جدید تمام پیام‌های مربوط به همان گفت‌وگوی خاص مورد بازیابی و استفاده قرار می‌گیرد.

خوشبختانه در ماژول `RunnableWithMessageHistory` نیز با در نظر گرفتن یک شناسه‌ی نشست (`session_id`) امکان مدیریت تاریخچه‌ی گفت‌وگو‌های مختلف فراهم شده است. یعنی به‌ازای هر گفت‌وگوی جداگانه می‌توانید یک شناسه‌ی یکتا و یک تاریخچه/حافظه تعریف کنید و با مشخص کردن این شناسه برای `RunnableWithMessageHistory` دقیقاً تاریخچه‌ی مربوط به همان گفت‌وگو را بازیابی کنید. به‌صورت کلی وقتی می‌خواهیم یک زنجیره را همراه با تاریخچه‌ی پیام تعریف کنیم از `RunnableWithMessageHistory` به‌شکل زیر استفاده می‌کنیم. توجه داشته باشید که منظور از `runnable` همان زنجیره‌ی ماست و `get_session_history` نیز تابع دلخواهی‌ست که به‌ازای شناسه‌ی نشست (`session_id`) حافظه‌ی مربوط به آن را باز می‌گرداند. در ادامه همراه با مثال این موارد را بیشتر متوجه خواهیم شد.

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(
    # The underlying runnable
    runnable,
    # A function that takes in a session id and returns a memory object
    get_session_history,
    # Other parameters that may be needed to align the inputs/outputs
    # of the Runnable with the memory object
    ...
)
```

برای اجرای این زنجیره‌ی همراه با حافظه نیز کافیست از تابع `invoke` استفاده کنیم و با مقداردهی به آرگومان `config` آن، شناسه‌ی نشست را مشخص کنیم.

```python
with_message_history.invoke(
    # Inputs of the chain
    {"input": "دستور ورودی کاربر"},
    # Configuration specifying the `session_id`,
    # which controls which conversation to load
    config={"configurable": {"session_id": "abc123"}}
)
```

حال بیایید با یک مثال کامل‌تر پیش برویم تا نحوه‌ی مدیریت خودکار تاریخچه در یک زنجیره را بررسی کنیم. ابتدا طبق معمول کلید API خود را تنظیم می‌کنیم.

```python
import getpass
import os
os.environ["COHERE_API_KEY"] = getpass.getpass()
```

حال می‌خواهیم یک قالب دستور طراحی کنیم که شامل یک پیام سیستمی، یک نگه‌دارنده‌ی پیام (تاریخچه‌ی پیام‌ها) و پیام ورودی کاربر است. سپس با استفاده از این قالب دستور و مدل گفت‌وگوی Cohere یک زنجیره می‌سازیم.

```python
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate

chat_model = ChatCohere(model='command-r-08-2024', temperature=0.2)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "تو یک مدل گفت‌وگو هستی که مانند دوست با کاربر صحبت می‌کنی.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)

chain = prompt | chat_model
```

حال نوبت به این می‌رسد که قابلیت مدیریت خودکار تاریخچه‌ی پیام‌ها را به این زنجیره اضافه کنیم. برای این کار ابتدا نیاز است تابعی بنویسیم که به‌ازای هر شناسه‌ی نشست (`session_id`) یک شیء تاریخچه‌ی پیام را بر می‌گرداند. برای این کار ابتدا یک دیکشنری به‌نام `store` تعریف می‌کنیم و در هنگام دریافت یک شناسه ابتدا بررسی می‌شود که آیا این کلید در `store` وجود دارد یا خیر. اگر وجود نداشته باشد یک حافظه ساخته می‌شود. در این‌جا ما از حافظه‌ی `ChatMessageHistory` که در درسنامه‌ی پیشین با آن آشنا شدیم استفاده کرده‌ایم. توجه داشته باشید که در پروژه‌های واقعی معمولاً از حافظه‌های پایداری نظیر `SQLChatMessageHistory` استفاده می‌شود

```python
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# A dictionary to store the chat history for each session id
store = {}

# A function that returns the chat history for a given session id
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # If the session id is not in the store dictionary
    if session_id not in store:
        # Create a new ChatMessageHistory object and add it to the store
        store[session_id] = ChatMessageHistory()
    # Return the message history for the session id
    return store[session_id]
```

حال کافیست زنجیره‌ی خود (`chain`) و تابع دریافت تاریخچه (`get_session_history`) را به `RunnableWithMessageHistory` ورودی دهیم و همچنین مشخص کنیم که در قالب پیام، ورودی کاربر باید به‌جای کلید `"input"` و تاریخچه‌ی پیام‌ها به‌جای `"chat_history"` قرار بگیرد.

همه‌چیز آماده‌ست. می‌توانیم به‌راحتی پیام خود را به‌همراه شناسه‌ی نشست ورودی دهیم و خوانش و درج در حافظه به‌صورت خودکار مدیریت می‌شود. به مثال زیر دقت کنید:

```python
while (True):

    # Get user message
    user_message = input('پیام خود را بنویسید ... (برای خروج 0 را بزنید)\n')

    # Exit the loop if the user enters '0'
    if (user_message == '0'):
        break
    else:
        print('User:', user_message, '\n')

        model_message = ''
        print('AI: ', end='')
        for chunk in with_message_history.stream({"input": user_message},
                                                 {"configurable": {"session_id": "1234"}}):
            model_message =  model_message + chunk.content
            print(chunk.content, end="", flush=True)
        print('\n')
```

{% endraw %}
