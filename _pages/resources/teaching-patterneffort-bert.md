---
layout: legacy_page
title: BERT
permalink: /resources/teaching-patterneffort-bert/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/patterneffort/BERT/
legacy_group: Pattern recognition and machine learning
legacy_dir: rtl
lang: fa
---

{% raw %}

# Bert

**نویسنده**: محمد صالح علی اکبری

<img loading="lazy" alt="BERT — illustration 1" src="https://quera.org/media/CACHE/images/public/avatars/8e111895562e470888dde40a0018e0eb/f93253aa8612f91a5a7b7f9d25cfabd4.jpg" />

<a href="https://github.com/mohammadsaleh40" target = "_blank">
Course illustration

Course illustration
</a>

دانشجوی مقطع کارشناسی ارشد

دانشکده: مرکز آموزش الکترونیکی

رشته: مهندسی کامپیوتر گرایش هوش مصنوعی و رباتیک

<iframe src="https://www.aparat.com/video/video/embed/videohash/pobvma9/vt/frame"

        allowFullScreen="true"


        width="1027" height="530"


        style="max-width: 100%; border: none;">

</iframe>

## ویدئو پیاده سازی BERT در Google colab و سیستم Local جهت embeding

<iframe src="https://www.aparat.com/video/video/embed/videohash/ikk00l5/vt/frame"

        allowFullScreen="true"


        width="1027" height="530"


        style="max-width: 100%; border: none;">

</iframe>

## مدل‌های زبانی

چند سال پیش مربی یک کلاس برنامه و تفکر الگوریتمی بودم. در بین پروژه‌هایی که دانش‌آموزان انجام می‌دادن یک روز یکی از دانش‌آموزان کلاس ایده ساختن محصولی مشابه <a href="https://en.wikipedia.org/wiki/Cortana_\(virtual_assistant\" target="_blank">کورتانا</a> ویندوز پیش اومد.

<img loading="lazy" alt="BERT — illustration 2" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Microsoft_Cortana_transparent.svg/120px-Microsoft_Cortana_transparent.svg.png" decoding="async" class="mw-file-element" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Microsoft_Cortana_transparent.svg/250px-Microsoft_Cortana_transparent.svg.png 2x" >

این دانش‌آموز می‌خواست به کمک مجموعه بزرگی از شرط‌ها شرایط رو برای یک گفت و گو اولیه فراهم کنه.  
اگر گفت:«سلام.» برنامه بگه :«سلام چطوری؟» و … . خوب این کار برای یک دانش‌آموز ممکن نبود. حتی برای یک گروه عظیم از کارمندان یک شرکت هم حتی شاید ممکن نباشه. پس اینجا به یک برنامه‌ای نیاز داریم که جملات و گفت و گوها رو بیشتر از یک string خشک و ساده ببینه.

<a href="https://static.vecteezy.com/system/resources/previews/036/171/064/non_2x/chatbot-using-and-chatting-artificial-intelligence-chat-bot-developed-by-tech-company-digital-chat-bot-robot-application-conversation-assistant-concept-optimizing-language-models-for-dialogue-vector.jpg">Original illustration source</a>

### تبدیل کردن به قطعات کوچک تر از جمله و عبارت

برای این که کامپیوتر بتونه برای خودش دیکشنری از معانی و مفاهیم جملات درست کنه درست کردن دیکشنری از کل عبارت‌های ممکن کار سختی هست. در طرف دیگر اگر زبان را از دید بخش‌های کوچک تر از کلمه یعنی حرف ببینیم کامپیوتر به سختی درکی از زبان بدست می‌آورد.

<h4>
<a href="https://en.wikipedia.org/wiki/Large_language_model#Tokenization" target="_blank">
Tokenization
</a>
</h4>

گاهی ممکن است نیاز باشد که درباره کلماتی جدید صحبت به میان بیاد پس به حروف کوچک و تعیین کردن شرط و شروط در مورد حروف داریم ولی اگر فقط حروف باشد پیچیده می‌شود پس کلمات هم باید باشند. از طرفی پسوندهای معنی دار هم جایگاه مهمی در زبان دارند و تعیین کردن شرط برای آن‌ها هم می‌تواند کمک کننده باشد پس با معرفی کردن همه آن‌ها به ماشین شاید به حل مسئله چت بات برسیم.

| کلمه دارای پیشوند | پیوشند | کلمه دارای پسوند | پسوند |
| ----------------- | ------ | ---------------- | ----- |
| می‌روم            | می##   | خانه‌ام          | ##ام  |

به فرایند تبدیل کردن جملات و عبارت‌های متنی به این بخش‌های قابل فهم برای کامپیوتر Tokenization می‌گویند.  
روش‌های متفاوتی برای این کار وجود دارد. در مقاله BERT از روش **WordPiece Tokenization** استفاده شده است.

در این روش، برخلاف روش‌های ساده‌تری مثل جدا کردن جمله بر اساس فاصله‌ها (space) یا استفاده از فهرستی ثابت از کلمات، مدل ابتدا یک واژگان (vocabulary) پایه دارد و سپس سعی می‌کند کلمات جدید را به ترکیبی از قطعات کوچک‌تر که در آن واژگان موجود هستند تبدیل کند.

برای مثال اگر واژه‌ی «playing» در واژگان نباشد، مدل می‌تواند آن را به صورت «play» و «##ing» بنویسد. علامت «##» نشان می‌دهد که بخش دوم در ادامه‌ی بخش قبلی آمده است، نه در ابتدای یک کلمه‌ی جدید.

این ایده از روش‌های مشابهی مانند **Byte Pair Encoding (BPE)** الهام گرفته است. در روش BPE، پرتکرارترین جفت نویسه‌ها به تدریج ترکیب می‌شوند تا یک واژگان فشرده و کارآمد ساخته شود. WordPiece نیز فرآیندی شبیه دارد، با این تفاوت که به جای تکرار ساده‌ی نویسه‌ها، احتمال وقوع توالی‌ها را در کل داده‌های آموزشی بررسی می‌کند و بر اساس آن تصمیم می‌گیرد چه ترکیب‌هایی باید در واژگان بمانند.

