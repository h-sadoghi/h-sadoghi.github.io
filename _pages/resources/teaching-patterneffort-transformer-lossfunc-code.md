---
layout: legacy_page
title: آشنایی با توابع ضرر استفاده شده در ترنسفورمر ها
permalink: /resources/teaching-patterneffort-transformer-lossfunc-code/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/patterneffort/Transformer-LossFunc_code
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

# آشنایی با توابع ضرر استفاده شده در ترنسفورمر ها

---

<div markdown="1">

    <img loading="lazy" src="/assets/img/legacy/fum-logo-c752fa7c60.jpg" alt="STFT-overview">

</div>

**نویسنده**: صابره عسکری

**دانشگاه فردوسی مشهد**
**دانشکده مهندسی**
**گروه کامپیوتر**

---

دانشجوی ارشد هوش‌ مصنوعی دانشگاه فردوسی مشهد  
آزمایشگاه شناسایی الگو دکتر هادی صدوقی یزدی

---

# مقدمه

در سال‌های اخیر، معماری ترنسفورمر به‌عنوان نقطه‌ی عطفی در حوزه‌ی یادگیری عمیق و پردازش زبان طبیعی معرفی شده است. این معماری که نخستین بار در <a href="https://doi.org/10.48550/arXiv.1706.03762" target="_blank">
مقاله‌ی Attention Is All You Need توسط Vaswani و همکاران (۲۰۱۷)
</a> مطرح شد، توانست محدودیت‌های مدل‌های بازگشتی (RNN) و حافظه‌های طولانی‌کوتاه‌مدت (LSTM) را پشت سر بگذارد و با بهره‌گیری از مکانیزم Self-Attention، وابستگی‌های طولانی‌مدت در داده‌های متنی را با کارایی بالا مدل‌سازی کند.

با وجود اهمیت ساختار شبکه و مکانیزم توجه، آنچه فرآیند یادگیری ترنسفورمر را هدایت می‌کند، تابع ضرر (Loss Function) است. تابع ضرر به‌عنوان قطب‌نمای یادگیری عمل کرده و مسیر بهینه‌سازی وزن‌ها را مشخص می‌سازد. انتخاب و طراحی مناسب تابع ضرر نه‌تنها بر سرعت همگرایی مدل اثرگذار است، بلکه کیفیت نهایی نمایش‌های یادگرفته‌شده و توانایی مدل در انجام وظایف مختلف را تعیین می‌کند.

در مدل‌های زبانی بزرگ مانند GPT و BERT، معمولاً از Cross-Entropy Loss برای پیش‌بینی توکن‌های بعدی یا بازسازی بخش‌های حذف‌شده‌ی متن استفاده می‌شود. اما در وظایف خاص‌تر مانند ترجمه ماشینی، طبقه‌بندی متون یا یادگیری نمایش‌های معنایی، ترکیب یا جایگزینی این تابع با توابعی همچون Mean Squared Error (MSE)، Binary Cross-Entropy یا Contrastive Loss می‌تواند عملکرد مدل را به‌طور چشمگیری تغییر دهد.

هدف این مقاله، بررسی معماری ترنسفورمر از منظر طراحی و بهینه‌سازی توابع ضرر است. در این مسیر، ابتدا به معرفی اجزای اصلی ترنسفورمر پرداخته می‌شود، سپس انواع توابع ضرر رایج و نوین در آموزش این مدل‌ها تحلیل خواهند شد، و در نهایت تأثیر انتخاب تابع ضرر بر همگرایی، کیفیت یادگیری و مسیرهای پژوهشی آینده مورد بحث قرار می‌گیرد.

---

# مروری بر معماری ترنسفورمر

معماری ترنسفورمر در سال ۲۰۱۷ معرفی شد و به‌سرعت به ستون اصلی مدل‌های زبانی مدرن تبدیل گردید. ویژگی کلیدی این معماری، استفاده از مکانیزم **Self-Attention** است که امکان مدل‌سازی وابستگی‌های طولانی‌مدت در داده‌های متنی را فراهم می‌کند. برخلاف RNNها، ترنسفورمرها به‌صورت موازی عمل می‌کنند و همین امر باعث افزایش سرعت آموزش و مقیاس‌پذیری آن‌ها شده است.

