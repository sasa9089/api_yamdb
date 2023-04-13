from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from api_yamdb.settings import NUM_OF_CHAR


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    ]
    username = models.SlugField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.SlugField(
        verbose_name='Роль',
        choices=CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username[:NUM_OF_CHAR]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name = 'Произведение',
    )
    text = models.TextField(
        verbose_name = 'Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name = 'Автор',
    )
    score = models.IntegerField(
        validators=(MinValueValidator(1),MaxValueValidator(10)),
        error_messages={'validators': 'Оценка от 1 до 10.'},
        verbose_name = 'Оценка',
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique review',
            ),
        )
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name = 'Отзыв',
    )
    text = models.TextField(
        verbose_name = 'Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name = 'Автор',
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:20]