هدف از این روش ایجاد تعادلی بین فهم دقیق واژه‌ها و توانایی برخورد با کلمات ناشناخته است. به این ترتیب مدل می‌تواند هم واژه‌های پرتکرار را به عنوان یک واحد مستقل یاد بگیرد، و هم واژه‌های جدید را از ترکیب قطعات شناخته‌شده بسازد.

به کمک این نوع Tokenization، مدل BERT قادر است با متون بسیار متنوعی روبه‌رو شود و در عین حال معنا و ساختار واژه‌ها را تا حد زیادی حفظ کند. این مرحله یکی از کلیدهای اصلی موفقیت BERT در درک زبان طبیعی به شمار می‌رود.

###### پیش بینی کلمه بعدی

حالا که تونستیم اجزای زبان موجود در گفت و گو رو برای ماشین تعریف کنیم یک ایده برای ساختن توالی از این اجزا پیش بینی مرحله به مرحله جزئ در این دنباله‌ها است ولی یک مشکل وجود دارد. به این دو عبارت دقت کنید:

«شیر آب چکه می‌کند.»

«شیر تشنه است و آب می‌خواهد.»

این دو جمله در ارتباط با یک مشکل هستند. اگر در ادامه بنویسیم:«راهکار تو برای حل مشکل چیست؟» این ماشین باید برای جمله اول در ارتباط با تعمیر شیر آب صحبت کند و برای جمله دوم در مورد آب رسانی به شیر صحبت کند.

### درک معنای پویای کلمات

حال این سؤال پیش می‌آید: چگونه می‌توان به مدل آموخت که یک توکن مانند «شیر» در دو جمله مختلف، معانی کاملاً متفاوتی دارد؟

پاسخ در معماری‌های پیشرفته‌ای نهفته است که از **مکانیزم توجه (Attention)** استفاده می‌کنند. در این معماری‌ها، هر کلمه نه به صورت مجزا، بلکه در بستر کامل جمله پردازش می‌شود.

وقتی جمله وارد مدل می‌شود، نمایش اولیه هر کلمه (embedding اولیه) ثابت است، اما در حین پردازش، این نمایش‌ها به طور پویا بر اساس **همه کلمات موجود در جمله** به‌روزرسانی می‌شوند.

### مکانیزم توجه چگونه عمل می‌کند؟

هر کلمه در جمله با تمام کلمات دیگر (از جمله خودش) تعامل برقرار می‌کند. مدل به طور خودکار یاد می‌گیرد که برای درک هر کلمه، به کدام کلمات دیگر باید «توجه» بیشتری کند.

- در جمله «شیر آب چکه می‌کند»:

  - کلمه «شیر» با «آب»، «چکه» و «می‌کند» ارتباط معنایی قوی برقرار می‌کند
  - در نتیجه، نمایش نهایی آن به سمت مفاهیم مرتبط با شیرآلات و لوازم خانگی حرکت می‌کند

- در جمله «شیر تشنه است و آب می‌خواهد»:

  - کلمه «شیر» با «تشنه»، «آب» و «می‌خواهد» تعامل می‌کند
  - نمایش نهایی آن به موجود زنده، حیوان و طبیعت نزدیک می‌شود

#### نتیجه این فرآیند چیست؟

پس از گذر از چندین لایه پردازش، هر کلمه یک **نمایش زمینه‌ای (Contextualized Representation)** پیدا می‌کند. این نمایش نه تنها معنای اصلی کلمه، بلکه نقش و معنای آن در جمله فعلی را نیز در بر می‌گیرد.

به این ترتیب، مدل می‌تواند به طور خودکار ابهام‌زدایی کند و برای یک توالی یکسان از کلمات («راهکار تو برای حل مشکل چیست؟») پاسخ‌های متناسب با زمینه ارائه دهد - بدون نیاز به قواعد دستی یا شرط‌های از پیش تعریف شده.

این توانایی درک پویای زبان، پایه و اساس مدل‌های زبانی مدرن است که می‌توانند گفت‌وگوهای طبیعی و معناداری با انسان برقرار کنند.

##### شیر با شیر چه فرقی داره؟

در زیر یک کد ارائه می‌کنم که کلمه شیر به همراه چند کلمه دیگر در جملات مختلف را بررسی می‌کند. نمودار آن نکات جالبی دارد.

```python
import torch
import numpy as np
import os
from transformers import AutoTokenizer, AutoModel
from sklearn.manifold import TSNE
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# --- بارگذاری مدل و توکنایزر ---
model_path = os.path.abspath("persian_bert_tiny_final_model_large_2")
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModel.from_pretrained(model_path, local_files_only=True)
model.eval()

# --- داده‌های ورودی ---

# لیست کلمات یا جملات نمونه
sentences = [
    "شیر در بیابان گرسنه است.",
    "شیر حیوان وحشی است.",
    "شیر خانه ما چکه می‌کند.",
    "شیر تشنه است و آب نیاز دارد.",
    "شیر خانه ما نشتی دارد.",
    "شیر حیوان درنده‌ای است.",

]
words_to_visualize = ["شیر","آب","حیوان","درنده","شیرالات","چکه"] # تعداد کلمات بیشتر از تعداد جملات


# --- استخراج embeddingها ---
embeddings = []
labels = []

for sent in sentences:
    inputs = tokenizer(sent, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
        last_hidden_states = outputs.last_hidden_state  # [1, seq_len, hidden_size]

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    for word in words_to_visualize:
        word_tokens = tokenizer.tokenize(word)
        if word_tokens and word_tokens[0] in tokens:
            start_idx = tokens.index(word_tokens[0])
            emb = last_hidden_states[0, start_idx].numpy()
            embeddings.append(emb)
            labels.append(f"{word} (in: {sent[:20]}...)")

# --- بررسی وجود داده ---
if len(embeddings) == 0:
    print("No embeddings found!")
else:
    print(f"Found {len(embeddings)} embeddings.")
    embeddings = np.array(embeddings)

    # --- t-SNE ---
    n_samples = len(embeddings)
    if n_samples < 2:
        print("Need at least 2 samples for t-SNE.")
    else:
        perplexity = min(30, n_samples - 1) if n_samples > 1 else 1
        tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
        embeddings_2d = tsne.fit_transform(embeddings)

        # --- ساخت نمودار با Plotly ---
        fig = go.Figure()

        # اضافه کردن نقاط
        fig.add_trace(go.Scatter(
            x=embeddings_2d[:, 0],
            y=embeddings_2d[:, 1],
            mode='markers+text',
            text=labels,
            textposition="top center",
            marker=dict(size=10, color='lightblue', line=dict(width=1, color='black')),
            hovertemplate='%{text}<extra></extra>'
        ))

        fig.update_layout(
            title="t-SNE Visualization of BERT Embeddings for Selected Words",
            xaxis_title="t-SNE Component 1",
            yaxis_title="t-SNE Component 2",
            width=900,
            height=700,
            showlegend=False,
            font=dict(size=12),
            plot_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridcolor='lightgray')
        )

        # --- ذخیره به عنوان HTML استاتیک ---
        output_file = "embeddings_tsne.html"
        pio.write_html(fig, file=output_file, full_html=True, include_plotlyjs='cdn')
        print(f"Interactive plot saved to: {os.path.abspath(output_file)}")
```