---

## اجزای اصلی ترنسفورمر

#### 1. **Encoder**

- شامل چندین لایه متوالی از Self-Attention و شبکه‌های Feed-Forward.
- وظیفه: استخراج ویژگی‌های معنایی از ورودی.

#### 2. **Decoder**

- مشابه Encoder اما با مکانیزم Attention اضافی برای ارتباط با خروجی قبلی.
- وظیفه: تولید توالی خروجی (مثلاً ترجمه جمله).

#### 3. **Self-Attention**

- مکانیزمی برای محاسبه ارتباط هر توکن با سایر توکن‌ها در توالی.

#### 4. **Feed-Forward Networks**

- شبکه‌های کاملاً متصل (Fully Connected) که پس از Attention قرار می‌گیرند.
- وظیفه: تبدیل ویژگی‌های استخراج‌شده به نمایش‌های غنی‌تر.

#### 5. **Position Encoding**

- چون ترنسفورمر ذاتاً ترتیبی نیست، از کدگذاری موقعیت برای حفظ ترتیب توکن‌ها استفاده می‌شود.

---

## ارتباط با تابع ضرر

- خروجی Decoder معمولاً یک توزیع احتمالاتی روی واژگان است.
- این توزیع با توزیع واقعی مقایسه می‌شود و **تابع ضرر** (مثلاً Cross-Entropy) محاسبه می‌گردد.
- سپس گرادیان‌ها از طریق لایه‌های Attention و Feed-Forward به عقب انتشار می‌یابند و وزن‌ها به‌روزرسانی می‌شوند.

---

# نقش تابع ضرر در آموزش ترنسفورمر

تابع ضرر (Loss Function) قلب فرآیند یادگیری در ترنسفورمرهاست. این تابع مشخص می‌کند که خروجی مدل تا چه حد با داده‌های واقعی فاصله دارد و سپس با انتشار گرادیان‌ها در لایه‌های مختلف، وزن‌ها به‌روزرسانی می‌شوند. انتخاب درست تابع ضرر می‌تواند سرعت همگرایی و کیفیت نهایی مدل را به‌طور چشمگیری تحت تأثیر قرار دهد.

---

# انواع توابع ضرر در ترنسفورمرها

ترنسفورمرها بسته به وظیفه‌ای که برای آن‌ها طراحی یا تنظیم (Fine-Tune) می‌شوند، از توابع ضرر متفاوتی استفاده می‌کنند. در ادامه، مهم‌ترین توابع ضرر و کاربرد آن‌ها را بررسی می‌کنیم.

## 1. **Cross-Entropy Loss (مدل‌های زبانی)**

رایج‌ترین تابع ضرر در آموزش ترنسفورمرهای زبانی، **Cross-Entropy Loss** است. این تابع میزان اختلاف بین توزیع احتمالاتی پیش‌بینی‌شده توسط مدل و توزیع واقعی (برچسب‌ها) را اندازه‌گیری می‌کند.

- رایج‌ترین تابع ضرر در آموزش مدل‌های زبانی مثل GPT و BERT.
- هدف: کمینه کردن اختلاف بین توزیع پیش‌بینی‌شده و توزیع واقعی توکن‌ها.

### فرمول:

$$
Loss = - \sum_{i=1}^{C} y_i \cdot \log(\hat{p}_i)
$$

- $C$ : تعداد کلاس‌ها
- $y_i$: برچسب واقعی (بردار one-hot)
- $\hat{p}_i$: احتمال پیش‌بینی‌شده برای کلاس $i$

این فرمول باعث می‌شود مدل احتمال بیشتری به توکن‌های درست اختصاص دهد و به‌تدریج توزیع خروجی به توزیع واقعی نزدیک شود.

### مفهوم اصلی

در مسائل طبقه‌بندی، مدل برای هر ورودی یک **توزیع احتمال** روی کلاس‌ها تولید می‌کند. اما در واقعیت، هر نمونه فقط به یک کلاس تعلق دارد (مثلاً گربه یا سگ).  
Cross-Entropy Loss میزان فاصله بین این دو توزیع (پیش‌بینی مدل و حقیقت) را اندازه‌گیری می‌کند. هرچه مدل احتمال بیشتری به کلاس درست بدهد، مقدار Loss کمتر خواهد بود.

