import re

from django.forms import ValidationError

REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
REGEX_IMAGE_URL = '^[a-zA-Z0-9+-_.]+.(jpg|jpeg|gif|png|bmp|tiff|tga|svg)$'

def email_validate(email):
    if not re.match(REGEX_EMAIL, email):
        raise ValidationError("Invalid_Key")
    
def password_validate(password):
    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError("Invalid_Key")

def image_url_validate(image_url):
    if not re.match(REGEX_IMAGE_URL, image_url):
        raise ValidationError("Invalid Key")