<div markdown="1">

<div id="275b82cc-16ce-4bf7-ab1a-794190fb6ecd" class="plotly-graph-div js-plotly-plot" markdown="1">

<div class="plot-container plotly" markdown="1">

<div class="user-select-none svg-container" markdown="1">

<svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="900" height="700"><defs id="defs-70b7b9"><g class="clips"><clipPath id="clip70b7b9xyplot" class="plotclip"><rect width="740" height="520"></rect></clipPath><clipPath class="axesclip" id="clip70b7b9x"><rect x="80" y="0" width="740" height="700"></rect></clipPath><clipPath class="axesclip" id="clip70b7b9y"><rect x="0" y="100" width="900" height="520"></rect></clipPath><clipPath class="axesclip" id="clip70b7b9xy"><rect x="80" y="100" width="740" height="520"></rect></clipPath></g><g class="gradients"></g><g class="patterns"></g></defs><g class="bglayer"></g><g class="draglayer cursor-crosshair"><g class="xy"><rect class="nsewdrag drag" data-subplot="xy" x="80" y="100" width="740" height="520"></rect><rect class="nwdrag drag cursor-nw-resize" data-subplot="xy" x="60" y="80" width="20" height="20"></rect><rect class="nedrag drag cursor-ne-resize" data-subplot="xy" x="820" y="80" width="20" height="20"></rect><rect class="swdrag drag cursor-sw-resize" data-subplot="xy" x="60" y="620" width="20" height="20"></rect><rect class="sedrag drag cursor-se-resize" data-subplot="xy" x="820" y="620" width="20" height="20"></rect><rect class="ewdrag drag cursor-ew-resize" data-subplot="xy" x="154" y="620.5" width="592" height="20"></rect><rect class="wdrag drag cursor-w-resize" data-subplot="xy" x="80" y="620.5" width="74" height="20"></rect><rect class="edrag drag cursor-e-resize" data-subplot="xy" x="746" y="620.5" width="74" height="20"></rect><rect class="nsdrag drag cursor-ns-resize" data-subplot="xy" x="59.5" y="152" width="20" height="416"></rect><rect class="sdrag drag cursor-s-resize" data-subplot="xy" x="59.5" y="568" width="20" height="52"></rect><rect class="ndrag drag cursor-n-resize" data-subplot="xy" x="59.5" y="100" width="20" height="52"></rect></g></g><g class="layer-below"><g class="imagelayer"></g><g class="shapelayer"></g></g><g class="cartesianlayer"><g class="subplot xy"><g class="layer-subplot"><g class="shapelayer"></g><g class="imagelayer"></g></g><g class="minor-gridlayer"><g class="x"></g><g class="y"></g></g><g class="gridlayer"><g class="x"><path class="xgrid crisp" transform="translate(177.28,0)" d="M0,100v520"></path><path class="xgrid crisp" transform="translate(291.28999999999996,0)" d="M0,100v520"></path><path class="xgrid crisp" transform="translate(519.31,0)" d="M0,100v520"></path><path class="xgrid crisp" transform="translate(633.31,0)" d="M0,100v520"></path><path class="xgrid crisp" transform="translate(747.32,0)" d="M0,100v520"></path></g><g class="y"><path class="ygrid crisp" transform="translate(0,587.64)" d="M80,0h740"></path><path class="ygrid crisp" transform="translate(0,508.1)" d="M80,0h740"></path><path class="ygrid crisp" transform="translate(0,428.57)" d="M80,0h740"></path><path class="ygrid crisp" transform="translate(0,269.51)" d="M80,0h740"></path><path class="ygrid crisp" transform="translate(0,189.97)" d="M80,0h740"></path><path class="ygrid crisp" transform="translate(0,110.44)" d="M80,0h740"></path></g></g><g class="zerolinelayer"><path class="xzl zl crisp" transform="translate(405.3,0)" d="M0,100v520"></path><path class="yzl zl crisp" transform="translate(0,349.03999999999996)" d="M80,0h740"></path></g><g class="layer-between"><g class="shapelayer"></g><g class="imagelayer"></g></g><path class="xlines-below"></path><path class="ylines-below"></path><g class="overlines-below"></g><g class="xaxislayer-below"></g><g class="yaxislayer-below"></g><g class="overaxes-below"></g><g class="overplot"><g class="xy" transform="translate(80,100)" clip-path="url(#clip70b7b9xyplot)"><g class="scatterlayer mlayer"><g class="trace scatter trace2882bc"><g class="fills"></g><g class="errorbars"></g><g class="lines"></g><g class="points"><path class="point" transform="translate(593.24,442.68)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(344.44,487.75)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(696.75,278.42)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(551.17,152.34)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(300.02,203.46)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(43.25,241.19)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(146.07,76.17)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(395.88,32.25)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(438.33,316.41)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path><path class="point" transform="translate(187.22,368.47)" d="M5,0A5,5 0 1,1 0,-5A5,5 0 0,1 5,0Z"></path></g><g class="text"><g class="textpoint" transform="translate(0,-10.25)"><text x="593.24" y="442.68" data-unformatted="شیر (in: شیر در بیابان گرسنه ...)" data-math="N" text-anchor="middle">شیر (in: شیر در بیابان گرسنه ...)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="344.44" y="487.75" data-unformatted="شیر (in: شیر حیوان وحشی است....)" data-math="N" text-anchor="middle">شیر (in: شیر حیوان وحشی است....)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="696.75" y="278.42" data-unformatted="حیوان (in: شیر حیوان وحشی است....)" data-math="N" text-anchor="middle">حیوان (in: شیر حیوان وحشی است....)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="551.17" y="152.34" data-unformatted="شیر (in: شیر خانه ما چکه می‌ک...)" data-math="N" text-anchor="middle">شیر (in: شیر خانه ما چکه می‌ک...)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="300.02" y="203.46" data-unformatted="چکه (in: شیر خانه ما چکه می‌ک...)" data-math="N" text-anchor="middle">چکه (in: شیر خانه ما چکه می‌ک...)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="43.25" y="241.19" data-unformatted="شیر (in: شیر تشنه است و آب نی...)" data-math="N" text-anchor="middle">شیر (in: شیر تشنه است و آب نی...)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="146.07" y="76.17" data-unformatted="آب (in: شیر تشنه است و آب نی...)" data-math="N" text-anchor="middle">آب (in: شیر تشنه است و آب نی...)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="395.88" y="32.25" data-unformatted="شیر (in: شیر خانه ما نشتی دار...)" data-math="N" text-anchor="middle">شیر (in: شیر خانه ما نشتی دار...)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="438.33" y="316.41" data-unformatted="شیر (in: شیر حیوان درنده‌ای ا...)" data-math="N" text-anchor="middle">شیر (in: شیر حیوان درنده‌ای ا...)</text></g><g class="textpoint" transform="translate(0,-10.25)"><text x="187.22" y="368.47" data-unformatted="حیوان (in: شیر حیوان درنده‌ای ا...)" data-math="N" text-anchor="middle">حیوان (in: شیر حیوان درنده‌ای ا...)</text></g></g></g></g></g></g><path class="xlines-above crisp" d="M0,0"></path><path class="ylines-above crisp" d="M0,0"></path><g class="overlines-above"></g><g class="xaxislayer-above"><g class="xtick"><text text-anchor="middle" x="0" y="633" data-unformatted="−100" data-math="N" transform="translate(177.28,0)">−100</text></g><g class="xtick"><text text-anchor="middle" x="0" y="633" data-unformatted="−50" data-math="N" transform="translate(291.28999999999996,0)">−50</text></g><g class="xtick"><text text-anchor="middle" x="0" y="633" data-unformatted="0" data-math="N" transform="translate(405.3,0)">0</text></g><g class="xtick"><text text-anchor="middle" x="0" y="633" data-unformatted="50" data-math="N" transform="translate(519.31,0)">50</text></g><g class="xtick"><text text-anchor="middle" x="0" y="633" data-unformatted="100" data-math="N" transform="translate(633.31,0)">100</text></g><g class="xtick"><text text-anchor="middle" x="0" y="633" data-unformatted="150" data-math="N" transform="translate(747.32,0)">150</text></g></g><g class="yaxislayer-above"><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="−150" data-math="N" transform="translate(0,587.64)">−150</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="−100" data-math="N" transform="translate(0,508.1)">−100</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="−50" data-math="N" transform="translate(0,428.57)">−50</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="0" data-math="N" transform="translate(0,349.03999999999996)">0</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="50" data-math="N" transform="translate(0,269.51)">50</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="100" data-math="N" transform="translate(0,189.97)">100</text></g><g class="ytick"><text text-anchor="end" x="79" y="4.199999999999999" data-unformatted="150" data-math="N" transform="translate(0,110.44)">150</text></g></g><g class="overaxes-above"></g></g></g><g class="polarlayer"></g><g class="smithlayer"></g><g class="ternarylayer"></g><g class="geolayer"></g><g class="funnelarealayer"></g><g class="pielayer"></g><g class="iciclelayer"></g><g class="treemaplayer"></g><g class="sunburstlayer"></g><g class="glimages"></g></svg>