### چرا مهم است؟

- **هدایت یادگیری:** این تابع ضرر مدل را مجبور می‌کند احتمال کلاس درست را افزایش دهد و احتمال کلاس‌های اشتباه را کاهش دهد.
- **پایداری:** برخلاف برخی توابع دیگر، Cross-Entropy به خوبی با داده‌های بزرگ و چندکلاسه کار می‌کند.
- **کاربرد گسترده:** تقریباً در همه‌ی مدل‌های طبقه‌بندی مدرن (از شبکه‌های ساده تا ترنسفورمرها) استفاده می‌شود.

### مثال ساده

فرض کنید یک مدل برای یک تصویر سه کلاس پیش‌بینی می‌کند:

- کلاس A: 0.7
- کلاس B: 0.2
- کلاس C: 0.1

اگر برچسب واقعی کلاس A باشد، Cross-Entropy Loss مقدار کمی خواهد داشت چون مدل احتمال بالایی به کلاس درست داده است. اما اگر برچسب واقعی کلاس C باشد، Loss بزرگ خواهد شد چون مدل احتمال کمی به کلاس درست داده است.

### نکته

Cross-Entropy Loss در واقع **اطلاعات از دست‌رفته** بین دو توزیع را اندازه‌گیری می‌کند. اگر مدل کاملاً درست پیش‌بینی کند، Loss برابر صفر خواهد بود. اگر مدل کاملاً اشتباه باشد، Loss بزرگ می‌شود.

> کاربرد: پیش‌بینی توکن بعدی یا بازسازی بخش‌های حذف‌شده‌ی متن.

### Cross-Entropy Loss (طبقه‌بندی چندکلاسه)

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# داده‌های فرضی: 50 نمونه، 3 کلاس
torch.manual_seed(0)
outputs = torch.randn(50, 3)  # logits
labels = torch.randint(0, 3, (50,))  # برچسب‌های واقعی

loss_fn = nn.CrossEntropyLoss()
loss = loss_fn(outputs, labels)
print("Cross-Entropy Loss:", loss.item())

# محاسبه احتمال‌ها
probs = torch.softmax(outputs, dim=1).detach().numpy()

# رسم نمودار احتمال‌های اولین 10 نمونه
plt.figure(figsize=(10,6))
for i in range(10):
    plt.bar([f"class {j}" for j in range(3)], probs[i], alpha=0.6, label=f"Sample {i+1}")
