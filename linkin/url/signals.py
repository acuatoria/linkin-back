
from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver

from .models import UrlUser
from .tasks import clean_urls_task, update_public_urls_task, update_category_urls_task, fetch_url_info_task


@receiver(post_delete, sender=UrlUser)
def clean_urls(sender, instance, **kwargs):
    clean_urls_task.apply_async()


@receiver(post_save, sender=UrlUser)
def post_save_urluser(sender, instance, **kwargs):
    if not instance.url.title:
        fetch_url_info_task.apply_async([str(instance.url.url), ])
    update_public_urls_task.apply_async([str(instance.url.id), ])
    update_category_urls_task.apply_async([str(instance.url.id), ])