<div class="gl-container" markdown="1">

</div>

<svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="900" height="700"><defs id="topdefs-70b7b9"><g class="clips"></g></defs><g class="indicatorlayer"></g><g class="layer-above"><g class="imagelayer"></g><g class="shapelayer"></g></g><g class="selectionlayer"></g><g class="infolayer"><g class="g-gtitle"><text class="gtitle" x="45" y="50" text-anchor="start" dy="0em" data-unformatted="t-SNE Visualization of BERT Embeddings for Selected Words" data-math="N">t-SNE Visualization of BERT Embeddings for Selected Words</text></g><g class="g-xtitle"><text class="xtitle" x="450" y="662.3164031982421" text-anchor="middle" data-unformatted="t-SNE Component 1" data-math="N">t-SNE Component 1</text></g><g class="g-ytitle"><text class="ytitle" transform="rotate(-90,31.28359375,360)" x="31.28359375" y="360" text-anchor="middle" data-unformatted="t-SNE Component 2" data-math="N">t-SNE Component 2</text></g></g><g class="menulayer"></g><g class="zoomlayer"></g></svg>

<div class="modebar-container" markdown="1">

<div id="modebar-70b7b9" class="modebar modebar--hover ease-bg" markdown="1">

<div class="modebar-group" markdown="1">

<a rel="tooltip" class="modebar-btn" data-title="Download plot as a png" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a>

</div>

<div class="modebar-group" markdown="1">

