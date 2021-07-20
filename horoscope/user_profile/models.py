from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify as django_slugify
from django.urls import reverse
from django.db.models.signals import post_save
# Create your models here.


def slugify(s):
    '''
    Overriding django slugify that allows to use russian words as well.
    '''

    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
                'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'y', 'э': 'e', 'ю': 'yu',
                'я': 'ya'}
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    username = models.CharField('Имя пользователя', max_length=100)
    email = models.EmailField('Email', max_length=130)
    surname = models.CharField('Фамилия', max_length=100, blank=True)
    firstname = models.CharField('Имя', max_length=100, blank=True)
    password = models.CharField('Пароль', max_length=30)
    url = models.URLField(unique=True, blank=True, db_index=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile_url', kwargs={'slug': self.name})

    def save(self, *args, **kwargs):
        self.firstname = self.firstname.title()
        self.surname = self.surname.title()
        self.url = slugify(self.username)
        super().save(*args, **kwargs)

    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    post_save.connect(create_profile, sender=User)
