from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import (CASCADE, BooleanField, CharField, DateTimeField,
                              EmailField, ForeignKey, ManyToManyField, Model,
                              UniqueConstraint)
from recipes.constants import LEN_CONSTANTS as LC


class User(AbstractUser):
    username = CharField(
        'Ник-нейм',
        validators=[RegexValidator('^[\\w.@+-]+\\Z')],
        max_length=LC['name'],
        unique=True
    )
    email = EmailField('Электронная почта', unique=True)
    first_name = CharField(("Имя пользователя"), max_length=LC['name'])
    last_name = CharField('Фамилия пользователя', max_length=LC['name'])
    is_active = BooleanField(
        'Действующий пользователь',
        default=True,
        help_text='''
            Снимите галочку, если хотите
            заблокировать этого пользователя
        '''
    )
    is_superuser = BooleanField(
        'Администратор',
        default=False,
        help_text='''
            Поставьте галочку, если хотите
            сделать этого пользователя администратором
        '''
    )
    following = ManyToManyField(
        'self', through='UserSubscription',
        related_name='followers', symmetrical=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователей сайта'


class UserSubscription(Model):
    """Модель подписок."""

    follower = ForeignKey(
        User, on_delete=CASCADE,
        null=True,
        blank=False,
        related_name='follower',
        verbose_name='пользователь')
    follow_to = ForeignKey(
        User, on_delete=CASCADE,
        null=True,
        blank=False,
        related_name='follow_to',
        verbose_name='следит за')
    created = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            UniqueConstraint(
                fields=['follower', 'follow_to'],
                name='unique_subscribtion'
            )
        ]

    def __str__(self):
        return f'{self.follower} - {self.follow_to}'
