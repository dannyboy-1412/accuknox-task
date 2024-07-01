from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class StatusChoices(models.TextChoices):
    ACCEPTED = "A", _("Accepted")
    PENDING = "P", _("Pending")

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        name = email.split("@",1)[0]
        user = self.model(email=email, first_name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField("email address", max_length=255, unique=True, validators=[EmailValidator()])
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=StatusChoices, default=StatusChoices.PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.from_user.first_name} -> {self.to_user.first_name}"

    def clean(self):
        # Check if reversed request already exists
        reversed_request = FriendRequest.objects.filter(
            from_user=self.to_user,
            to_user=self.from_user
        ).exists()

        if reversed_request:
            raise ValidationError('A reversed friend request already exists.')

        return
