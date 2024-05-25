from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """
    email_validator = EmailValidator(
        _("You must provide a valid email address"), code="invalid_email"
    )
    def create_user(self, email, password, **extra_fields):
        """
        Create and save user with given email and password
        """
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(
                _("Base User Account: An email address is required"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save user with given email and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must be staff."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    