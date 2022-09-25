from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UrlUser, Url


@receiver(post_save, sender=UrlUser)
def clean_urls(sender, instance, **kwargs):
    Url.objects.filter(urluser__isnull=True).delete()


@receiver(post_save, sender=UrlUser)
def update_public_urls(sender, instance, **kwargs):
    if UrlUser.objects.filter(url=instance.url, public=True).exists():
        instance.url.public = True
    else:
        instance.url.public = False
    instance.url.save()