<a rel="tooltip" class="modebar-btn active" data-title="Zoom" data-attr="dragmode" data-val="zoom" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m1000-25l-250 251c40 63 63 138 63 218 0 224-182 406-407 406-224 0-406-182-406-406s183-406 407-406c80 0 155 22 218 62l250-250 125 125z m-812 250l0 438 437 0 0-438-437 0z m62 375l313 0 0-312-313 0 0 312z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Pan" data-attr="dragmode" data-val="pan" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m1000 350l-187 188 0-125-250 0 0 250 125 0-188 187-187-187 125 0 0-250-250 0 0 125-188-188 186-187 0 125 252 0 0-250-125 0 187-188 188 188-125 0 0 250 250 0 0-126 187 188z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Box Select" data-attr="dragmode" data-val="select" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m0 850l0-143 143 0 0 143-143 0z m286 0l0-143 143 0 0 143-143 0z m285 0l0-143 143 0 0 143-143 0z m286 0l0-143 143 0 0 143-143 0z m-857-286l0-143 143 0 0 143-143 0z m857 0l0-143 143 0 0 143-143 0z m-857-285l0-143 143 0 0 143-143 0z m857 0l0-143 143 0 0 143-143 0z m-857-286l0-143 143 0 0 143-143 0z m286 0l0-143 143 0 0 143-143 0z m285 0l0-143 143 0 0 143-143 0z m286 0l0-143 143 0 0 143-143 0z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Lasso Select" data-attr="dragmode" data-val="lasso" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 1031 1000" class="icon" height="1em" width="1em"><path d="m1018 538c-36 207-290 336-568 286-277-48-473-256-436-463 10-57 36-108 76-151-13-66 11-137 68-183 34-28 75-41 114-42l-55-70 0 0c-2-1-3-2-4-3-10-14-8-34 5-45 14-11 34-8 45 4 1 1 2 3 2 5l0 0 113 140c16 11 31 24 45 40 4 3 6 7 8 11 48-3 100 0 151 9 278 48 473 255 436 462z m-624-379c-80 14-149 48-197 96 42 42 109 47 156 9 33-26 47-66 41-105z m-187-74c-19 16-33 37-39 60 50-32 109-55 174-68-42-25-95-24-135 8z m360 75c-34-7-69-9-102-8 8 62-16 128-68 170-73 59-175 54-244-5-9 20-16 40-20 61-28 159 121 317 333 354s407-60 434-217c28-159-121-318-333-355z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a>

</div>

<div class="modebar-group" markdown="1">

<a rel="tooltip" class="modebar-btn" data-title="Zoom in" data-attr="zoom" data-val="in" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 875 1000" class="icon" height="1em" width="1em"><path d="m1 787l0-875 875 0 0 875-875 0z m687-500l-187 0 0-187-125 0 0 187-188 0 0 125 188 0 0 187 125 0 0-187 187 0 0-125z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Zoom out" data-attr="zoom" data-val="out" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 875 1000" class="icon" height="1em" width="1em"><path d="m0 788l0-876 875 0 0 876-875 0z m688-500l-500 0 0 125 500 0 0-125z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Autoscale" data-attr="zoom" data-val="auto" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m250 850l-187 0-63 0 0-62 0-188 63 0 0 188 187 0 0 62z m688 0l-188 0 0-62 188 0 0-188 62 0 0 188 0 62-62 0z m-875-938l0 188-63 0 0-188 0-62 63 0 187 0 0 62-187 0z m875 188l0-188-188 0 0-62 188 0 62 0 0 62 0 188-62 0z m-125 188l-1 0-93-94-156 156 156 156 92-93 2 0 0 250-250 0 0-2 93-92-156-156-156 156 94 92 0 2-250 0 0-250 0 0 93 93 157-156-157-156-93 94 0 0 0-250 250 0 0 0-94 93 156 157 156-157-93-93 0 0 250 0 0 250z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a><a rel="tooltip" class="modebar-btn" data-title="Reset axes" data-attr="zoom" data-val="reset" data-toggle="false" data-gravity="n" data-btn-style-event-added="true"><svg viewBox="0 0 928.6 1000" class="icon" height="1em" width="1em"><path d="m786 296v-267q0-15-11-26t-25-10h-214v214h-143v-214h-214q-15 0-25 10t-11 26v267q0 1 0 2t0 2l321 264 321-264q1-1 1-4z m124 39l-34-41q-5-5-12-6h-2q-7 0-12 3l-386 322-386-322q-7-4-13-4-7 2-12 7l-35 41q-4 5-3 13t6 12l401 334q18 15 42 15t43-15l136-114v109q0 8 5 13t13 5h107q8 0 13-5t5-13v-227l122-102q5-5 6-12t-4-13z" transform="matrix(1 0 0 -1 0 850)"></path></svg></a>

</div>

<div class="modebar-group" markdown="1">

<a href="https://plotly.com/" target="_blank" data-title="Produced with Plotly.js (v3.0.1)" class="modebar-btn plotlyjsicon modebar-btn--logo" data-btn-style-event-added="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 132 132" height="1em" width="1em"> <title>plotly-logomark</title> <g id="symbol"> <rect fill="#000" x="0" y="0" width="132" height="132" rx="18" ry="18"></rect> <circle fill="#9EF" cx="102" cy="30" r="6"></circle> <circle fill="#BAC" cx="78" cy="30" r="6"></circle> <circle fill="#BAC" cx="78" cy="54" r="6"></circle> <circle fill="#D69" cx="54" cy="30" r="6"></circle> <circle fill="#F26" cx="30" cy="30" r="6"></circle> <circle fill="#F26" cx="30" cy="54" r="6"></circle> <path fill="#FFF" d="M30,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,30,72Z"></path> <path fill="#FFF" d="M78,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,78,72Z"></path> <path fill="#FFF" d="M54,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,54,48Z"></path> <path fill="#FFF" d="M102,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,102,48Z"></path> </g></svg></a>

</div>

</div>

</div>

<svg class="main-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="900" height="700"><g class="hoverlayer"></g></svg>

</div>

</div>

</div>

</div>

همان طور که در بالا مشاهده می‌کنید کلمات بالا و چپ مربوط به آب و کلمات پایین و چپ مربوط به جنگل و حیوان است. و کلمه شیر که بین هر دو مشترک است با توجه به جمله در این فضا حرکت کرده و موقعیت‌های متفاوت گرفته.

## حافظه و توجه به کدام کلمات؟

همان طور که اشاره شد در مدل‌های زبانی کلمات به کمک معماری که مثل حافظه امکان توجه به توکن‌های گذشته را به مدل می‌داد مدل زبانی می‌توانست با توجه به کلمات گفته شده در گذشته تک کلمه جدید را کشف کند ولی اگر کلمات ابتدایی یک جمله وابسطه به کلمات بعدی همان جمله یا جملات بعد باشد محاسبه آینده دور قبل از شروع این جمله برای مدل‌های زبانی چالش بود. در مدل BERT با توجه کردن به کلمات گذشته (اصطلاحا سمت چپ) و کلمات آینده (اصطلاحا سمت راست) جملات را راحت تر و معنی دار تر می‌نوشت.

