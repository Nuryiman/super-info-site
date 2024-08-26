from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Hashtag(models.Model):
    title = models.CharField(max_length=255, verbose_name='Хэштег')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Хэштег'
        verbose_name_plural = 'Хэштеги'


class Publication(models.Model):
    is_new = models.BooleanField(default=True, verbose_name='Новое')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        related_name='publications',
        verbose_name='Категория'
    )
    title = models.CharField(max_length=100, verbose_name='Название')
    short_description = models.CharField(max_length=100, verbose_name='Краткое описание')
    description = RichTextField(verbose_name='Описание')
    image = models.ImageField(null=True, verbose_name='Изображение')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    hashtags = models.ManyToManyField(
        Hashtag,
        null=True,
        related_name='publications',
        verbose_name='Хэштеги'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

class PublicationComment(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateField(auto_now_add=True, null=True, verbose_name='Дата создания')
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
        verbose_name='Публикация'
    )

    class Meta:
        verbose_name = 'Комментарий к публикации'
        verbose_name_plural = 'Комментарии к публикациям'


class Address(models.Model):
    address = models.CharField(max_length=100, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')
    last_text = models.CharField(max_length=100, verbose_name='Последний текст')

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class SocialNetwork(models.Model):
    facebook = models.URLField(verbose_name='Facebook')
    instagram = models.URLField(verbose_name='Instagram')
    twitter = models.URLField(verbose_name='Twitter')
    youtube = models.URLField(verbose_name='YouTube')

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'


class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    subject = models.CharField(max_length=50, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
