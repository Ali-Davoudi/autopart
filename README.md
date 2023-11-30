# Autopart. This is a project that I develop in my spare time and I usually implement everything I learn in this project.
### Usage
- Geting the project source
```
git clone https://github.com/ali-davoudi/autopart
```
- At the main project directory(~\autopart), create ``` .env ``` file and based on ``` .env-example ``` fill the informations.

- Install virtualenv globally on your  ```Ubuntu-Debian``` distribution or anything else(It requires its own installation principles)
```
sudo apt install python3-virtualenv
```
- Then you need to create a ```venv``` for your project. at ~\autopart open the terminal and follow these commands:
```
python3 -m virtualenv venv
```
```
source venv\bin\activate
```
- Install requirements
```
pip install -r requirements.txt
```
- Follow these commands:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py runserver
```

- If you want be a superuser, going to admin, directley working with features and etc
```
python manage.py createsuperuser
```

### Some features [fa]
- سیستم احراز هویت از طریق خود وب سایت و اکانت گوگل
- احراز هویت: ورود، خروج، ثبت نام، مرا به خاطر بسپار، ارسال کد فعال سازی ایمیل به کاربر برای ثبت نام، Token Authentication، فراموشی رمز عبور، بازیابی رمز عبور
- گوگل ریکپتچا
- از بین رفتن خودکار اطلاعات سبد خرید کاربر در صورت باز بودن و عدم پرداخت در مدت زمان معین (در صورت تغییر مدت زمان، از مسیر autopart\apps\basket_order\signals.py اقدام نمایید. بطور تستی 30 ثانیه قرار داده شده که قابل رویت باشد)
- امتیازدهی ستاره ای برای محصولات
- اعمال کوپن تخفیف
- امکان اعمال درصد تخفیف برای هر محصول توسط ادمین
- انبارداری و پویایی آن در صورت اضافه شدن، حذف از سبد خرید و همچنین نهایی شدن خرید
- تخفیفات ویژه
- استفاده از CKEditor به عنوان ویرایشگر برای بخش های وبلاگ و تماس
- ما می توانیم از طریق صفحه تماس از پنل مدیریت مستقیماً به کاربری که برای ما پیام ارسال کرده است پاسخ اش را بدهیم
- مدیریت نظرات کاربران در مورد هر محصول و مقاله و امکان تایید نمایش آن در صفحه توسط ادمین
- مدیریت سبد خرید توسط کاربر جاری
- امکان اشتراک گذاری محصولات و مقالات بر اساس اشتراک اجتماعی (شبکه های اجتماعی)
- پنل کاربری: امکان ویرایش اطلاعات شخصی، تغییر رمز عبور، مشاهده وضعیت سبد خرید، فاکتور خرید و ... .
- قابلیت جستجو برای محصولات و مقالات
- نمایش پربازدیدترین و پرفروش ترین محصولات
- نمایش محصولات و مقالات مرتبط
- فیلتر بر اساس برند و کتگوری
- لیست علاقه مندی ها
- گالری محصولات
- صفحه بندی
- اسلایدر
- بنرهای تبلیغاتی
- قابلیت PWA
- استفاده از SweetAlert در ساختارهای Ajax.

### Some features [en]
* Authentication system through the website itself and Google account
* Auth: Login, Logout, Register, Remember me checkbox, Sending Email active code to user for complete registration, Token Authentication, Forgot password, Reset password
* Google reCaptcha
* The automatic loss of the user's shopping cart information if it is open and does not pay within a certain period of time (I used 30 seconds for tesing purpose. If you want changing the value. Go to ~\autopart\apps\basket_order\signals.py)
* Star ratings for each product
* Apply coupon code
* The possibility of applying a discount percentage to each product by admin
* In Stock and its dynamicity in case of addition, removing from the cart and also finalizing the purchase
* Special discounts
* Using CKEditor as an editor for blog and contact sections
* We can reply directly to the user who sent us a message through the contact page from the admin panel
* Managing user comments on each product and article and possibility for confirming its display on the page by admin
* Management of the shopping cart by related user
* Ability to share products and articles by social share (Social Media)
* User panel: Possibility to edit personal information, change password, view shopping cart status, purchase invoice, etc
* PWA feature
* The dynamic nature of the website information
* Search functionality for products and articles
* Advertising banners
* Dynamic slider
* Displaying the most visited and best selling products
* Related products and articles
* Filter by category or brand
* List of favorites
* Product galleries
* Pagination
* Using SweetAlert in Ajax structures
* ...
