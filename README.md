# بازار لینکَر — Django

راهنمای محلی فروشگاه‌ها و آگهی‌های کسب‌وکارهای محلی با Django. این پروژه برای معرفی فروشگاه و محصول و ارتباط مستقیم با فروشنده ساخته شده است؛ سبد خرید و درگاه پرداخت آنلاین ندارد.

## اجرای محلی در ویندوز

1. Python 3.11 تا 3.13 را نصب کن و گزینه Add Python to PATH را فعال کن.
2. ZIP را استخراج کن و CMD را در همین پوشه، جایی که `manage.py` قرار دارد، باز کن.
3. دستورات زیر را اجرا کن:

```bat
py -3.13 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
set DJANGO_DEBUG=1
set DJANGO_SECRET_KEY=django-insecure-local-development-only-change-before-deployment
set DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
python manage.py migrate
python manage.py seed_bazaar
python manage.py createsuperuser
python manage.py runserver
```

سایت در `http://127.0.0.1:8000/` باز می‌شود. پنل مدیریت سایت: `/manage/` و پنل Django: `/django-admin/`. اگر محیط مجازی از قبل داری، مراحل ساخت `.venv` را رد کن.

## انتقال به GitHub و Render

این مخزن دارای `render.yaml` است. پس از push کردن پروژه به GitHub، در داشبورد Render از **New → Blueprint** مخزن را انتخاب کن و Blueprint را Apply کن. Render بر اساس `render.yaml` یک وب‌سرویس و PostgreSQL ایجاد می‌کند. Build script خودش نصب بسته‌ها، اجرای migrationها، ساخت تنظیمات اولیه و جمع‌آوری static files را انجام می‌دهد.

در Environment سرویس Render این سه مقدار را تنظیم کن تا مدیر اولیه به‌طور خودکار ساخته شود:

- `DJANGO_SUPERUSER_USERNAME`: نام کاربری دلخواه مدیر
- `DJANGO_SUPERUSER_EMAIL`: ایمیل مدیر
- `DJANGO_SUPERUSER_PASSWORD`: رمز عبور قوی و منحصربه‌فرد

این مقادیر را فقط در تنظیمات خصوصی Environment در Render وارد کن؛ هرگز در GitHub یا داخل کد ننویس. دستور ساخت مدیر فقط وقتی حساب با آن نام وجود نداشته باشد حساب جدید می‌سازد و در Deployهای بعدی رمز حساب موجود را تغییر نمی‌دهد.

## Git از Windows CMD

از پوشه پروژه، در صورتی که مخزن Git هنوز ساخته نشده، اجرا کن (آدرس را با مخزن خودت عوض کن):

```bat
git init
git add .
git status
git commit -m "Prepare Bazaar Linker for Render"
git branch -M main
git remote add origin https://github.com/USERNAME/bazaar-django.git
git push -u origin main
```

اگر `remote origin already exists` دیدی، دستور `git remote set-url origin https://github.com/USERNAME/bazaar-django.git` را جایگزین دستور `git remote add origin ...` کن. اگر `src refspec main does not match any` دیدی، اول مطمئن شو دستور `git commit` موفق شده است.

## متغیرهای محیطی و امنیت

- کلید `DJANGO_SECRET_KEY` در Render به‌طور خودکار تولید می‌شود.
- `DJANGO_DEBUG=0` برای سرویس عمومی خاموش می‌ماند.
- `DJANGO_ALLOWED_HOSTS=.onrender.com` دامنه عمومی Render را مجاز می‌کند.
- اتصال دیتابیس از `DATABASE_URL` خوانده می‌شود؛ اگر این متغیر در محیط محلی تنظیم نشده باشد، پروژه از SQLite محلی استفاده می‌کند.
- فایل `.env`، دیتابیس SQLite، تصاویر آپلودی و رسیدهای خصوصی در `.gitignore` قرار دارند و نباید در GitHub قرار بگیرند.

## محدودیت‌های پلن رایگان Render

سرویس رایگان پس از ۱۵ دقیقه بی‌درخواست به حالت خواب می‌رود و درخواست بعدی ممکن است حدود یک دقیقه طول بکشد. دیسک وب‌سرویس رایگان ماندگار نیست؛ فایل‌های تصویری/رسیدهای آپلودشده ممکن است با restart یا deploy از بین بروند. PostgreSQL رایگان Render نیز پس از ۳۰ روز منقضی می‌شود. این تنظیمات برای دموی آزمایشی مناسب است، نه نگهداری بلندمدت داده‌های واقعی.

## فونت فارسی

از فونت وزیرمتن استفاده شده و stylesheet آن از CDN رسمی پروژه بارگذاری می‌شود. اگر CDN در دسترس نباشد، مرورگر از فونت‌های جایگزین `Tahoma` یا `Arial` استفاده می‌کند. منبع و مجوز فونت: https://github.com/rastikerdar/vazirmatn (SIL Open Font License).