plt.title("Predicted Probabilities (first 10 samples)")
plt.ylabel("Probability")
plt.legend()
plt.show()
```

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/outputcrossentropy-a95f8892e1-480.webp 480w, /assets/img/legacy/outputcrossentropy-a95f8892e1-800.webp 800w, /assets/img/legacy/outputcrossentropy-a95f8892e1-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/outputcrossentropy-a95f8892e1.png" alt="آشنایی با توابع ضرر استفاده شده در ترنسفورمر ها — illustration 2"></picture>

</div>

این کد یک مسئله‌ی طبقه‌بندی با ۳ کلاس و ۵۰ نمونه رو شبیه‌سازی می‌کنه.

- برای هر نمونه، مدل خروجی خام (logits) تولید می‌کنه.
- برچسب واقعی هر نمونه مشخصه (کلاس درست).
- کد اختلاف بین پیش‌بینی مدل و برچسب واقعی رو محاسبه می‌کنه.
- بعد احتمال هر کلاس برای چند نمونه‌ی اول محاسبه و به صورت نمودار میله‌ای نمایش داده می‌شه.
- مقدار محاسبه : Cross-Entropy Loss: 1.3174546957015991
  > خروجی تصویری: نشان می‌دهد مدل برای هر نمونه چه احتمالاتی برای کلاس‌ها در نظر گرفته است.

---

## 2. **Mean Squared Error (MSE)**

- برای وظایف رگرسیون یا پیش‌بینی مقادیر عددی.
- مدل خروجی عددی تولید می‌کند و MSE اختلاف میانگین مربعی بین خروجی و مقدار واقعی را محاسبه می‌کند.

### فرمول:

$$
\mathcal{L}_{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

### پارامترها

- **\(n\):** تعداد نمونه‌ها در مجموعه داده.
- **\(y_i\):** مقدار واقعی یا همان ground truth برای نمونه \(i\).
- **\(\hat{y}\_i\):** مقدار پیش‌بینی‌شده توسط مدل برای نمونه \(i\).

### توضیح

ابتدا اختلاف بین مقدار واقعی و پیش‌بینی‌شده محاسبه می‌شود. سپس این اختلاف به توان دو می‌رسد تا هم علامت منفی حذف شود و هم خطاهای بزرگ‌تر بیشتر جریمه شوند. در نهایت میانگین همه‌ی این خطاها گرفته می‌شود تا یک عدد کلی به‌عنوان معیار دقت مدل به دست آید. اگر MSE کوچک باشد، یعنی پیش‌بینی‌های مدل به طور میانگین نزدیک به مقادیر واقعی هستند. اگر بزرگ باشد، یعنی مدل در پیش‌بینی دچار خطاهای قابل توجه شده است.

> کاربرد: پیش‌بینی ویژگی‌های پیوسته مثل امتیاز احساسات یا مقادیر عددی در داده‌های علمی.

### Mean Squared Error (MSE)

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# داده‌های فرضی: 50 نمونه
torch.manual_seed(0)
preds = torch.randn(50)  # خروجی مدل
targets = torch.randn(50)  # مقادیر واقعی

loss_fn = nn.MSELoss()
loss = loss_fn(preds, targets)
print("MSE Loss:", loss.item())

# رسم مقایسه بین خروجی و مقدار واقعی
plt.figure(figsize=(10,6))
plt.plot(preds.numpy(), label="Predictions", marker='o')
plt.plot(targets.numpy(), label="Targets", marker='x')
plt.title("Predictions vs Targets")
plt.xlabel("Sample")
plt.ylabel("Value")
plt.legend()
plt.show()
```

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/outputmse-2f69e6d8fb-480.webp 480w, /assets/img/legacy/outputmse-2f69e6d8fb-800.webp 800w, /assets/img/legacy/outputmse-2f69e6d8fb-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/outputmse-2f69e6d8fb.png" alt="آشنایی با توابع ضرر استفاده شده در ترنسفورمر ها — illustration 3"></picture>

</div>

این کد یک مسئله‌ی رگرسیون با ۵۰ نمونه رو شبیه‌سازی می‌کنه.

- مدل برای هر نمونه یک مقدار عددی پیش‌بینی می‌کنه.
- داده‌ی واقعی هم برای هر نمونه داریم.
- کد اختلاف بین پیش‌بینی‌ها و داده‌های واقعی رو محاسبه می‌کنه.
- سپس نمودار خطی رسم می‌شود که پیش‌بینی‌ها و مقادیر واقعی را کنار هم نشان می‌دهد.
- مقدار محاسبه شده : MSE Loss: 2.2969024181365967
  > خروجی تصویری: نشان می‌دهد مدل چقدر به مقادیر واقعی نزدیک یا دور بوده است.

---

## 3. **Binary Cross-Entropy (BCE)**

- برای وظایف طبقه‌بندی دودویی (مثلاً مثبت/منفی یا درست/غلط).

### فرمول:

$$
Loss = - \frac{1}{n} \sum_{i=1}^{n} \Big[ y_i \cdot \log(p_i) + (1-y_i) \cdot \log(1-p_i) \Big]
$$

### پارامترها

- **\(n\):** تعداد نمونه‌ها در مجموعه داده.
- **\(y_i\):** برچسب واقعی برای نمونه \(i\). این مقدار یا ۰ (کلاس منفی) یا ۱ (کلاس مثبت) است.
- **\(p_i\):** احتمال پیش‌بینی‌شده توسط مدل برای نمونه \(i\) که بین ۰ و ۱ قرار دارد.

### توضیح

