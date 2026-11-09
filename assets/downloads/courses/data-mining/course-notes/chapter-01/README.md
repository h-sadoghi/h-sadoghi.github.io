# اجرای نمونهٔ فصل اول داده‌کاوی

فایل `transactions.csv` ده تراکنش **ساختگی** دارد. برنامهٔ `chapter01_example.py` فقط به پایتون استاندارد (نسخهٔ 3.10 به بالا) نیاز دارد و بدون اینترنت اجرا می‌شود:

```bash
python chapter01_example.py
```

برای اجرای دفترچهٔ Jupyter، محیط دارای `numpy`، `pandas`، `matplotlib`، `jupyter` لازم است:

```bash
python -m pip install -r requirements.txt
jupyter notebook chapter01_example.ipynb
```

کدها و داده‌ها در یک پوشه قرار دارند؛ در اجرا هیچ فایل خارجی دانلود نمی‌شود. خروجی‌های عددی همان نمونهٔ ده‌تراکنشی‌اند و هیچ تعمیم آماری به جمعیت واقعی ندارند.
