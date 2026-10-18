---
layout: legacy_page
title: PULP
permalink: /resources/teaching-toolkit-pulp/
description: Archived teaching material
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/toolkit/PULP/
legacy_group: Research toolkit
legacy_dir: rtl
lang: fa
---

{% raw %}

# چطور با PuLP کار کنیم

## آشنایی با مسأله

مسألهٔ تخصیص کارها به تیم‌ها در ۵ روز

از یک مثال کوچک استفاده می‌کنیم. در ابتدا با این ساختار آشنا شو:

### مثالِ ساده

```python
tasks = {
    "T1": {"hours": 4},
    "T2": {"hours": 3},
    "T3": {"hours": 6},
}

teams = {
    "TeamA": {"daily_capacity": 8, "can_do": ["T1","T2","T3"]},
    "TeamB": {"daily_capacity": 6, "can_do": ["T1","T3"]},
}

days = ["0","1","2","3","4"]
```

- سه کار (T1, T2, T3) داریم با ساعت‌های مورد نیاز
- دو تیم با ظرفیت روزانه مشخص
- ۵ روز کاری داریم

## گام ۲ — تعریف متغیرهای تصمیم در PuLP

کدام تیم، در کدام روز، کدام کار را انجام دهد.

در مدل‌های تخصیص (assignment)، معمولاً از متغیر دودویی (binary) استفاده می‌کنیم:

- اگر تیم i در روز d کار t را انجام دهد → مقدار 1
- در غیر این صورت → مقدار 0

```python
import pulp

# داده‌ها از گام قبل
tasks = ["T1", "T2", "T3"]
teams = ["TeamA", "TeamB"]
days = ["0","1","2","3","4"]

# مدل اصلی
model = pulp.LpProblem("Task_Assignment", pulp.LpMaximize)  # بعداً تابع هدف را می‌گذاریم

# متغیر دودویی x[team][day][task]
x = pulp.LpVariable.dicts(
    "assign",
    ((team, day, task) for team in teams for day in days for task in tasks),
    cat="Binary"
)
```

### توضیح متغیرها:

- `x[("TeamA","Mon","T1")] = 1` یعنی تیم A در دوشنبه کار T1 را انجام می‌دهد
- `x[("TeamB","Wed","T3")] = 0` یعنی انجام نمی‌دهد

`pulp.LpVariable.dicts` یک دیکشنری از متغیرها می‌سازد که کلیدهایش همان `(team,day,task)` هستند.

دسته‌ی `"Binary"` باعث می‌شود فقط 0 یا 1 مجاز باشند.

# چطور با PuLP کار کنیم

## گام ۳ — تعریف تابع هدف (Objective Function)

به مدل باید بگوییم که می‌خواهد چه چیزی را بهینه کند.

در مسائل تخصیص، معمولاً یکی از هدف‌های زیر داریم:

- کمینه کردن مجموع هزینه‌ها یا زمان‌ها
- متعادل کردن حجم کار بین تیم‌ها
- حداکثر کردن تعداد کارهای انجام‌شده

برای شروع، ساده‌ترین حالت را یاد می‌گیریم:
👉 **«می‌خواهیم مجموع کل کارهای انجام‌شده را حداکثر کنیم.»**

```python
# تابع هدف: بیشینه کردن مجموع کارهای انجام‌شده
model += pulp.lpSum(x[(team, day, task)] for team in teams for day in days for task in tasks)
```

### توضیح:

- `lpSum` تابع جمع در PuLP است
- چون x فقط ۰ یا ۱ است، جمع آن یعنی چند کار در کل انجام شده است
- `model += ...` یعنی این عبارت تابع هدف مدل است

## گام ۴: نوشتن قیدهای اصلی تخصیص و ظرفیت تیم‌ها

### 🧩 قید ۱: هر کار فقط یک‌بار در کل هفته انجام شود

یعنی هر کار نباید توسط چند تیم در چند روز تکرار شود.

```python
for task in tasks:
    model += pulp.lpSum(x[(team, day, task)] for team in teams for day in days) <= 1, f"EachTaskOnce_{task}"
```

**🔹 توضیح:**
جمع تمام متغیرهایی که نشان‌دهندهٔ انجام یک کار هستند، باید حداکثر ۱ باشد.
(می‌توانی `== 1` بگذاری اگر مطمئنی همهٔ کارها باید حتماً انجام شوند.)

