from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse


class Communities(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название")
    about = models.TextField(max_length=500, verbose_name='О сообществе', blank=True)
    create_date = models.DateField(null=True, verbose_name='Дата создания', blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers', blank=True)
    favcolor = models.CharField(max_length=10, verbose_name='Любимый цвет', blank=True)
    avatar = models.CharField(max_length=150, verbose_name='Аватар', blank=True)

    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('community', kwargs={'name': self.name})


class Publication(models.Model):
    community = models.ForeignKey(Communities, on_delete=models.CASCADE, verbose_name='Сообщество', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор статьи', blank=True, null=True)
    name = models.CharField(max_length=120, verbose_name="Название")
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name="Текст")
    karma = models.IntegerField(verbose_name="Популярность статьи", default=0)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

    def total_karma(self):
        return self.likes.count() - self.dislikes.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('page', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = "Статьи"


class Comments(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, verbose_name='Статья', blank=True, null=True, related_name='comments_publication')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name="Текст комментария")
    status = models.BooleanField(verbose_name="Видемость статьи", default=True)
    karma = models.IntegerField(verbose_name="Популярность комментария", default=0)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Profile(models.Model):
    username = models.OneToOneField(User, verbose_name='Id ползователя', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, verbose_name='Биография', blank=True)
    birth_date = models.DateField(null=True, verbose_name='Дата рождения', blank=True)
    karma = models.IntegerField(verbose_name="Популярность пользователя", default=0)
    favcolor = models.CharField(max_length=10, verbose_name='Любимый цвет', blank=True)
    avatar = models.CharField(max_length=150, verbose_name='Аватар', blank=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