## BERT مخفف چیست؟

کلمه BERT مخفف عبارت Bidirectional Encoder Representations from Transformers‌

است. همبن طور که در عنوان مشخص است در این مقاله رمز گذاری که قرار هست اتفاق بیوفتد و توکن ما را به فضای embeding خاص خودش ببرد، دو جهته است. قبل از مدل BERT تمام مدل‌های زبان این مشکل را داشتند. یا تک جهته بودند یا نهایتا از دو سمت جداگانه متن رو بررسی می‌کردند و بعد تحلیل‌های دو جهت را به هم وصل می‌کردند ولی به طور هم زمان هیچ مدلی به کلمات سمت راست و چپ کلمه‌ای که می‌خواست پیش بینی شود توجه نمی‌کرد. در مدل BERT دو مرحله ایجاد کردن. مرحله اول به عنوان پیش آموزش (pre treaning) به شکل عمومی برای تمام وظیفه‌های مختلف NLP مدل به صورت «بدون نظارت» (unsupervised learning) آموزش می‌بینیه بعد برای وظایف تخصصی مثل پرسش و پاسخ، انتخاب این که چه گزینه‌ای از ۴ گزینه جمله ادامه مطلب هست، دسته بندی مطالب و … «تنظیم دقیق» (fine tune) می‌شه. از مزایای این عمل fine tune می‌شه گفت که هم خیلی سریع می‌تونه انجام بشه و هم به منابع سخت افزاری کم تر نیاز داره و هم به نسبت تنظیم یک مدل از پایه به داده‌های کم تری نیاز داره. این طور می‌شه بیان کرد که آموزش از ابتدا مثل اینه که یک انسان رو از نوزادی تا اون وظیفه خاص تربیت کنیم ولی fine tune مثل اینه که یک کسی که یک سری دانش‌های عمومی داره رو استخدام کنیم و با مقدار کمی آموزش تخصصی اون نیرویی که نیاز داریم رو تربیت کنیم.

### پیش آموزش pre treaning

این عملیات شامل دو وظیفه، مدل زبانی ماسک شده (masked language model) و پیش بینی عبارت بعدی (Next Sentence Prediction) بود. برای این کار نیاز است از منابع مختلف مثل wikipedia و … کمک گرفت و هر سند به شکل به هم پیوسته در یک فایل txt قرار بگیرد و بین اسناد یک خط فاصله باشد.

#### مدل زبانی ماسک شده (Masked Language Model - MLM)

در این روش هدف این است که مدل بتواند مفهوم و ارتباط بین کلمات جمله را درک کند، نه این‌که صرفاً ترتیب آن‌ها را حفظ کند. برای این کار، درصدی از کلمات جمله به طور تصادفی با نماد خاصی به نام \[MASK\] جایگزین می‌شوند.  
برای مثال جمله «من امروز به مدرسه رفتم» را در نظر بگیر. اگر کلمه «مدرسه» را پنهان کنیم، مدل باید با توجه به بقیه جمله حدس بزند که در جای خالی چه کلمه‌ای باید باشد. یعنی جمله به شکل «من امروز به \[MASK\] رفتم» در ورودی مدل قرار می‌گیرد و مدل با استفاده از فهمش از ساختار و معنای زبان، کلمه‌ی گم‌شده را پیش‌بینی می‌کند.

این تمرین باعث می‌شود مدل نه‌تنها معنی هر کلمه را به تنهایی درک کند، بلکه بفهمد هر کلمه چگونه با کلمات قبل و بعد از خودش ارتباط دارد. نکته جذاب‌تر این است که BERT جمله را از هر دو جهت می‌بیند — از راست و از چپ — بنابراین در پیش‌بینی‌اش از تمام اطلاعات جمله بهره می‌گیرد.  
این بخش شبیه تمرین پر کردن جای خالی در زبان‌آموزی است؛ با این تفاوت که برای مقیاس میلیاردها جمله انجام می‌شود. حاصل این مرحله، مدلی است که می‌تواند درک عمیقی از معنای زبان داشته باشد و پایه اصلی قدرت BERT نیز همین یادگیری دوطرفه از طریق MLM است.

---

#### پیش‌بینی عبارت بعدی (Next Sentence Prediction - NSP)

در کنار یادگیری معنی در سطح کلمه، مدل باید بتواند درک کند دو جمله پشت سر هم با هم ارتباط معنایی دارند یا نه.  
برای این آموزش، به مدل جفت‌جملاتی داده می‌شود. در نیمی از موارد جمله دوم واقعاً ادامه جمله اول است، و در نیمی دیگر جمله‌ای تصادفی از متن دیگر جای آن گذاشته می‌شود. مدل باید تشخیص دهد که آیا جمله دوم در ادامه جمله اول آمده یا خیر.

برای مثال:

- جمله ۱: «امروز هوا بارانی بود.»
- جمله ۲: «من چترم را با خودم برداشتم.» → این دو جمله به هم مربوط‌اند.  
  اما اگر جمله دوم را جایگزین کنیم با:
- جمله ۲: «کتابخانه تا ساعت ۸ باز است.» → این دو جمله به هم نامرتبط هستند.

با تمرین روی میلیون‌ها جفت جمله، مدل یاد می‌گیرد که پیوند منطقی بین جملات را بشناسد. همین توانایی است که بعداً در وظایفی مثل پاسخ به سؤال، خلاصه‌سازی متن یا تشخیص تداوم گفتگو به کار می‌آید.

به زبان ساده، در حالی که بخش MLM به مدل یاد می‌دهد «کلمه‌ی مناسب جمله چیست»، بخش NSP به آن می‌آموزد «جمله‌ی بعدی مرتبط کدام است».

یک نمونه از ورودی‌های مدل هنگام تمرین دیدن برای عملیات پیش پردازش به شکل زیر است:

<p dir="rtl">
<span>[CLS]</span> در | سال | ۱۳۹۹ | پژوهشگران | دانشگاه | <span>تهران</span> | <span>مدل</span> | جدیدی | از | پردازش | <span>زبان</span> | طبیعی | معرفی | کردند | .  
این | مدل | بر | پایه | معماری | [MASK] | طراحی | شده | و | توانست | در | وظایف | مختلف | مانند | طبقه‌بندی | متن | و | تحلیل | احساسات | عملکرد | چشمگیری | نشان | دهد | .  
هدف | اصلی | آن | بهبود | [MASK] | مدل‌های | زبانی | در | متون | فارسی | بود | .  
<span>[SEP]</span>  
در | مرحله | دوم | پژوهش | ، | تیم | توسعه | تصمیم | گرفت | مدل | را | بر | روی | پیکره‌ای | بزرگ‌تر | شامل | داده‌های | خبری | و | گفت‌وگویی | [MASK] | دهد | .  
نتایج | اولیه | نشان | داد | که | دقت | مدل | در | تشخیص | نیت | کاربران | حدود | [MASK] | درصد | افزایش | یافته | است | .  
با | این | حال | برخی | خطاها | هنوز | در | واژه‌های | [MASK] | و | ترکیبات | [MASK] | باقی | مانده | بود | .  
برای | رفع | این | مشکل | ، | پژوهشگران | از | روش | یادگیری | انتقالی | و | بهینه‌سازی | [MASK] | استفاده | کردند | تا | عملکرد | مدل | در | داده‌های | واقعی | بهتر | شود | .  
همچنین | در | فاز | نهایی | ، | از | الگوریتم | [MASK] | برای | کاهش | [MASK] | حافظه | و | افزایش | سرعت | آموزش | بهره | گرفته | شد | .  
این | رویکرد | سبب | شد | تا | <span>کتاب</span> | نسبت | به | <span>داده</span> | خود | سریع‌تر | و | <span>نرم‌افزار</span> | عمل | کند | .  
<span>[SEP]</span>
</p>

سه توکن قرمز (کتاب, داده, نرم‌افزار) همان‌هایی هستند که اشتباه جایگزین شده‌اند.

سه توکن سبز (تهران, مدل, زبان) همان‌هایی‌اند که بدون تغییر باقی مانده‌اند.

همین طور هم که می‌بینین دنباله‌هایی که با توکن [SEP] از هم جدا شدند دو دنباله پشت سر هم بودند و مدل در ازای این پشت سر هم بودن باید بعد از تحلیل توکن [CLS] باید `IsNext` را پیش بینی کند.

#### اتمام مرحله پیش‌آموزش و ورود به تنظیم دقیق (Fine-tuning)

پس از اینکه مدل در مرحله پیش‌آموزش (Pre-training) یاد گرفت چگونه کلمات را درک کند و چطور ارتباط بین جمله‌ها را تشخیص دهد، نوبت به مرحله تنظیم دقیق یا همان Fine-tuning می‌رسد. در این مرحله مدل دیگر از صفر شروع نمی‌کند، بلکه دانشی کلی از ساختار زبان به‌دست آورده و آماده است تا با داده‌های خاص‌تر برای یک وظیفه مشخص آموزش ببیند.

برای نمونه، اگر بخواهیم از BERT برای پاسخ به سؤالات (Question Answering) استفاده کنیم، تنها کافی است آن را با مجموعه‌ای از نمونه سؤال و پاسخ‌ها دوباره آموزش دهیم تا توانایی‌اش در این نوع کار تقویت شود. یا اگر هدف ما دسته‌بندی احساسی جملات باشد (مثلاً تشخیص مثبت یا منفی بودن نظر کاربران)، کافی است داده‌هایی شامل جملات و برچسب احساساتشان را در اختیار مدل بگذاریم تا یاد بگیرد از معنای جمله، حالت عاطفی آن را تشخیص دهد.

BERT به دلیل همین ساختار دوه‌مرحله‌ای خود — یعنی یادگیری عمومی در مرحله Pre-training و یادگیری خاص در مرحله Fine-tuning — می‌تواند در وظایف مختلف زبانی با داده‌های اندک عملکردی بسیار قوی داشته باشد. همین ویژگی باعث شد که BERT نقطه عطفی در تاریخ مدل‌های زبانی و مبنایی برای ده‌ها مدل جدید مانند RoBERTa، ALBERT، DistilBERT و غیره شود.

در واقع می‌توان گفت مدل‌های زبانی قبل از BERT مثل شاگردانی بودند که فقط از روی مثال یاد می‌گرفتند، اما BERT شاگردی است که زبان را «می‌فهمد» و بعد از آن می‌تواند در هر زمینه‌ای تخصص پیدا کند — از ترجمه گرفته تا تحلیل احساسات یا درک سؤالات.

## 📦 نصب و اجرا

کدهای اجرا و تمرین دادن مدل BERT‌ در GitHub قرار دارد ولی دیگه به حالت بایگانی در اومدن و پشتیبانی نمی‌شن اما با همین معماری توسط کتابخانه‌های pytorch و HuggingFace دوباره پیاده سازی شدن. در این بخش طبق این راهنما می‌توانید پیاده سازی مدل پیش پردازش و مصور سازی embeding را انجام دهید.

## ⚙️ پیش‌نیازها

### ✅ نسخه‌ی پیشنهادی پایتون

این پروژه در محیط **Python 3.12.3** تست و توسعه داده شده است.  
نسخه‌های بالاتر (به‌ویژه **3.13** و **3.14**) ممکن است با برخی پکیج‌ها مانند `torch` یا `transformers` ناسازگار باشند (به‌خصوص در هنگام نصب با pip).

> ⚠️ **توصیه:**  
> اگر از نسخه‌های جدیدتر استفاده می‌کنید و با خطای نصب مواجه شدید، یکی از دو روش زیر را انجام دهید:

**روش ۱️⃣: استفاده از نسخه‌ی پیشنهادی پایتون (پیشنهادی‌ترین گزینه)**  
در لینوکس یا مک:

```bash
pyenv install 3.12.3
pyenv local 3.12.3
```

در ویندوز می‌توانید از python.org نسخه‌ی 3.12.3 را دانلود کنید.