این فرمول برای مسائل دودویی (دو کلاس) استفاده می‌شود. اگر برچسب واقعی برابر ۱ باشد، بخش اول فرمول یعنی \(y_i \cdot \log(p_i)\) فعال می‌شود و مدل باید احتمال بالایی برای کلاس مثبت بدهد تا Loss کوچک شود. اگر برچسب واقعی برابر ۰ باشد، بخش دوم فرمول یعنی \((1-y_i) \cdot \log(1-p_i)\) فعال می‌شود و مدل باید احتمال کمی برای کلاس مثبت بدهد تا Loss کوچک شود.

به زبان ساده، BCE بررسی می‌کند که آیا مدل برای نمونه‌های مثبت احتمال نزدیک به ۱ و برای نمونه‌های منفی احتمال نزدیک به ۰ داده است یا نه. هرچه این پیش‌بینی‌ها دقیق‌تر باشند، مقدار Loss کمتر خواهد بود.

> Binary Cross-Entropy معیار استاندارد برای آموزش مدل‌های دودویی است و به مدل یاد می‌دهد که احتمال درست برای کلاس مثبت یا منفی را پیش‌بینی کند.

> کاربرد: تشخیص احساسات مثبت/منفی یا وجود/عدم وجود یک ویژگی خاص.

### Binary Cross-Entropy (BCE)

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# داده‌های فرضی: 50 نمونه، خروجی بین 0 و 1
torch.manual_seed(0)
outputs = torch.sigmoid(torch.randn(50))  # احتمالات پیش‌بینی
labels = torch.randint(0, 2, (50,)).float()  # برچسب‌های واقعی

loss_fn = nn.BCELoss()
loss = loss_fn(outputs, labels)
print("Binary Cross-Entropy Loss:", loss.item())

