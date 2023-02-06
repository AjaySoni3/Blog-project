from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.db.models import Q
from .managers import CustomUserManager
import uuid


# Create your models here.

class LowercaseEmailField(models.EmailField):

    def to_python(self, value):
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            value = value.lower()
        return value


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, )
    email = LowercaseEmailField(_('email address'), unique=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Types(models.TextChoices):
        Reader = "Reader", "READER"
        Author = "Author", "AUTHOR"

    default_type = Types.Reader

    user_type = MultiSelectField(choices=Types.choices,
                                 default=[],
                                 max_choices=2,
                                 max_length=255,
                                 null=True,
                                 blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.id:
            self.user_type = self.default_type
        return super().save(*args, **kwargs)


class ReaderManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(user_type__contains=CustomUser.Types.Reader))


class ReaderAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.email


class Reader(CustomUser):
    default_type = CustomUser.Types.Reader
    objects = ReaderManager()

    class Meta:
        proxy = True

    @property
    def showAdditional(self):
        return self.readeradditional


class AuthorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(Q(user_type__contains=CustomUser.Types.Author))


class AuthorAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.email

class Author(CustomUser):
    default_type = CustomUser.Types.Author
    objects = AuthorManager()

    class Meta:
        proxy = True

    @property
    def showAdditional(self):
        return self.authoradditional

