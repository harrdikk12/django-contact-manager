from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_email(value):
    if not value.endswith('@gmail.com'):
        raise ValidationError(
            _('%(value)s  is not a valid Gmail address'),
            params={'value': value},
        )

def validate_phone(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a valid phone number'),
            params={'value': value},
        )

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator(), validate_email])
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits'), validate_phone]
    )
    
    
    def __str__(self):
        return self.name
    