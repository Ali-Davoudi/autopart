import re

from django.core.exceptions import ValidationError

from bs4 import BeautifulSoup


# Custom validators

def validate_rate(value: int) -> int:
    """Validate rating customer comments."""
    if value > 5:
        raise ValidationError('امتیاز نمی تواند بیشتر از 5 باشد.')
    elif value <= 0:
        raise ValidationError('امتیاز نمی تواند صفر باشد.')
    else:
        return value


def validate_email(email: str) -> str:
    """Validate email address"""
    accepted_serivces = ['gmail.com', 'yahoo.com', 'protonmail.com', 'pm.me', 'hotmail.com', 'outlook.com']
    _, service = email.split('@')
    if service.lower() not in accepted_serivces:
        raise ValidationError('آدرس ایمیل از سرویس های ایمیل مشهور یا امن مانند گوگل، یاهو و... نمی باشد.')
    return email


def validate_discount(percentage: int) -> int:
    """Validate discount percentage"""
    if percentage <= 100:
        return percentage
    else:
        raise ValidationError('برای اعمال تخفیف، درصد نمی تواند بیشتر از 100 باشد.')


def validate_password_strenght(password):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$'
    if not re.match(pattern, password):
        raise ValidationError(
            'کلمه عبور باید حداقل شامل یک حرف بزرگ، یک عدد و یک کاراکتر خاص (Special character) باشد.'
        )


def validate_rich_text(message):
    """Use BeautifulSoup to strip HTML tags and get the plain text"""
    plain_text = BeautifulSoup(message, "html.parser").get_text()

    if not plain_text.strip():
        raise ValidationError('پیام شما نباید خالی باشد.')

    if len(plain_text.strip()) < 5:
        raise ValidationError('پیام شما بسیار کوتاه است.')

    return message