**روش ۲️⃣: رفع ناسازگاری در نسخه‌های بالاتر**
اگر پایتون شما 3.13 یا 3.14 است، قبل از نصب بسته‌ها دستور زیر را اجرا کنید تا نسخه‌ی سازگار PyTorch نصب شود:

```bash
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
pip install transformers==4.46.1
```

در صورت وجود GPU از آدرس پکیج‌های PyTorch نسخه‌ی مناسب CUDA را انتخاب کنید.

---

### 1️⃣ دریافت ریپازیتوری

```bash
git clone https://github.com/mohammadsaleh40/bert_hf.git
cd bert_hf
```

2️⃣ ایجاد محیط مجازی و نصب وابستگی‌ها

```bash
python3 -m venv venv
source venv/bin/activate       # در ویندوز: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

⚙️ آماده‌سازی داده‌ها
الف) دریافت داده‌ی نمونه MirasText

```bash
wget https://raw.githubusercontent.com/miras-tech/MirasText/refs/heads/master/MirasText/MirasText_sample.txt -O MirasText_sample.txt
```

ب) پیش‌پردازش داده‌ها

```bash
python prepare_mirastext.py
```

📄 خروجی: `mirastext_preprocessed.txt`

---

ج) افزودن Wikipedia فارسی

1. دانلود فایل فشرده ویکی‌پدیا فارسی:

```bash
wget https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2
```

2. استخراج محتوای متنی با WikiExtractor:

```bash
python -m wikiextractor.WikiExtractor fawiki-latest-pages-articles.xml.bz2 -o fawiki-latest-pages-articles
```

3. اضافه کردن مقالات ویکی‌پدیا به انتهای داده‌ی MirasText:

```bash
python add_wiki_to_preprocessed.py
```

## 📄 خروجی نهایی: `mirastext_preprocessed.txt` شامل MirasText + Wikipedia فارسی

🧰 ساخت واژگان (اختیاری)

در صورت تمایل می‌توانید واژگان جدید بسازید:

```bash
python create_vocab.py
```

فایل تولیدی نامش باید به `vocab.txt` تغییر پیدا کند. با دستور زیر آن را تغییر می‌دهیم.

```bash
mv persian_bert_tokenizer/wp-vocab.txt persian_bert_tokenizer/vocab.txt
```

---

🚀 آموزش مدل BERT فارسی

فایل run_pretraining_hf_v2.py مسئول اجرای آموزش مدل بر پایه‌ی HuggingFace Trainer است.
پارامترهای اصلی درون فایل تعریف شده‌اند (مثل اندازه‌ی مدل، توکنایزر، مسیر داده‌ها و غیره).

```bash
python run_pretraining_hf_v2.py
```

📂 خروجی مدل ذخیره می‌شود در مسیر:

```bash
persian_bert_tiny_output_large_2/
```

🔍 بررسی و تست مدل

برای آزمایش مدل آموزش‌دیده، دو روش در دسترس است:

🔹 روش ۱: اجرای مستقیم اسکریپت

```bash
python check_model.py
```

## این فایل چند جمله‌ی فارسی را پردازش کرده و با استفاده از t-SNE توزیع بردارهای کلمات را نمایش می‌دهد.

🔹 روش ۲: استفاده از نوت‌بوک

فایل chek_model.ipynb را با Jupyter باز کنید:

```bash
jupyter notebook chek_model.ipynb
```

در این نوت‌بوک:

مدل از مسیر `persian_bert_tiny_final_model_large_2` بارگذاری می‌شود.

چند جمله‌ی فارسی نمونه به مدل داده می‌شود.

و خروجی‌ها (embedding و شباهت‌ها) بررسی می‌شوند.

## نسخه‌های از پیش تمرین داده شده

در <a href="https://github.com/hooshvare/parsbert" target="_blank"> این لینک </a> می‌تونین با پروژه <a href="https://link.springer.com/article/10.1007/s11063-021-10528-4" target="_blank"> parsBERT </a> آشنا بشین. نسخه‌های مختلفی از bert روی دیتاست‌های بزرگی از زبان فارسی تمرین داده شده که می‌تونین از اون‌ها استفاده کنین.

### کامل کردن کلمه گم شده

مثلا در <a href="https://huggingface.co/HooshvareLab/bert-fa-zwnj-base?maximized=true&amp;text=%D8%B2%D9%86%D8%AF%DA%AF%DB%8C+%DB%8C%DA%A9+%D8%B3%D9%88%D8%A7%D9%84+%D8%A7%D8%B3%D8%AA+%D9%88+%D8%A7%DB%8C%D9%86+%DA%A9%D9%87+%DA%86%DA%AF%D9%88%D9%86%D9%87+%5BMASK%5D+%DA%A9%D9%86%DB%8C%D9%85+%D9%BE%D8%A7%D8%B3%D8%AE+%D8%A7%DB%8C%D9%86+%D8%B3%D9%88%D8%A7%D9%84%21" target="_blank"> این لینک </a> می‌تونین جملاتی دارای توکن \[MASK\] به مدل بدین و خروجی به شما می‌گه چه کلماتی احتمال دارد به جای کلمه گم شده قرار گیرند.

## مقاله ترجمه شده

در صورت علاقه به خواندن اصل مقاله BERT در <a href="https://aclanthology.org/N19-1423/" target="_blank">این لینک</a> نسخه ترجمه فارسی اون قرار داره که به کمک ChatGPT ترجمه شده.

## منابع

1. <a href="https://arxiv.org/abs/1810.04805" target="_blank"><strong>BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding</strong></a>
2. <a href="https://github.com/hooshvare/parsbert" target="_blank"><strong>ParsBERT</strong></a>
3. <a href="https://en.wikipedia.org/wiki/Cortana_/(virtual_assistant/" target="_blank"><strong>Cortana</strong></a>
4. <a href="https://medium.com/@atharv6f_47401/wordpiece-tokenization-a-bpe-variant-73cc48865cbf" target="_blank"><strong>WordPiece Tokenization: A BPE Variant</strong></a>
5. <a href="https://arxiv.org/abs/1706.03762" target="_blank"><strong>Attention Is All You Need</strong></a>
   <!--bundle exec jekyll serve --host 0.0.0.0 --port 8085-->
   {% endraw %}