# رسم نمودار مقایسه
plt.figure(figsize=(10,6))
plt.scatter(range(50), outputs.numpy(), label="Predicted Probabilities", color='blue')
plt.scatter(range(50), labels.numpy(), label="True Labels", color='red', marker='x')
plt.title("Predicted vs True Labels")
plt.xlabel("Sample")
plt.ylabel("Probability / Label")
plt.legend()
plt.show()
```

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/outputbce-2cdb6cadb4-480.webp 480w, /assets/img/legacy/outputbce-2cdb6cadb4-800.webp 800w, /assets/img/legacy/outputbce-2cdb6cadb4-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/outputbce-2cdb6cadb4.png" alt="آشنایی با توابع ضرر استفاده شده در ترنسفورمر ها — illustration 4"></picture>

</div>

این کد یک مسئله‌ی دودویی (دو کلاس: ۰ یا ۱) با ۵۰ نمونه رو شبیه‌سازی می‌کنه.

- مدل برای هر نمونه یک احتمال بین ۰ و ۱ تولید می‌کنه.
- داده‌ی واقعی مشخص می‌کنه که نمونه مثبت (۱) یا منفی (۰) است.
- کد اختلاف بین احتمال پیش‌بینی و برچسب واقعی رو محاسبه می‌کنه.
- سپس نمودار پراکندگی رسم می‌شود که احتمال پیش‌بینی و برچسب واقعی را برای همه‌ی نمونه‌ها نشان می‌دهد.
- مقدار محاسبه شده: Binary Cross-Entropy Loss: 0.8622072339057922
  > خروجی تصویری: نشان می‌دهد مدل برای نمونه‌های مثبت و منفی چه احتمالاتی داده و چقدر درست یا غلط بوده.

---

## 4. **Contrastive Loss**

- برای یادگیری نمایش‌های معنایی (Representation Learning).
- هدف: نزدیک کردن نمونه‌های مشابه و دور کردن نمونه‌های غیرمشابه.

### فرمول:

$$
\mathcal{L}_{contrastive} = \frac{1}{2n} \sum_{i=1}^{n} \Big[ y_i \cdot D_i^2 + (1-y_i) \cdot \max(0, m - D_i)^2 \Big]
$$

### پارامترها

- **\(n\):** تعداد جفت نمونه‌ها در مجموعه داده.
- **\(y_i\):** برچسب برای جفت نمونه \(i\). اگر دو نمونه مشابه باشند مقدار ۱ و اگر غیرمشابه باشند مقدار ۰ است.
- **\(D_i\):** فاصله بین دو نمونه در جفت \(i\). این فاصله معمولاً با فاصله اقلیدسی بین بردارهای ویژگی محاسبه می‌شود.
- **\(m\):** مقدار margin یا آستانه‌ای که تعیین می‌کند نمونه‌های غیرمشابه باید حداقل چه فاصله‌ای داشته باشند.

### توضیح

Contrastive Loss برای آموزش مدل‌هایی استفاده می‌شود که باید **تشابه یا عدم تشابه بین نمونه‌ها** را یاد بگیرند. این تابع دو حالت دارد:

- اگر دو نمونه مشابه باشند (\(y_i=1\))، Loss برابر با مربع فاصله بین آن‌هاست. یعنی مدل تشویق می‌شود نمونه‌های مشابه را به هم نزدیک کند.
- اگر دو نمونه غیرمشابه باشند (\(y_i=0\))، Loss برابر با مربع \((m - D_i)\) است، البته فقط وقتی که فاصله کمتر از margin باشد. یعنی مدل تشویق می‌شود نمونه‌های غیرمشابه را حداقل به اندازه margin از هم دور کند.

به زبان ساده، Contrastive Loss مدل را وادار می‌کند **بردارهای مشابه نزدیک‌تر و بردارهای غیرمشابه دورتر** باشند. این ویژگی در مسائل مثل **تشخیص چهره، جستجوی تصویر و یادگیری نمایش‌ها** بسیار کاربردی است.

> Contrastive Loss یک ابزار کلیدی برای یادگیری نمایش‌های برداری است که بتوانند شباهت‌ها و تفاوت‌ها را به خوبی بازتاب دهند.

> کاربرد: در مدل‌های Sentence-BERT برای یادگیری نمایش‌های معنایی جملات.

### Contrastive Loss (نمایش‌های برداری)

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# داده‌های فرضی: 50 جفت نمونه
torch.manual_seed(0)
x1 = torch.randn(50, 5)
x2 = torch.randn(50, 5)
labels = torch.randint(0, 2, (50,))  # 1=مشابه، 0=غیرمشابه

# فاصله بین بردارها
distances = torch.norm(x1 - x2, dim=1)

# Contrastive Loss
margin = 1.0
losses = labels * distances**2 + (1-labels) * torch.clamp(margin - distances, min=0)**2
loss = losses.mean()
print("Contrastive Loss:", loss.item())

# رسم توزیع فاصله‌ها
plt.figure(figsize=(10,6))
plt.hist(distances[labels==1].numpy(), bins=10, alpha=0.6, label="Similar pairs")
plt.hist(distances[labels==0].numpy(), bins=10, alpha=0.6, label="Dissimilar pairs")
plt.title("Distribution of Distances")
plt.xlabel("Distance")
plt.ylabel("Count")
plt.legend()
plt.show()
```

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/outputcontrastive-7d562e61c0-480.webp 480w, /assets/img/legacy/outputcontrastive-7d562e61c0-800.webp 800w, /assets/img/legacy/outputcontrastive-7d562e61c0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/outputcontrastive-7d562e61c0.png" alt="آشنایی با توابع ضرر استفاده شده در ترنسفورمر ها — illustration 5"></picture>

</div>

این کد ۵۰ جفت نمونه رو شبیه‌سازی می‌کنه.

- هر جفت نمونه یا مشابه هستند یا غیرمشابه.
- فاصله‌ی برداری بین هر جفت محاسبه می‌شود.
- کد اختلاف بین فاصله‌های مشابه و غیرمشابه را محاسبه می‌کند.
- سپس نمودار هیستوگرام رسم می‌شود که توزیع فاصله‌ها را برای جفت‌های مشابه و غیرمشابه نشان می‌دهد.
- مقدار محاسبه شده : Contrastive Loss: 3.8370351791381836
  > خروجی تصویری: نشان می‌دهد نمونه‌های مشابه معمولاً فاصله‌ی کمی دارند و نمونه‌های غیرمشابه فاصله‌ی بیشتری.

---

## 5. **Triplet Loss**

