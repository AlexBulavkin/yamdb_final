from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер для User."""

    def create_user(self, username, email, password=None, role='', bio=''):
        """Создает и возвращает пользователя с имэйлом и именем."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            bio=bio)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,
                         password=None, role='', bio=''):
        """Создает и возввращает пользователя с привилегиями суперадмина."""
        user = self.create_user(
            username,
            email,
            password=password,
            role='',
            bio=''
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


CHOICES_ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """Кастомная модель User."""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    username = models.CharField(
        'Username',
        db_index=True,
        blank=False,
        unique=True,
        max_length=150)
    email = models.EmailField(
        'Электронная почта',
        db_index=True,
        blank=False,
        unique=True,
        max_length=254)
    first_name = models.CharField('Имя', blank=True, max_length=150)
    last_name = models.CharField('Фамилия', blank=True, max_length=150)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        default='user',
        max_length=16,
        choices=CHOICES_ROLES)

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    confirmation_code = models.SlugField(blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Пользователи'