### ⚙️ قید ۲: ظرفیت روزانهٔ هر تیم رعایت شود

فرض کنیم هر کار t تعداد ساعت نیاز دارد (`tasks[t]["hours"]`)،
و هر تیم در هر روز حداکثر `teams[team]["daily_capacity"]` ساعت وقت دارد.

```python
for team in teams:
    for day in days:
        model += pulp.lpSum(
            tasks[task]["hours"] * x[(team, day, task)] for task in tasks
        ) <= teams[team]["daily_capacity"], f"Capacity_{team}_{day}"
```

**توضیح:**
برای هر تیم و هر روز، مجموع ساعات کارهایی که به او اختصاص داده می‌شود، نباید از ظرفیتش بیشتر شود.

### کد کامل تا این مرحله:

```python
import pulp

# داده‌ها
tasks = {
    "T1": {"hours": 4},
    "T2": {"hours": 6},
    "T3": {"hours": 3}
}

teams = {
    "TeamA": {"daily_capacity": 8},
    "TeamB": {"daily_capacity": 6}
}

days = ["0", "1", "2", "3", "4"]

# مدل اصلی
model = pulp.LpProblem("Task_Assignment", pulp.LpMaximize)

# متغیر دودویی x[team][day][task]
x = pulp.LpVariable.dicts(
    "assign",
    ((team, day, task) for team in teams for day in days for task in tasks),
    cat="Binary"
)

# تابع هدف: بیشینه کردن مجموع کارهای انجام‌شده
model += pulp.lpSum(x[(team, day, task)] for team in teams for day in days for task in tasks)

# قید ۱: هر کار فقط یک‌بار انجام شود
for task in tasks:
    model += pulp.lpSum(x[(team, day, task)] for team in teams for day in days) <= 1, f"EachTaskOnce_{task}"

# قید ۲: ظرفیت روزانه تیم‌ها
for team in teams:
    for day in days:
        model += pulp.lpSum(tasks[task]["hours"] * x[(team, day, task)] for task in tasks) <= teams[team]["daily_capacity"], f"Capacity_{team}_{day}"

print("مدل با موفقیت ساخته شد!")
```

## گام ۵ — حل مدل و نمایش نتایج

### ۱. حل مدل

در PuLP فقط کافی است بنویسی:

```python
model.solve()
```

اما بهتر است وضعیت حل را هم چاپ کنیم:

```python
status = pulp.LpStatus[model.status]
print("وضعیت حل:", status)
```

### ۲. استخراج و چاپ نتایج

حالا باید ببینیم کدام متغیر مقدار 1 گرفته (یعنی تخصیص انجام شده است):

```python
print("\nنتایج تخصیص:")
for team in teams:
    for day in days:
        for task in tasks:
            if pulp.value(x[(team, day, task)]) == 1:
                print(f"✅ {task} ← {team} در روز {day}")
```

### ۳. کل خروجی مدل

اگر می‌خواهی کل مدل و مقادیر هدف را هم ببینی:

```python
print("\nمقدار تابع هدف:", pulp.value(model.objective))
```

## آزمایش دوم

الان می‌خواهیم مدل را به حالت واقعی و بزرگ‌تر گسترش دهیم —
یعنی:

تعداد کارها زیاد است (مثلاً 30 تا)

فقط 3 تیم داریم

هر کار زمان اجرای خودش را دارد

هر تیم در هر روز فقط تا ظرفیت مشخص می‌تواند کار کند

مدل باید بیشترین تعداد کار ممکن در طول ۵ روز هفته را انتخاب و تخصیص دهد