- مشابه Contrastive Loss اما با سه نمونه: Anchor، Positive، Negative.
- هدف: فاصله Anchor با Positive کمتر از فاصله Anchor با Negative باشد.

### فرمول:

$$
\mathcal{L}_{triplet} = \frac{1}{n} \sum_{i=1}^{n} \max \big(0, D(a_i, p_i) - D(a_i, n_i) + m \big)
$$

### پارامترها

- **\(n\):** تعداد سه‌تایی‌ها (Triplets) در مجموعه داده.
- **\(a_i\):** نمونه Anchor یا همان نقطه‌ی مرجع.
- **\(p_i\):** نمونه Positive که باید به Anchor نزدیک باشد.
- **\(n_i\):** نمونه Negative که باید از Anchor دور باشد.
- **\(D(x,y)\):** فاصله بین دو نمونه (معمولاً فاصله اقلیدسی یا کسینوسی).
- **\(m\):** مقدار margin یا آستانه‌ای که تعیین می‌کند فاصله Anchor-Positive باید حداقل به اندازه‌ی margin کمتر از فاصله Anchor-Negative باشد.

### توضیح

Triplet Loss برای آموزش مدل‌هایی طراحی شده که باید **نمایش‌های برداری (embeddings)** را یاد بگیرند. ایده‌ی اصلی این است که برای هر Anchor، یک نمونه مشابه (Positive) و یک نمونه غیرمشابه (Negative) انتخاب می‌کنیم. مدل باید یاد بگیرد که فاصله Anchor-Positive کمتر از فاصله Anchor-Negative باشد، و این اختلاف حداقل به اندازه margin باشد.

اگر این شرط برقرار باشد، عبارت داخل max منفی می‌شود و Loss برابر صفر خواهد بود (یعنی مدل کارش را درست انجام داده). اگر شرط برقرار نباشد، Loss مثبت می‌شود و مدل باید وزن‌هایش را تغییر دهد تا نمایش‌ها اصلاح شوند.

به زبان ساده، Triplet Loss مدل را مجبور می‌کند **بردارهای مشابه نزدیک‌تر و بردارهای غیرمشابه دورتر** باشند، با یک فاصله‌ی ایمن (margin) بین آن‌ها. این ویژگی در مسائل مثل **تشخیص چهره، جستجوی تصویر، و یادگیری نمایش‌های معنایی** بسیار کاربردی است.

> Triplet Loss یک ابزار قدرتمند برای یادگیری نمایش‌های برداری است که روابط شباهت و تفاوت را به‌طور دقیق‌تر از Contrastive Loss مدل‌سازی می‌کند.

> کاربرد: یادگیری نمایش‌های معنایی دقیق‌تر در وظایف جستجو و تطبیق.

---

### Triplet Loss (Anchor, Positive, Negative)

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# فرض: بردارهای Anchor, Positive, Negative
anchor = torch.tensor([[1.0, 2.0]])
positive = torch.tensor([[1.2, 2.1]])
negative = torch.tensor([[3.0, 4.0]])

# تعریف TripletMarginLoss
loss_fn = nn.TripletMarginLoss(margin=1.0, p=2)
loss = loss_fn(anchor, positive, negative)

print("Triplet Loss:", loss.item())

# رسم نقاط Anchor, Positive, Negative
points = {
    'Anchor': anchor[0].numpy(),
    'Positive': positive[0].numpy(),
    'Negative': negative[0].numpy()
}

colors = {'Anchor':'blue','Positive':'green','Negative':'red'}

plt.figure(figsize=(6,6))
for label, coord in points.items():
    plt.scatter(coord[0], coord[1], color=colors[label], s=100, label=label)
    plt.text(coord[0]+0.05, coord[1]+0.05, label, fontsize=12)

# رسم خطوط بین Anchor-Positive و Anchor-Negative
plt.plot([anchor[0][0], positive[0][0]], [anchor[0][1], positive[0][1]], 'g--')
plt.plot([anchor[0][0], negative[0][0]], [anchor[0][1], negative[0][1]], 'r--')

