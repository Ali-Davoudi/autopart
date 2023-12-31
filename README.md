# Autopart. This is a project that I develop in my spare time and I usually to implement the cool things I experience in it.

> [!NOTE]
> This project deployed on [PythonAnywhere](https://www.pythonanywhere.com/):
> - https://alidavoudi.pythonanywhere.com/

### Usage
- Get the project source
```
git clone https://github.com/ali-davoudi/autopart
```
- At the main project directory(~\autopart), create `.env ` file and based on ` .env-example ` fill the informations.

- Install `virtualenv` globally on your  `Ubuntu/Debian` distribution or anything else(It requires its own installation principles)
```
sudo apt install python3-virtualenv
```
- Then you need to create a `venv` for your project. at ~\autopart open the terminal and follow these commands:
```
python3 -m virtualenv venv
```
```
source venv/bin/activate
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
> [!TIP]
> If you want be a superuser, going to admin, working directley with features and etc. Run the following command:
```
python manage.py createsuperuser
```

> [!NOTE]
> Some hints about custom validators:
> - Password strength validation with regular expression.
> - Using BeautifulSoup4 for getting the plain text from CKEditor and validate it.

### Some features [fa]
- سیستم احراز هویت از طریق خود وب سایت و اکانت گوگل
- احراز هویت: ورود، خروج، ثبت نام، مرا به خاطر بسپار، ارسال کد فعال سازی ایمیل به کاربر برای ثبت نام، Token Authentication، فراموشی رمز عبور، بازیابی رمز عبور
- گوگل ریکپتچا
- از بین رفتن خودکار اطلاعات سبد خرید کاربر در صورت باز بودن و عدم پرداخت در مدت زمان معین (در صورت تغییر مدت زمان، از مسیر autopart\apps\basket_order\signals.py اقدام نمایید.)
- امتیازدهی ستاره ای برای محصولات
- امکان اعمال کوپن تخفیف توسط کاربر (درصورت معتبر بودن کوپن)
- امکان اعمال درصد تخفیف برای هر محصول توسط ادمین
- انبارداری و پویایی آن در صورت اضافه شدن، حذف از سبد خرید و همچنین نهایی شدن خرید
- بخش تخفیفات ویژه در صفحه اصلی، درصورتی که درصد تخفیف محصولات بالای 5 درصد باشند
- استفاده از CKEditor به عنوان ویرایشگر برای بخش های وبلاگ و تماس
- ما می‌توانیم مستقیماً از پنل مدیریت به کاربری که از طریق صفحه <**ارتباط با ما**> برای ما پیام ارسال کرده است، در صورت تمایل، پاسخش را ایمیل کنیم
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
- استفاده از SweetAlert در ساختارهای Ajax
- و ...

### Some features [en]
* Authentication system through the website itself and Google account
* Auth: Login, Logout, Register, Remember me checkbox, Sending Email active code to user for complete registration, Token Authentication, Forgot password, Reset password
* Google reCAPTCHA
* The automatic loss of the user's shopping cart information if it is open and does not pay within a certain period of time (If you want changing the value. Go to ~\autopart\apps\basket_order\signals.py)
* Star ratings for each product
* The possibility of applying a discount coupon by the user (if the coupon is valid)
* The possibility of applying a discount percentage to each product by admin
* In Stock and its dynamicity in case of addition, removing from the cart and also finalizing the purchase
* Special discounts section on the main page, if the discount percentage of the products is above 5%
* Using CKEditor as an editor for blog and contact sections
* We can email a reply directly from the admin panel to a user who has sent us a message through the contact page, if desired
* Managing user comments on each product and article and possibility for confirming its display on the page by admin
* Management of the shopping cart by related user
* Ability to share products and articles by social share (Social Media)
* User panel: Possibility to edit personal information, change password, view shopping cart status, purchase invoice, etc
* PWA feature
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