```python
import pulp
import random

# -----------------------------
# 1. داده‌ها (Tasks, Teams, Days)
# -----------------------------
num_tasks = 30  # تعداد کارها (می‌توانی زیادتر هم کنی)
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# هر کار ساعت کاری تصادفی بین 1 تا 6 ساعت دارد
tasks = {f"T{i+1}": {"hours": random.randint(1, 6)} for i in range(num_tasks)}

teams = {
    "TeamA": {"daily_capacity": 8},
    "TeamB": {"daily_capacity": 6},
    "TeamC": {"daily_capacity": 7},
}

# -----------------------------
# 2. تعریف مدل
# -----------------------------
model = pulp.LpProblem("Large_Task_Assignment", pulp.LpMaximize)

# متغیر دودویی x[team, day, task] = 1 اگر تیم در آن روز آن کار را انجام دهد
x = pulp.LpVariable.dicts(
    "assign",
    ((team, day, task) for team in teams for day in days for task in tasks),
    cat="Binary"
)

# -----------------------------
# 3. تابع هدف: بیشینه‌سازی تعداد کل کارهای انجام‌شده
# -----------------------------
model += pulp.lpSum(x[(team, day, task)] for team in teams for day in days for task in tasks), "Maximize_Total_Tasks"

# -----------------------------
# 4. قید ۱: هر کار فقط یک‌بار در کل هفته انجام شود
# -----------------------------
for task in tasks:
    model += pulp.lpSum(x[(team, day, task)] for team in teams for day in days) <= 1, f"EachTaskOnce_{task}"

# -----------------------------
# 5. قید ۲: ظرفیت روزانهٔ هر تیم رعایت شود
# -----------------------------
for team in teams:
    for day in days:
        model += pulp.lpSum(tasks[task]["hours"] * x[(team, day, task)] for task in tasks) <= teams[team]["daily_capacity"], f"Capacity_{team}_{day}"

# -----------------------------
# 6. حل مدل
# -----------------------------
print("در حال حل مدل ...")
model.solve(pulp.PULP_CBC_CMD(msg=False))

status = pulp.LpStatus[model.status]
print("وضعیت حل:", status)
print("مقدار تابع هدف (تعداد کارهای انجام‌شده):", pulp.value(model.objective))

# -----------------------------
# 7. نمایش نتایج تخصیص
# -----------------------------
assignments = []
for team in teams:
    for day in days:
        day_tasks = [task for task in tasks if pulp.value(x[(team, day, task)]) == 1]
        if day_tasks:
            total_hours = sum(tasks[t]["hours"] for t in day_tasks)
            assignments.append((team, day, day_tasks, total_hours))

# مرتب‌سازی خروجی برای زیبایی
assignments.sort(key=lambda a: (a[0], a[1]))

print("\nنتایج تخصیص:")
for team, day, day_tasks, total_hours in assignments:
    print(f"{team} در {day}: {day_tasks} (جمع ساعت = {total_hours})")

# -----------------------------
# 8. تعداد کارهای انجام‌نشده
# -----------------------------
done_tasks = {t for (_, _, tasks_list, _) in assignments for t in tasks_list}
not_done = [t for t in tasks if t not in done_tasks]
print(f"\nتعداد کارهای انجام‌شده: {len(done_tasks)} از {len(tasks)}")
print("کارهای انجام‌نشده:", not_done)
```

در حال حل مدل ...
وضعیت حل: Optimal
مقدار تابع هدف (تعداد کارهای انجام‌شده): 29.0

نتایج تخصیص:
TeamA در Fri: ['T6', 'T15'] (جمع ساعت = 8)
TeamA در Mon: ['T17', 'T23'] (جمع ساعت = 8)
TeamA در Thu: ['T5', 'T14'] (جمع ساعت = 8)
TeamA در Tue: ['T10', 'T29'] (جمع ساعت = 8)
TeamA در Wed: ['T26', 'T28'] (جمع ساعت = 8)
TeamB در Fri: ['T4', 'T25'] (جمع ساعت = 5)
TeamB در Mon: ['T30'] (جمع ساعت = 6)
TeamB در Thu: ['T8'] (جمع ساعت = 6)
TeamB در Tue: ['T13', 'T16'] (جمع ساعت = 6)
TeamB در Wed: ['T20', 'T22', 'T27'] (جمع ساعت = 6)
TeamC در Fri: ['T1', 'T11'] (جمع ساعت = 7)
TeamC در Mon: ['T2', 'T7'] (جمع ساعت = 7)
TeamC در Thu: ['T3', 'T9'] (جمع ساعت = 7)
TeamC در Tue: ['T12', 'T21'] (جمع ساعت = 7)
TeamC در Wed: ['T19', 'T24'] (جمع ساعت = 7)

تعداد کارهای انجام‌شده: 29 از 30
کارهای انجام‌نشده: ['T18']
{% endraw %}