plt.title(f"Triplet Loss Example (Loss={loss.item():.4f})")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)
plt.show()
```

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/tripleloss-d4d58c26a6-480.webp 480w, /assets/img/legacy/tripleloss-d4d58c26a6-800.webp 800w, /assets/img/legacy/tripleloss-d4d58c26a6-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/tripleloss-d4d58c26a6.png" alt="آشنایی با توابع ضرر استفاده شده در ترنسفورمر ها — illustration 6"></picture>

</div>

- نقاط **Anchor (آبی)**، **Positive (سبز)** و **Negative (قرمز)** روی نمودار دوبعدی رسم می‌شوند.
- خط سبز فاصله Anchor تا Positive را نشان می‌دهد.
- خط قرمز فاصله Anchor تا Negative را نشان می‌دهد.
- تابع Triplet Loss تلاش می‌کند فاصله Anchor-Positive را **کمتر** از فاصله Anchor-Negative کند (با در نظر گرفتن margin).

---

## جدول مقایسه توابع ضرر

| تابع ضرر                       | فرمول                                                       | کاربرد اصلی              | نکته کلیدی                                                                         |
| ------------------------------ | ----------------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------- |
| **Cross-Entropy Loss**         | \(- \sum y_i \cdot \log(p_i)\)                              | طبقه‌بندی چندکلاسه       | مدل را مجبور می‌کند احتمال کلاس درست را بالا ببرد                                  |
| **MSE Loss**                   | \(\frac{1}{n} \sum (y_i - \hat{y}\_i)^2\)                   | رگرسیون                  | به خطاهای بزرگ حساس است و میانگین فاصله پیش‌بینی‌ها را نشان می‌دهد                 |
| **Binary Cross-Entropy (BCE)** | \(- \frac{1}{n} \sum [y_i \log(p_i) + (1-y_i)\log(1-p_i)]\) | طبقه‌بندی دودویی         | بررسی می‌کند که مدل برای مثبت‌ها احتمال نزدیک ۱ و برای منفی‌ها احتمال نزدیک ۰ بدهد |
| **Contrastive Loss**           | \(\frac{1}{2n} \sum [y_i D_i^2 + (1-y_i)\max(0, m-D_i)^2]\) | یادگیری شباهت/عدم شباهت  | نمونه‌های مشابه را نزدیک و غیرمشابه‌ها را دور نگه می‌دارد                          |
| **Triplet Loss**               | \(\frac{1}{n} \sum \max(0, D(a,p) - D(a,n) + m)\)           | یادگیری نمایش‌های برداری | Anchor-Positive باید نزدیک‌تر از Anchor-Negative باشد با فاصله‌ی margin            |

## منابع

| موضوع                                | منبع                                                                                                                          | لینک                                                                                                         |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| معماری ترنسفورمر                     | Vaswani et al. (2017). _Attention Is All You Need_. NeurIPS                                                                   | <a> [Paper](https://doi.org/10.48550/arXiv.1706.03762)                                                       |
| مبانی توابع ضرر (Cross-Entropy, MSE) | Goodfellow, I., Bengio, Y., & Courville, A. (2016). _Deep Learning_. MIT Press                                                | [Book](https://www.deeplearningbook.org/)                                                                    |
| Cross-Entropy در ترنسفورمرها         | Hackernoon. (2023). _Cross-Entropy Loss Analysis in Transformer Networks_                                                     | [Article](https://hackernoon.com/cross-entropy-loss-analysis-in-transformer-networks)                        |
| Binary Cross-Entropy                 | Towards Data Science. (2023). _Understanding Binary Cross-Entropy in Machine Learning_                                        | [Article](https://towardsdatascience.com/understanding-binary-cross-entropy-in-machine-learning-4d4afcba6f5) |
| Contrastive Loss                     | Hadsell, R., Chopra, S., & LeCun, Y. (2006). _Dimensionality Reduction by Learning an Invariant Mapping_. CVPR                | [Paper](https://doi.org/10.1109/CVPR.2006.100)                                                               |
| Triplet Loss                         | Schroff, F., Kalenichenko, D., & Philbin, J. (2015). _FaceNet: A Unified Embedding for Face Recognition and Clustering_. CVPR | [Paper](https://doi.org/10.1109/CVPR.2015.7298682)                                                           |

{% endraw %}
